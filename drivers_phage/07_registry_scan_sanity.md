Reference: see `Uni-Lab-OS/drivers_phage/00_project_rules.md`.

# Registry Scan Sanity Check

## Decorator pattern

Validated against:

- `unilabos/devices/virtual/workbench.py` lines `112-150` and `293-310`
- `unilabos/registry/decorators.py`

Every guessed driver:

- imports `device` and `action` from `unilabos.registry.decorators`
- applies `@device(...)` to a class
- applies `@action()` to each exported method

## Scanner behavior

Validated against `unilabos/registry/ast_registry_scanner.py`.

- `_collect_py_files()` includes every `.py` file whose name does not start with `__`
- `scan_directory()` recursively parses those files
- there is no filename restriction to `driver.py`

Result:

- `driver_guessed.py` files are discoverable without renaming

## Syntax check

`python3` + `ast.parse()` succeeded for every generated `driver_guessed.py` file.
