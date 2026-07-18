---
name: upload-external-package
description: Upload an external Uni-Lab-OS device package to Device Square, including YAML registry packages, AST @device packages, optional 3D model upload, model path patching, and real-vs-virtual device distinctions. Use when asked to upload external packages, community packages, registry.yaml packages, package models, or Device Square templates.
---

# Upload External Package To Device Square

## Core Workflow

- Use the active `LeapLab/Uni-Lab-OS` checkout for `unilabos.app.package_cli`; avoid stale installed CLI code.
- Use the package's existing `pyproject.toml` if present. Create a minimal one only when absent.
- Determine registry source before editing:
  - AST style: device classes already use `@device`; do not construct YAML for those devices.
  - YAML style: root `registry.yaml` defines devices; use this for unchanged external drivers or plain classes.
  - Mixed packages are allowed only if device IDs do not duplicate between AST and YAML.
- Validate locally with `inspect_package`, then upload with AK/SK; never write secrets into package files or scratch JSON.

## YAML Device Conventions

- Use a root mapping keyed by stable ASCII `device_id`.
- Each device should include:
  - `version`, `resource_type: device`
  - `category`, `displayname`, `description` (Chinese-facing metadata when publishing to square)
  - `model` if a 3D model exists
  - `init_param_schema`
  - `class.module`, `class.type: python`, `class.init`, `class.action_value_mappings`, `class.status_types`
- Keep external/raw drivers unchanged; point `class.module` at real importable classes.
- Put every `${config.*}` placeholder used in `class.init` into `init_param_schema.config.properties` and `required`.
- Expose real parameterized actions in `class.action_value_mappings`; do not ship setup-only devices.
- Prefer public hardware operations; skip private/internal helpers and object-rich parameters unless the caller can provide resolvable resource/device IDs.
- For one class with many models, create multiple YAML entries sharing the class but differing metadata, model, and init/backend config.
- For real devices, avoid `mock`, `virtual`, `chatterbox`, and `simulator` backends or descriptions.

## Upload Without Models

- Run `inspect_package(<package_path>)` with `PYTHONPATH=<LeapLab/Uni-Lab-OS>[:<package_path>]`.
- Confirm:
  - source is expected (`registry.yaml` or AST scan)
  - resource count and device IDs are correct
  - `source_registry` exists
  - display names, descriptions, config schema, and action schemas are present
- Upload the package to the target addr, then save only sanitized response summaries.

## Upload With Models

- Pass the local model source explicitly to `upload_device_model`; it may be a model directory or one standalone model file anywhere on disk.
- Do not create temporary symlinks or mutate `model_upload._MESH_BASE_DIR`. That private global remains only as the backward-compatible fallback when `model_source` is omitted.
- Keep local source location separate from `model.mesh`: `model_source` locates local bytes, while `mesh` is the stable remote namespace used in `model/<mesh>/<version>/`.
- Choose the registry `format` from the published entry file, not from the local
  folder name:

| Entry file | Registry `format` | Upload shape | Frontend axis contract |
| --- | --- | --- | --- |
| `.xacro` | `xacro` | Bundle | ROS Z-up; frontend rotates it into the Y-up scene |
| `.urdf` | `urdf` | Bundle | ROS Z-up; frontend rotates it into the Y-up scene |
| `.stl` | `stl` | Normally standalone | See the STL axis caveat below |
| `.glb` | `gltf` | Standalone/self-contained | Standard glTF Y-up; no extra model rotation |
| `.gltf` | `gltf` | Standalone only when self-contained; otherwise bundle its dependencies | Standard glTF Y-up; no extra model rotation |

- Never write `format: glb`; both `.glb` and `.gltf` publish as `format: gltf`.
- Supported layouts include:

```text
# XACRO/URDF bundle
device_models_zup/<mesh>/modal.xacro
device_models_zup/<mesh>/meshes/*

# Standalone STL
device_models_zup/<mesh>/<mesh>.stl

# Standalone binary glTF
device_models/<mesh>/<mesh>.glb

# JSON glTF with external dependencies (prefer GLB when possible)
device_models/<mesh>/<mesh>.gltf
device_models/<mesh>/<referenced .bin and texture files>
```

- XACRO device model block:

```yaml
model:
  type: device
  format: xacro
  mesh: <mesh_folder>
  mesh_tf: [0, 0, 0, 0, 0, 0]
  encrypted: true
  path: ""
```

- Standalone STL device model block:

```yaml
model:
  type: device
  format: stl
  mesh: <mesh_name>
  mesh_tf: [0, 0, 0, 0, 0, 0]
  encrypted: true
  path: ""
```

- Standalone GLB/GLTF device model block (`format` is `gltf` even when the file
  extension is `.glb`):

```yaml
model:
  type: device
  format: gltf
  mesh: <mesh_name>
  mesh_tf: [0, 0, 0, 0, 0, 0]
  encrypted: true
  path: ""
```

