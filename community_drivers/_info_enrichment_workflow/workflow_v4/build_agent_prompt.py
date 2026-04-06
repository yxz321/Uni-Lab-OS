#!/usr/bin/env python3
"""Build a production subagent prompt by copying the shared template and appending assigned batch details."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--batch-dir', type=Path, required=True)
    parser.add_argument('--batch-name', required=True)
    parser.add_argument('--devices-file', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--workflow-doc', type=Path, required=True)
    parser.add_argument('--state-file', type=Path, required=True)
    parser.add_argument('--subagent-model', required=True)
    parser.add_argument('--api-model', required=True)
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()

    out = args.out or (args.batch_dir / 'agent_prompt.md')
    template = args.template.read_text(encoding='utf-8').rstrip()
    assigned = f"""
## Assigned Batch

- batch_name: `{args.batch_name}`
- batch_dir: `{args.batch_dir}`
- devices_file: `{args.devices_file}`
- manifest: `{args.manifest}`
- workflow_doc: `{args.workflow_doc}`
- state_file: `{args.state_file}`
- subagent_model: `{args.subagent_model}`
- api_model: `{args.api_model}`
- reasoning_effort: `{args.reasoning_effort}`
- write the report to: `{args.batch_dir / 'report.md'}`
"""
    out.write_text(template + '\n\n' + assigned.lstrip('\n'), encoding='utf-8')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
