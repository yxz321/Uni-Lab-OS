#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def sanitize_model_name(model: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '__', model).strip('_') or 'model_run'


def main() -> None:
    parser = argparse.ArgumentParser(description='Build one agent prompt from the shared template.')
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--run-root', type=Path, required=True)
    parser.add_argument('--workflow-doc', type=Path, required=True)
    parser.add_argument('--benchmark-state', type=Path, required=True)
    parser.add_argument('--reasoning-effort', default='medium')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--run-name', help='Optional filesystem-safe run folder name; defaults to sanitized model id')
    args = parser.parse_args()

    run_name = args.run_name or sanitize_model_name(args.model)
    run_dir = args.run_root / run_name
    out = args.out or (args.run_root / f'{run_name}.agent_prompt.md')

    template = args.template.read_text(encoding='utf-8').rstrip()
    assigned = f"""
## Assigned run

- api_model: `{args.model}`
- reasoning_effort: `{args.reasoning_effort}`
- run_dir: `{run_dir}`
- workflow_doc: `{args.workflow_doc}`
- benchmark_state: `{args.benchmark_state}`
- write the report to: `{run_dir / 'report.md'}`
"""
    out.write_text(template + '\n\n' + assigned.lstrip('\n'), encoding='utf-8')
    print(f'wrote {out}')


if __name__ == '__main__':
    main()
