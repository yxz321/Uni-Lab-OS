"""包上传同时兼容根目录遗留 registry.yaml 和 AST @device 注册。"""

from pathlib import Path

from unilabos.app.package_cli import inspect_package


def _write_mixed_package(pkg_dir: Path) -> None:
    pkg_dir.mkdir()
    (pkg_dir / "pyproject.toml").write_text(
        """
[project]
name = "mixed-registry-package"
version = "1.2.3"
""".strip(),
        encoding="utf-8",
    )
    (pkg_dir / "driver.py").write_text(
        """
from unilabos.registry.decorators import action, device


@device(id="ast_device", description="AST device")
class AstDevice:
    @action(description="Run AST action")
    def run(self, cycles: int = 1):
        return cycles
""".strip(),
        encoding="utf-8",
    )
    (pkg_dir / "registry.yaml").write_text(
        """
legacy_yaml_device:
  resource_type: device
  description: Legacy YAML device
  legacy_marker: keep-me
  class:
    module: mixed_registry_package.legacy:LegacyDevice
    type: python
    action_value_mappings:
      setup:
        type: UniLabJsonCommand
        goal:
          type: object
          properties: {}
""".strip(),
        encoding="utf-8",
    )


def test_inspect_package_merges_ast_devices_with_root_legacy_registry(tmp_path):
    pkg_dir = tmp_path / "mixed_registry_package"
    _write_mixed_package(pkg_dir)

    info = inspect_package(str(pkg_dir), out_dir=str(tmp_path / "dist"))

    assert set(info["devices"]) == {"ast_device", "legacy_yaml_device"}
    by_id = {resource["id"]: resource for resource in info["resources"]}

    # 旧 YAML 条目仍原样用作 source_registry。
    assert by_id["legacy_yaml_device"]["source_registry"]["legacy_marker"] == "keep-me"
    assert "setup" in by_id["legacy_yaml_device"]["class"]["action_value_mappings"]

    # 根目录 YAML 不再屏蔽 Python 中的 @device。
    ast_resource = by_id["ast_device"]
    assert ast_resource["class"]["module"].endswith("driver:AstDevice")
    run_action = ast_resource["class"]["action_value_mappings"]["run"]
    assert run_action["schema"] == {
        "title": "run参数",
        "description": "Run AST action",
        "type": "object",
        "properties": {
            "goal": {
                "type": "object",
                "properties": {
                    "cycles": {
                        "type": "integer",
                        "title": "cycles",
                    },
                },
            },
            "feedback": {
                "type": "object",
                "properties": {},
            },
            "result": {
                "type": "object",
                "properties": {},
            },
        },
        "required": ["goal"],
    }


def test_inspect_package_includes_nested_community_registry(tmp_path):
    pkg_dir = tmp_path / "mixed_registry_package"
    _write_mixed_package(pkg_dir)
    community_dir = pkg_dir / "community_bio" / "up20"
    community_dir.mkdir(parents=True)
    (community_dir / "registry.yaml").write_text(
        """
interson_up20:
  resource_type: device
  class:
    module: mixed_registry_package.community_bio.up20.driver:Interson
    type: python
    action_value_mappings: {}
""".strip(),
        encoding="utf-8",
    )

    info = inspect_package(str(pkg_dir), out_dir=str(tmp_path / "dist"))

    assert set(info["devices"]) == {"ast_device", "interson_up20", "legacy_yaml_device"}
    by_id = {resource["id"]: resource for resource in info["resources"]}
    assert (
        by_id["interson_up20"]["class"]["module"]
        == "mixed_registry_package.community_bio.up20.driver:Interson"
    )
