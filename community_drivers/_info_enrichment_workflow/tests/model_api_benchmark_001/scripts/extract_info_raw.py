#!/usr/bin/env python3
"""
Deterministic local signal extractor for v4 enrichment workflow.

Produces 01_local_signals.json per device with:
- Registry fields split by reliability
- Driver AST with focal-class method extraction and function-type annotation
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
from typing import Any

import yaml


COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
TEST_ROOT = COMMUNITY_DIR / '_info_enrichment_workflow' / 'tests' / 'model_api_benchmark_001'


# ─────────────────────── Registry extraction ───────────────────────


def pick_registry_entry(device: str, registry_data: Any) -> tuple[str, dict[str, Any], list[str]]:
    if isinstance(registry_data, dict):
        if device in registry_data and isinstance(registry_data[device], dict):
            siblings = [k for k in registry_data.keys() if k != device]
            return device, registry_data[device], siblings
        first_key = next(iter(registry_data.keys()), None)
        if isinstance(first_key, str) and isinstance(registry_data[first_key], dict):
            siblings = [k for k in registry_data.keys() if k != first_key]
            return first_key, registry_data[first_key], siblings
    return device, {}, []


def extract_focal_class_name(entry: dict[str, Any]) -> str:
    """Extract the focal class name from the registry module field.

    Module format: 'unilabos.devices.<category>.<module_file>:<ClassName>'
    Returns the part after ':', or empty string if not found.
    """
    cls = entry.get('class') or {}
    module = cls.get('module', '') or ''
    if ':' in module:
        return module.rsplit(':', 1)[1]
    return ''


def extract_status_type_keys(entry: dict[str, Any]) -> list[str]:
    cls = entry.get('class') or {}
    st = cls.get('status_types') or {}
    if isinstance(st, dict):
        return list(st.keys())
    return []


def extract_registry_actions(entry: dict[str, Any]) -> list[str]:
    """Return compact one-liner per action, e.g. 'auto-reset (from reset())'."""
    mappings = ((entry.get('class') or {}).get('action_value_mappings')) or {}
    actions = []
    if not isinstance(mappings, dict):
        return actions
    for action_name, spec in mappings.items():
        spec = spec or {}
        schema = spec.get('schema') or {}
        title = schema.get('title', '')
        if title and title != action_name:
            actions.append(f"{action_name} (from {title}())")
        else:
            actions.append(action_name)
    return actions


def extract_registry_signals(entry: dict[str, Any]) -> dict[str, Any]:
    """Extract registry fields, organized by reliability."""
    cls = entry.get('class') or {}
    return {
        'name': entry.get('name', ''),
        'category': entry.get('category', []),
        'manufacturer': entry.get('manufacturer', ''),
        'model': entry.get('model', {}),
        'description': entry.get('description', ''),
        'module': cls.get('module', ''),
        'status_types': extract_status_type_keys(entry),
        'tags': entry.get('tags', []),
        'scene': entry.get('scene', {}),
        'actions': extract_registry_actions(entry),
    }


# ─────────────────────── Function type annotation ───────────────────────


def classify_function_type(method_name: str, status_keys: set[str],
                           has_value_param: bool = False) -> str:
    """Classify a method as status_getter, status_setter, or command.

    A method is a status_getter/setter if its name (with get_/set_ prefix
    stripped) matches a key in status_types.

    For property-style methods (no get_/set_ prefix), the presence of a
    non-self parameter distinguishes setters from getters.
    """
    bare = method_name
    explicit_getter = False
    explicit_setter = False

    if bare.startswith('get_'):
        bare = bare[4:]
        explicit_getter = True
    elif bare.startswith('set_'):
        bare = bare[4:]
        explicit_setter = True

    if bare in status_keys:
        if explicit_getter:
            return 'status_getter'
        if explicit_setter:
            return 'status_setter'
        # Property-style: use parameter count to distinguish
        return 'status_setter' if has_value_param else 'status_getter'

    return 'command'


# ─────────────────────── Driver AST extraction ───────────────────────


def format_args(fn: ast.AST) -> str:
    if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return '()'
    parts = []
    args = fn.args
    positional = list(args.posonlyargs) + list(args.args)
    defaults = [None] * (len(positional) - len(args.defaults)) + list(args.defaults)
    for arg, default in zip(positional, defaults):
        text = arg.arg
        if default is not None:
            try:
                text += '=' + ast.unparse(default)
            except Exception:
                text += '=...'
        parts.append(text)
    if args.vararg:
        parts.append('*' + args.vararg.arg)
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        text = arg.arg
        if default is not None:
            try:
                text += '=' + ast.unparse(default)
            except Exception:
                text += '=...'
        parts.append(text)
    if args.kwarg:
        parts.append('**' + args.kwarg.arg)
    return '(' + ', '.join(parts) + ')'


def collect_comments(lines: list[str], func_node: ast.AST) -> list[str]:
    """Collect all documentation for a method: comments above the def,
    standalone comments inside the body, and embedded docstrings (string
    literals that ast.get_docstring misses when they aren't the first stmt).

    Returns a flat list of text snippets in source order.
    """
    comments: list[str] = []

    # 1. Comments above the def line
    above: list[str] = []
    i = func_node.lineno - 2  # 0-indexed, line before def
    while i >= 0:
        stripped = lines[i].strip()
        if not stripped:
            if above:
                break
            i -= 1
            continue
        if stripped.startswith('#'):
            above.append(stripped.lstrip('#').strip())
            i -= 1
            continue
        break
    above.reverse()
    comments.extend(above)

    # 2. Walk the function body for inline comments and embedded docstrings
    if not hasattr(func_node, 'body'):
        return comments

    end_lineno = getattr(func_node, 'end_lineno', None)
    if end_lineno is None:
        return comments

    # Collect line numbers occupied by child AST nodes so we can find
    # comment-only lines in between
    body_start = func_node.body[0].lineno if func_node.body else func_node.lineno + 1
    body_end = end_lineno  # inclusive

    # Scan source lines inside the function body
    for li in range(body_start - 1, min(body_end, len(lines))):
        stripped = lines[li].strip()
        if stripped.startswith('#'):
            text = stripped.lstrip('#').strip()
            if text:
                comments.append(text)

    # Pick up string-literal docstrings that aren't the first statement
    # (ast.get_docstring only finds the first Expr(Constant(str)))
    for stmt in func_node.body:
        if (isinstance(stmt, ast.Expr) and
                isinstance(stmt.value, ast.Constant) and
                isinstance(stmt.value.value, str)):
            doc = stmt.value.value.strip()
            if doc:
                comments.append(doc)

    return comments


def extract_driver(device_dir: Path, focal_class_name: str, status_keys: set[str]) -> dict[str, Any]:
    """Parse driver.py and extract AST with focal-class focus.

    - All classes get name, line, bases, docstring
    - Only the focal class gets full method extraction with function_type
    - If focal_class_name is empty, the first class is treated as focal
    """
    driver_path = device_dir / 'driver.py'
    text = driver_path.read_text(encoding='utf-8')
    lines = text.splitlines()
    tree = ast.parse(text)
    module_doc = ast.get_docstring(tree) or ''

    all_classes: list[dict[str, Any]] = []
    focal_class = focal_class_name
    focal_methods: list[dict[str, Any]] = []
    found_focal = False

    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        is_focal = (
            (focal_class and node.name == focal_class) or
            (not focal_class and not found_focal)
        )

        cls_entry: dict[str, Any] = {
            'name': node.name,
            'bases': [ast.unparse(base) if hasattr(ast, 'unparse') else '' for base in node.bases],
            'docstring': ast.get_docstring(node) or '',
            'is_focal': is_focal,
        }
        all_classes.append(cls_entry)

        if is_focal:
            found_focal = True
            if not focal_class:
                focal_class = node.name
            for child in node.body:
                if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if child.name.startswith('_'):
                    continue
                non_self_params = [a.arg for a in child.args.args if a.arg != 'self']
                func_type = classify_function_type(
                    child.name, status_keys,
                    has_value_param=len(non_self_params) > 0,
                )
                focal_methods.append({
                    'function_type': func_type,
                    'function': f"{child.name}{format_args(child)}",
                    'comments': collect_comments(lines, child),
                })

    return {
        'module_docstring': module_doc,
        'all_classes': all_classes,
        'focal_class': focal_class or '',
        'focal_methods': focal_methods,
    }


# ─────────────────────── Output ───────────────────────


def build_local_signals(device: str, registry_signals: dict[str, Any],
                        driver_data: dict[str, Any]) -> dict[str, Any]:
    return {
        'device': device,
        'registry': registry_signals,
        'driver': driver_data,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--devices-file', type=Path, default=TEST_ROOT / 'devices.txt')
    parser.add_argument('--output-dir', type=Path, default=TEST_ROOT / 'materials')
    args = parser.parse_args()

    devices = [
        line.strip()
        for line in args.devices_file.read_text(encoding='utf-8').splitlines()
        if line.strip() and not line.startswith('#')
    ]

    for device in devices:
        device_dir = COMMUNITY_DIR / device
        registry_path = device_dir / 'registry.yaml'
        registry_data = yaml.safe_load(registry_path.read_text(encoding='utf-8'))
        _, entry, _ = pick_registry_entry(device, registry_data)

        focal_class_name = extract_focal_class_name(entry)
        status_keys = set(extract_status_type_keys(entry))
        registry_signals = extract_registry_signals(entry)
        driver_data = extract_driver(device_dir, focal_class_name, status_keys)

        signals = build_local_signals(device, registry_signals, driver_data)

        out_dir = args.output_dir / device
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / '01_local_signals.json').write_text(
            json.dumps(signals, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )

    print(f'generated 01_local_signals.json for {len(devices)} devices into {args.output_dir}')


if __name__ == '__main__':
    main()
