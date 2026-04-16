import ast
import json
import shutil
import textwrap
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_available_drivers"
DST = ROOT / "all_device_drivers"
SKIP = {"liquid_handler.prcxi"}

OUTLIER_DECISIONS = {
    "access2_backend": {"class_name": "Access2Backend", "final_id": "access2_backend"},
    "v_spin_backend": {"class_name": "VSpinBackend", "final_id": "v_spin_backend"},
    "li_ha": {"class_name": "LiHa", "final_id": "li_ha"},
    "star_backend": {"class_name": "STARBackend", "final_id": "star_backend"},
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text())


def normalize_lines(block: str):
    return [line + "\n" for line in block.rstrip("\n").split("\n")]


def insert_before_line(text: str, lineno: int, block: str) -> str:
    lines = text.splitlines(True)
    lines[lineno - 1 : lineno - 1] = normalize_lines(block)
    return "".join(lines)


def replace_span(text: str, start_lineno: int, end_lineno: int, block: str) -> str:
    lines = text.splitlines(True)
    lines[start_lineno - 1 : end_lineno] = normalize_lines(block)
    return "".join(lines)


def module_doc_end_lineno(tree: ast.Module):
    if (
        tree.body
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(getattr(tree.body[0], "value", None), ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    ):
        return tree.body[0].end_lineno
    return 0


def add_decorator_import(text: str) -> str:
    needle = "from unilabos.registry.decorators import action, device"
    if needle in text:
        return text
    tree = ast.parse(text)
    insert_at = module_doc_end_lineno(tree) + 1 or 1
    return insert_before_line(text, insert_at, needle)


def get_classes(tree: ast.Module):
    return {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}


def base_name(expr):
    if isinstance(expr, ast.Name):
        return expr.id
    if isinstance(expr, ast.Attribute):
        return expr.attr
    return None


def samefile_ancestor_names(class_name: str, classes: dict):
    seen = set()
    stack = [class_name]
    ancestors = set()
    while stack:
        current = stack.pop()
        cls = classes.get(current)
        if cls is None:
            continue
        for base in cls.bases:
            name = base_name(base)
            if not name or name in seen:
                continue
            seen.add(name)
            ancestors.add(name)
            if name in classes:
                stack.append(name)
    return ancestors


def class_methods(cls: ast.ClassDef):
    return {
        node.name: node
        for node in cls.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def is_property_method(node):
    return any(
        isinstance(dec, ast.Name) and dec.id == "property"
        for dec in getattr(node, "decorator_list", [])
    )


def header_text(text: str, node):
    lines = text.splitlines(True)
    body_start = node.body[0].lineno if node.body else node.end_lineno + 1
    return "".join(lines[node.lineno - 1 : body_start - 1]).rstrip("\n")


def call_args(node):
    args = []
    positional = list(node.args.posonlyargs) + list(node.args.args)
    if positional and positional[0].arg == "self":
        positional = positional[1:]
    args.extend(arg.arg for arg in positional)
    if node.args.vararg:
        args.append(f"*{node.args.vararg.arg}")
    for arg in node.args.kwonlyargs:
        args.append(f"{arg.arg}={arg.arg}")
    if node.args.kwarg:
        args.append(f"**{node.args.kwarg.arg}")
    return ", ".join(args)


def wrapper_block(
    text: str,
    method_node,
    description: str,
    target_expr: str | None,
    use_super: bool = False,
):
    header = header_text(text, method_node)
    desc = json.dumps(description, ensure_ascii=False)
    call = call_args(method_node)
    name = method_node.name
    if use_super:
        callee = f"super().{name}({call})" if call else f"super().{name}()"
    else:
        assert target_expr is not None
        callee = f"{target_expr}.{name}({call})" if call else f"{target_expr}.{name}()"

    if isinstance(method_node, ast.AsyncFunctionDef):
        body = f"    return await {callee}"
    else:
        if use_super:
            body = f"    return super().{name}()"
        elif is_property_method(method_node):
            body = f"    return {target_expr}.{name}"
        else:
            body = f"    return {callee}"

    return f'  @action(auto_prefix=True, description={desc})\n{header}\n{body}'


def device_decorator_block(final_id: str, categories: list[str], description: str):
    return textwrap.dedent(
        f"""\
        @device(
          id={json.dumps(final_id, ensure_ascii=False)},
          category={json.dumps(categories, ensure_ascii=False)},
          description={json.dumps(description, ensure_ascii=False)},
        )"""
    ).rstrip("\n")


def rewrite_registry_yaml_key(path: Path, final_id: str):
    data = load_yaml(path)
    old_key = next(iter(data))
    if old_key == final_id:
        return
    payload = data[old_key]
    path.write_text(yaml.safe_dump({final_id: payload}, allow_unicode=True, sort_keys=False))


def rewrite_info_yaml_key(path: Path, final_id: str):
    data = load_yaml(path)
    device_keys = [key for key in data if key != "auto_annotation_metadata"]
    if len(device_keys) != 1:
        raise ValueError(f"Unexpected info.txt shape in {path}")
    old_key = device_keys[0]
    if old_key == final_id:
        return
    payload = data[old_key]
    meta = data.get("auto_annotation_metadata")
    rebuilt = {final_id: payload}
    if isinstance(meta, dict):
        meta = dict(meta)
        meta["registry_key"] = final_id
        rebuilt["auto_annotation_metadata"] = meta
    path.write_text(yaml.safe_dump(rebuilt, allow_unicode=True, sort_keys=False))


def action_descriptions(info_payload):
    return {
        key.removeprefix("auto-"): value["schema"]["description"]
        for key, value in info_payload["class"]["action_value_mappings"].items()
    }


def category_english(info_root, info_payload):
    tag_lookup = {}
    meta = info_root.get("auto_annotation_metadata", {})
    for bucket in ("existing_tags", "proposed_new_tags"):
        for tag in meta.get(bucket, []):
            tag_lookup[tag["name"]] = tag["name_en"]
    categories = []
    for name in info_payload.get("category", []):
        if name not in tag_lookup:
            raise KeyError(f"missing category mapping for {name}")
        categories.append(tag_lookup[name])
    return categories


def choose_driver_config(src_dir: Path):
    info_root = load_yaml(src_dir / "info.txt")
    info_keys = [key for key in info_root if key != "auto_annotation_metadata"]
    if len(info_keys) != 1:
        raise ValueError(f"Unexpected info.txt shape in {src_dir / 'info.txt'}")
    info_key = info_keys[0]
    info_payload = info_root[info_key]

    reg_root = load_yaml(src_dir / "registry.yaml")
    reg_key = next(iter(reg_root))
    reg_payload = reg_root[reg_key]

    decision = OUTLIER_DECISIONS.get(src_dir.name, {})
    final_id = decision.get("final_id", src_dir.name)
    class_name = decision.get("class_name", reg_payload["class"]["module"].split(":")[-1])

    return {
        "source_id": src_dir.name,
        "info_key": info_key,
        "final_id": final_id,
        "class_name": class_name,
        "categories": category_english(info_root, info_payload),
        "description": info_payload["description"],
        "actions": action_descriptions(info_payload),
    }


def direct_action_insertions(text: str, class_name: str, actions: dict):
    tree = ast.parse(text)
    cls = get_classes(tree)[class_name]
    methods = class_methods(cls)
    inserts = []
    for name, description in actions.items():
        node = methods.get(name)
        if node is None:
            continue
        if any(
            isinstance(dec, ast.Call)
            and (
                (isinstance(dec.func, ast.Name) and dec.func.id == "action")
                or (isinstance(dec.func, ast.Attribute) and dec.func.attr == "action")
            )
            for dec in node.decorator_list
        ):
            continue
        inserts.append(
            (
                node.lineno,
                f'  @action(auto_prefix=True, description={json.dumps(description, ensure_ascii=False)})',
            )
        )
    for lineno, block in sorted(inserts, reverse=True):
        text = insert_before_line(text, lineno, block)
    return text


def replace_method(text: str, class_name: str, method_name: str, block: str):
    tree = ast.parse(text)
    cls = get_classes(tree)[class_name]
    node = class_methods(cls)[method_name]
    start = node.decorator_list[0].lineno if node.decorator_list else node.lineno
    return replace_span(text, start, node.end_lineno, block)


def append_to_class(text: str, class_name: str, blocks: list[str]):
    if not blocks:
        return text
    tree = ast.parse(text)
    cls = get_classes(tree)[class_name]
    combined = "\n\n".join(blocks)
    return insert_before_line(text, cls.end_lineno + 1, combined)


def build_outlier_rows(src_text: str, config: dict):
    tree = ast.parse(src_text)
    classes = get_classes(tree)
    chosen = config["class_name"]
    cls = classes[chosen]
    direct = class_methods(cls)
    ancestors = samefile_ancestor_names(chosen, classes)
    rows = []
    for action_name in config["actions"]:
        if action_name in direct:
            location = "declared on chosen class"
            impl = "decorate in place"
        else:
            providers = []
            for cname, cnode in classes.items():
                if cname == chosen:
                    continue
                if action_name in class_methods(cnode):
                    providers.append(cname)
            if not providers:
                location = "missing"
                impl = "manual blocker"
            else:
                provider = providers[0]
                if provider in ancestors:
                    location = "inherited"
                    impl = "add super() wrapper"
                else:
                    location = f"sibling/helper class `{provider}`"
                    impl = "add helper-forwarding wrapper"
        rows.append((action_name, location, impl))
    return rows


def provider_target(driver_id: str, provider_name: str, ancestors: set[str]):
    if provider_name in ancestors:
        return ("super", None)
    if driver_id == "access2_backend" and provider_name == "VSpinBackend":
        return ("helper", "self._ensure_vspin_backend()")
    if driver_id == "v_spin_backend" and provider_name == "Access2Backend":
        return ("helper", "self._ensure_access2_backend()")
    if driver_id == "li_ha" and provider_name in {"TecanLiquidHandler", "EVOBackend"}:
        return ("helper", "self.backend")
    if driver_id == "li_ha" and provider_name == "RoMa":
        return ("helper", "self._ensure_roma_helper()")
    if driver_id == "star_backend" and provider_name == "UnSafe":
        return ("helper", "self.unsafe")
    if driver_id == "centrifuge" and provider_name == "Loader":
        return ("helper", "self._loader_proxy()")
    raise RuntimeError(f"No wrapper target configured for {driver_id} -> {provider_name}")


def custom_blocks_for_driver(driver_id: str):
    blocks = []
    replacements = {}
    if driver_id == "access2_backend":
        replacements["__init__"] = textwrap.dedent(
            """\
              def __init__(
                self,
                device_id: str,
                timeout: int = 60,
              ):
                print("[UNILAB] Access2Backend.__init__() called", flush=True)
                \"\"\"
                Args:
                  device_id: The libftdi id for the loader. Find using
                    `python3 -m pylibftdi.examples.list_devices`
                \"\"\"
                self._device_id = device_id
                self.io = FTDI(device_id=device_id)
                self.timeout = timeout"""
        )
        blocks.append(
            textwrap.dedent(
                """\
                  def _ensure_vspin_backend(self):
                    backend = getattr(self, "_vspin_backend", None)
                    if backend is None:
                      backend = VSpinBackend(device_id=self._device_id)
                      self._vspin_backend = backend
                    return backend"""
            )
        )
    elif driver_id == "v_spin_backend":
        replacements["__init__"] = textwrap.dedent(
            """\
              def __init__(self, device_id: Optional[str] = None):
                print("[UNILAB] VSpinBackend.__init__() called", flush=True)
                \"\"\"
                Args:
                  device_id: The libftdi id for the centrifuge. Find using `python -m pylibftdi.examples.list_devices`
                \"\"\"
                self._device_id = device_id
                self.io = FTDI(device_id=device_id)
                self._bucket_1_remainder: Optional[int] = None
                if device_id is not None:
                  self._bucket_1_remainder = _load_vspin_calibrations(device_id)"""
        )
        blocks.append(
            textwrap.dedent(
                """\
                  def _ensure_access2_backend(self):
                    backend = getattr(self, "_access2_backend", None)
                    if backend is None:
                      backend = Access2Backend(device_id=self._device_id)
                      self._access2_backend = backend
                    return backend"""
            )
        )
    elif driver_id == "li_ha":
        blocks.append(
            textwrap.dedent(
                """\
                  def _ensure_roma_helper(self):
                    helper = getattr(self, "_roma_helper_instance", None)
                    if helper is None:
                      helper = RoMa(self.backend, getattr(self.backend, "ROMA", "C1"))
                      self._roma_helper_instance = helper
                    return helper"""
            )
        )
    elif driver_id == "centrifuge":
        blocks.append(
            textwrap.dedent(
                """\
                  def _loader_proxy(self):
                    loader = getattr(self, "loader", None)
                    if loader is not None:
                      return loader
                    return self.backend"""
            )
        )
    replacements = {name: textwrap.indent(block, "  ") for name, block in replacements.items()}
    blocks = [textwrap.indent(block, "  ") for block in blocks]
    return replacements, blocks


def main():
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    configs = []
    review_sections = ["# Outlier Review", ""]

    for src_dir in sorted(p for p in SRC.iterdir() if p.is_dir() and p.name not in SKIP):
        cfg = choose_driver_config(src_dir)
        configs.append(cfg)
        shutil.copytree(src_dir, DST / cfg["final_id"])
        if cfg["final_id"] != cfg["info_key"]:
            rewrite_info_yaml_key(DST / cfg["final_id"] / "info.txt", cfg["final_id"])
            rewrite_registry_yaml_key(DST / cfg["final_id"] / "registry.yaml", cfg["final_id"])

    for cfg in configs:
        driver_path = DST / cfg["final_id"] / "driver.py"
        text = driver_path.read_text()
        text = add_decorator_import(text)

        tree = ast.parse(text)
        cls = get_classes(tree)[cfg["class_name"]]
        text = insert_before_line(
            text,
            cls.lineno,
            device_decorator_block(cfg["final_id"], cfg["categories"], cfg["description"]),
        )

        replacements, helper_blocks = custom_blocks_for_driver(cfg["source_id"])
        for method_name, block in replacements.items():
            text = replace_method(text, cfg["class_name"], method_name, block)

        text = direct_action_insertions(text, cfg["class_name"], cfg["actions"])

        tree = ast.parse(text)
        classes = get_classes(tree)
        chosen_cls = classes[cfg["class_name"]]
        chosen_methods = class_methods(chosen_cls)
        ancestors = samefile_ancestor_names(cfg["class_name"], classes)

        wrapper_blocks = []
        for action_name, description in cfg["actions"].items():
            if action_name in chosen_methods:
                continue

            providers = []
            for cname, cnode in classes.items():
                if cname == cfg["class_name"]:
                    continue
                methods = class_methods(cnode)
                if action_name in methods:
                    providers.append((cname, methods[action_name]))

            if not providers:
                raise RuntimeError(f'Missing provider for {cfg["source_id"]}:{action_name}')

            provider_name, provider_node = providers[0]
            mode, target = provider_target(cfg["source_id"], provider_name, ancestors)
            wrapper_blocks.append(
                wrapper_block(text, provider_node, description, target, use_super=(mode == "super"))
            )

        text = append_to_class(text, cfg["class_name"], helper_blocks + wrapper_blocks)
        ast.parse(text)
        driver_path.write_text(text)

        if cfg["source_id"] in OUTLIER_DECISIONS:
            src_text = (SRC / cfg["source_id"] / "driver.py").read_text()
            rows = build_outlier_rows(src_text, cfg)
            retained = "retained" if cfg["final_id"].endswith("_backend") else "removed"
            review_sections.extend(
                [
                    f'## {cfg["source_id"]}',
                    "",
                    f'- Chosen decorated class: `{cfg["class_name"]}`',
                    f'- Final staged id: `{cfg["final_id"]}`',
                    f'- Final staged folder: `{cfg["final_id"]}`',
                    f'- `_backend` suffix: {retained}',
                    "",
                    "| Action | Current location | Implementation action |",
                    "| --- | --- | --- |",
                ]
            )
            for action_name, location, impl in rows:
                review_sections.append(f"| `{action_name}` | {location} | {impl} |")
            review_sections.append("")

    (DST / "_outlier_review.md").write_text("\n".join(review_sections).rstrip() + "\n")

    for cfg in configs:
        driver_path = DST / cfg["final_id"] / "driver.py"
        text = driver_path.read_text()
        tree = ast.parse(text)
        classes = get_classes(tree)
        chosen = classes[cfg["class_name"]]
        methods = class_methods(chosen)

        device_decorated = [
            node
            for node in classes.values()
            if any(
                isinstance(dec, ast.Call)
                and (
                    (isinstance(dec.func, ast.Name) and dec.func.id == "device")
                    or (isinstance(dec.func, ast.Attribute) and dec.func.attr == "device")
                )
                for dec in node.decorator_list
            )
        ]
        assert len(device_decorated) == 1, f'{cfg["final_id"]}: expected exactly one @device'

        for action_name in cfg["actions"]:
            assert action_name in methods, (
                f'{cfg["final_id"]}: action {action_name} missing from chosen class body'
            )
            node = methods[action_name]
            assert any(
                isinstance(dec, ast.Call)
                and (
                    (isinstance(dec.func, ast.Name) and dec.func.id == "action")
                    or (isinstance(dec.func, ast.Attribute) and dec.func.attr == "action")
                )
                for dec in node.decorator_list
            ), f'{cfg["final_id"]}: action {action_name} missing @action decorator'

    print(f"Generated staged drivers: {len(configs)}")
    for cfg in configs:
        print(f'{cfg["final_id"]}: {len(cfg["actions"])} actions')


if __name__ == "__main__":
    main()
