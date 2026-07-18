"""模型文件上传/下载管理。

提供 Edge 端本地模型文件与 OSS 之间的双向同步：
- upload_device_model: 本地模型 → OSS（Edge 首次接入时）
- download_model_from_oss: OSS → 本地（新 Edge 加入已有 Lab 时）
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Optional

import requests

from unilabos.utils.log import logger

if TYPE_CHECKING:
    from unilabos.app.web.client import HTTPClient

# 设备 mesh 根目录
_MESH_BASE_DIR = Path(__file__).parent.parent / "device_mesh"

# 支持的模型文件后缀
_MODEL_EXTENSIONS = frozenset({
    ".xacro", ".urdf", ".stl", ".dae", ".obj",
    ".gltf", ".glb", ".fbx", ".yaml", ".yml",
})

# 需要 XOR 加密/解密的 mesh 文件后缀（反爬保护 — 方案 C）
_MESH_ENCRYPT_EXTENSIONS = frozenset({
    ".stl", ".dae", ".obj", ".fbx", ".gltf", ".glb",
})

# 可作为前端模型入口的格式。依赖文件仍由 _MODEL_EXTENSIONS 控制。
_ENTRY_FORMATS = {
    ".xacro": "xacro",
    ".urdf": "urdf",
    ".stl": "stl",
    ".gltf": "gltf",
    ".glb": "gltf",
    ".fbx": "fbx",
    ".obj": "obj",
}

# XOR 密钥 — 从环境变量读取，与前端 mesh-decrypt.ts 一致
_XOR_KEY = os.environ.get("UNILAB_MESH_XOR_KEY", "unilab3d-model-protection-key-v1").encode()


def _xor_transform(data: bytes, key: bytes = _XOR_KEY) -> bytes:
    """XOR 加密/解密（对称操作）。"""
    key_len = len(key)
    return bytes(b ^ key[i % key_len] for i, b in enumerate(data))


@dataclass(frozen=True)
class _ModelUploadFile:
    """待上传的本地模型文件及其 OSS 相对路径。"""

    name: str
    local_path: Path
    size_kb: int


def _legacy_model_source(mesh_name: str, model_type: str) -> Path:
    """保留旧版 device_mesh 目录约定，供未传 model_source 的调用方使用。"""
    if model_type == "device":
        return _MESH_BASE_DIR / "devices" / mesh_name
    return _MESH_BASE_DIR / "resources" / mesh_name


def _collect_model_files(model_source: Path) -> list[_ModelUploadFile]:
    """从单文件或目录收集模型文件，并生成 POSIX 风格相对路径。"""
    if model_source.is_file():
        if model_source.suffix.lower() not in _MODEL_EXTENSIONS:
            return []
        return [_ModelUploadFile(
            name=model_source.name,
            local_path=model_source,
            size_kb=model_source.stat().st_size // 1024,
        )]

    files = []
    for local_path in sorted(model_source.rglob("*")):
        if local_path.is_file() and local_path.suffix.lower() in _MODEL_EXTENSIONS:
            files.append(_ModelUploadFile(
                name=local_path.relative_to(model_source).as_posix(),
                local_path=local_path,
                size_kb=local_path.stat().st_size // 1024,
            ))
    return files


def _normalize_entry_file(entry_file: str) -> str:
    """规范化入口相对路径并拒绝绝对路径或目录穿越。"""
    normalized = PurePosixPath(entry_file.replace("\\", "/"))
    if normalized.is_absolute() or ".." in normalized.parts:
        raise ValueError(f"非法模型入口路径: {entry_file}")
    return normalized.as_posix()


def _select_entry_file(
    files: list[_ModelUploadFile],
    model_type: str,
    entry_file: Optional[str],
) -> str:
    """选择发布入口；显式入口优先，否则按兼容约定安全推断。"""
    names = {file.name for file in files}
    if entry_file:
        selected = _normalize_entry_file(entry_file)
        if selected not in names:
            raise ValueError(f"模型入口文件不存在或未被收集: {selected}")
        if PurePosixPath(selected).suffix.lower() not in _ENTRY_FORMATS:
            raise ValueError(f"不支持作为模型入口的文件类型: {selected}")
        return selected

    # 先保留旧目录的命名约定，同时兼容外部资产常用的 modal.xacro。
    preferred = (
        ("macro_device.xacro", "modal.xacro")
        if model_type == "device"
        else ("modal.xacro", "macro_device.xacro")
    )
    for candidate in preferred:
        if candidate in names:
            return candidate

    root_descriptions = [
        file.name for file in files
        if "/" not in file.name
        and PurePosixPath(file.name).suffix.lower() in {".xacro", ".urdf"}
    ]
    if len(root_descriptions) == 1:
        return root_descriptions[0]

    description_files = [
        file.name for file in files
        if PurePosixPath(file.name).suffix.lower() in {".xacro", ".urdf"}
    ]
    if len(description_files) == 1:
        return description_files[0]

    entry_candidates = [
        file.name for file in files
        if PurePosixPath(file.name).suffix.lower() in _ENTRY_FORMATS
    ]
    if len(entry_candidates) == 1:
        return entry_candidates[0]

    raise ValueError("无法唯一确定模型入口文件，请显式传入 entry_file")


def _entry_format(entry_file: str) -> str:
    """从入口扩展名推断前端 model.format。"""
    suffix = PurePosixPath(entry_file).suffix.lower()
    model_format = _ENTRY_FORMATS.get(suffix)
    if not model_format:
        raise ValueError(f"不支持作为模型入口的文件类型: {entry_file}")
    return model_format


def upload_device_model(
    http_client: "HTTPClient",
    template_uuid: str,
    mesh_name: str,
    model_type: str,
    version: str = "1.0.0",
    *,
    model_source: Optional[str | Path] = None,
    entry_file: Optional[str] = None,
) -> Optional[str]:
    """上传本地模型文件或模型包到 OSS，返回入口文件的 OSS URL。

    ``model_source`` 可直接指向外部模型目录或单个模型文件。省略时继续使用
    ``device_mesh/{devices|resources}/{mesh_name}`` 旧目录约定。

    Args:
        http_client: HTTPClient 实例
        template_uuid: 设备模板 UUID
        mesh_name: mesh 目录名（如 "arm_slider"）
        model_type: "device" 或 "resource"
        version: 模型版本
        model_source: 显式本地模型文件/目录；省略时使用旧版内置目录
        entry_file: 目录内的显式入口相对路径；省略时自动推断

    Returns:
        入口文件 OSS URL，上传失败返回 None
    """
    source = (
        Path(model_source).expanduser()
        if model_source is not None
        else _legacy_model_source(mesh_name, model_type)
    )
    if not source.exists():
        logger.warning(f"[模型上传] 本地模型不存在: {source}")
        return None

    try:
        files = _collect_model_files(source)
        if not files:
            logger.warning(f"[模型上传] 未找到可上传的模型文件: {source}")
            return None

        selected_entry = _select_entry_file(files, model_type, entry_file)
        model_format = _entry_format(selected_entry)

        # 1. 获取预签名上传 URL
        upload_urls_resp = http_client.get_model_upload_urls(
            template_uuid=template_uuid,
            files=[{"name": file.name, "version": version} for file in files],
        )
        if not upload_urls_resp:
            return None

        url_items = upload_urls_resp.get("files", [])
        upload_targets = {
            item.get("name"): item.get("upload_url")
            for item in url_items
            if item.get("name")
        }

        # 2. 逐个上传文件
        for file in files:
            upload_url = upload_targets.get(file.name, "")
            if not upload_url:
                raise ValueError(f"未获取到模型文件上传地址: {file.name}")
            _put_upload(file.local_path, upload_url)

        # 3. 确认发布
        encrypted = any(
            file.local_path.suffix.lower() in _MESH_ENCRYPT_EXTENSIONS
            for file in files
        )
        publish_resp = http_client.publish_model(
            template_uuid=template_uuid,
            version=version,
            entry_file=selected_entry,
            encrypted=encrypted,
        )
        if not publish_resp:
            return None

        # 4. 当前 HTTPClient 支持时补充 format/files；旧版客户端仍可正常上传。
        update_template_model = getattr(http_client, "update_template_model", None)
        if callable(update_template_model):
            update_resp = update_template_model(
                template_uuid=template_uuid,
                model={
                    "format": model_format,
                    "files": [
                        {"name": file.name, "size_kb": file.size_kb}
                        for file in files
                    ],
                },
            )
            if update_resp is None:
                logger.warning(f"[模型上传] 模型已发布，但 format/files 更新失败: {mesh_name}")

        return publish_resp.get("path")

    except Exception as e:
        logger.error(f"[模型上传] 上传失败 ({mesh_name}): {e}")
        return None


def download_model_from_oss(
    model_config: dict,
    mesh_base_dir: Optional[Path] = None,
) -> bool:
    """检查本地模型文件是否存在，不存在则从 OSS 下载。

    Args:
        model_config: 节点的 model 配置字典
        mesh_base_dir: mesh 根目录，默认使用 device_mesh/

    Returns:
        True 表示本地文件就绪，False 表示下载失败或无需下载
    """
    if mesh_base_dir is None:
        mesh_base_dir = _MESH_BASE_DIR

    mesh_name = model_config.get("mesh", "")
    model_type = model_config.get("type", "")
    oss_path = model_config.get("path", "")

    if not mesh_name or not oss_path or not oss_path.startswith("https://"):
        return False

    # 确定本地目标目录
    if model_type == "device":
        local_dir = mesh_base_dir / "devices" / mesh_name
    elif model_type == "resource":
        resource_name = mesh_name.split("/")[0]
        local_dir = mesh_base_dir / "resources" / resource_name
    else:
        return False

    # 已有本地文件 → 跳过
    if local_dir.exists() and any(local_dir.iterdir()):
        return True

    # 从 OSS 下载
    local_dir.mkdir(parents=True, exist_ok=True)
    try:
        # 下载入口文件（OSS URL 通常直接可访问）
        entry_name = oss_path.rsplit("/", 1)[-1]
        _download_file(oss_path, local_dir / entry_name)

        # 如果有 children_mesh，也下载
        children_mesh = model_config.get("children_mesh")
        if isinstance(children_mesh, dict) and children_mesh.get("path"):
            cm_path = children_mesh["path"]
            if cm_path.startswith("https://"):
                cm_name = cm_path.rsplit("/", 1)[-1]
                meshes_dir = local_dir / "meshes"
                meshes_dir.mkdir(parents=True, exist_ok=True)
                _download_file(cm_path, meshes_dir / cm_name)

        logger.info(f"[模型下载] 成功下载模型到本地: {mesh_name} → {local_dir}")
        return True

    except Exception as e:
        logger.warning(f"[模型下载] 下载失败 ({mesh_name}): {e}")
        return False


def _put_upload(local_path: Path, upload_url: str) -> None:
    """通过预签名 URL 上传文件到 OSS。对 mesh 文件自动 XOR 加密。"""
    with open(local_path, "rb") as f:
        data = f.read()
    # 对 mesh 文件 XOR 加密后上传（反爬保护 — 方案 C）
    if local_path.suffix.lower() in _MESH_ENCRYPT_EXTENSIONS:
        data = _xor_transform(data)
        logger.debug(f"[模型上传] XOR 加密: {local_path.name}")
    resp = requests.put(upload_url, data=data, timeout=120)
    resp.raise_for_status()
    logger.debug(f"[模型上传] 已上传: {local_path.name}")


def _download_file(url: str, local_path: Path) -> None:
    """下载单个文件到本地路径。对 mesh 文件自动 XOR 解密。"""
    local_path.parent.mkdir(parents=True, exist_ok=True)
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    data = resp.content
    # 从 OSS 下载的 mesh 文件是加密的，需要 XOR 解密后再存本地
    if local_path.suffix.lower() in _MESH_ENCRYPT_EXTENSIONS:
        data = _xor_transform(data)
        logger.debug(f"[模型下载] XOR 解密: {local_path.name}")
    local_path.write_bytes(data)
    logger.debug(f"[模型下载] 已下载: {local_path}")