- Registry field rules:
  - `mesh` is the stable OSS namespace segment, not a local path, filename, or
    complete URL.
  - Keep `path: ""` only for the first package upload used to create the Device
    Square template. Replace it with the exact URL returned by
    `upload_device_model`, then re-upload the package.
  - A final standalone path ends in its real entry filename, for example
    `model/centrifuge/1.0.0/centrifuge.stl` or
    `model/centrifuge/1.0.0/centrifuge.glb`.
  - `mesh_tf` is transform metadata, not an OSS location. Do not rely on it to
    correct a standalone GLB/STL axis mismatch in the current Web renderer;
    export the asset with the expected axes and verify it in the frontend.

- Frontend coordinate guardrails:
  - Author GLB in any convenient DCC convention, but export a standards-compliant
    glTF/GLB whose delivered scene is Y-up. A normal Blender GLB export performs
    the authoring Z-up to glTF Y-up conversion, so it appears upright in the
    Three.js Y-up scene.
  - XACRO/URDF stays ROS Z-up; the frontend explicitly applies its conversion.
  - Standalone STL currently has a split contract: upload footprint calculation
    treats STL as Z-up, while the renderer does not apply the XACRO/URDF Z-up
    rotation. Always preview a standalone STL. If orientation is wrong, correct
    the exported STL or use XACRO/URDF to supply an explicit mesh origin; do not
    silently relabel the STL as another format.
  - GLB is preferred over `.gltf` only when a single self-contained glTF artifact
    is desirable. It is not categorically preferred over STL; choose based on
    axis behavior and whether materials, textures, hierarchy, or animation matter.

- Sequence:
  - Upload package once so Device Square templates exist.
  - Resolve each `template_uuid` from `/lab/square/list` or equivalent template search.
  - Upload each model from its real local source without copying it into Uni-Lab-OS:

    ```python
    from pathlib import Path
    from unilabos.app.model_upload import upload_device_model

    # Bundle: relative paths below model_source are preserved in OSS.
    path = upload_device_model(
        client,
        template_uuid,
        mesh_name="hamilton_star",
        model_type="device",
        version="1.0.0",
        model_source=Path("../device_models_zup/hamilton_star"),
        entry_file="modal.xacro",
    )

    # Standalone file: the file itself is the published entry.
    path = upload_device_model(
        client,
        template_uuid,
        mesh_name="centrifuge",
        model_type="device",
        version="1.0.0",
        model_source=Path("../device_models_zup/centrifuge/centrifuge.stl"),
    )

    # Standalone GLB: publishes a .glb entry whose registry format is "gltf".
    path = upload_device_model(
        client,
        template_uuid,
        mesh_name="centrifuge",
        model_type="device",
        version="1.0.0",
        model_source=Path("../device_models/centrifuge/centrifuge.glb"),
    )

    # External-dependency .gltf: upload its directory and name the entry.
    path = upload_device_model(
        client,
        template_uuid,
        mesh_name="centrifuge",
        model_type="device",
        version="1.0.0",
        model_source=Path("../device_models/centrifuge"),
        entry_file="centrifuge.gltf",
    )
    ```

  - `entry_file` is relative to a directory source. It may be omitted when the helper can uniquely infer `modal.xacro`, `macro_device.xacro`, one URDF/XACRO entry, or one standalone model file. Pass it explicitly for ambiguous directories.
  - Let the helper handle encryption: XACRO/URDF stays plaintext; mesh entry
    files including STL, GLB, and GLTF are XOR-encrypted; publish receives the
    derived `encrypted` flag.
  - The helper matches presigned URLs by relative filename, publishes only after every file uploads, and best-effort updates `model.format` plus the uploaded file inventory.
  - The backend owns the `model/<mesh>/<version>/` prefix. The uploader owns `version`, dependency-relative names, and `entry_file`; the frontend loads the exact published `model.path` and resolves bundle dependencies relative to it.
  - Patch the returned `model.path` back into the source registry:
    - YAML package: patch `registry.yaml`.
    - AST package: patch the `@device(model=...)` or `id_meta[id]["model"]` metadata.
  - Re-upload the package so `source_registry` contains final model paths.

## Real Vs Virtual Devices

- Real device entries should construct real drivers/backends and should not silently fall back to simulation.
- Virtual devices should be separate entries/packages with virtual runtime metadata and virtual backends.
- Model metadata belongs to the device entry, not the backend.
- Real/virtual pair metadata does not automatically carry models; each renderable real or virtual entry needs its own `model` block.

## Final Checks

- Existing `pyproject.toml` preserved unless user asked to change it.
- No duplicate device IDs across YAML and AST sources.
- `inspect_package` reports expected resource count.
- Real devices have no accidental virtual/mock/chatterbox/simulator references.
- Actions are present beyond `setup`/`stop`.
- Every model source exists, and every directory with multiple possible entries passes an explicit `entry_file`.
- Every final registry `format` matches the entry contract: `.stl` uses `stl`,
  while `.glb` and `.gltf` use `gltf`.
- Every GLB is previewed upright; every standalone STL is previewed because its
  current footprint and render axis handling differ.
- Model paths are nonblank when models are required.
- `model.encrypted: true` appears in registry and generated resources when encrypted helper upload was used.
- Final upload returns success, and saved logs/responses do not contain AK/SK.
