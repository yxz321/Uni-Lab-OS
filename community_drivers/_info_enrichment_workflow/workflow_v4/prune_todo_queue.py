#!/usr/bin/env python3
"""Prune the todo_queue in production_state_v4.json and remove the notes array.

Keeps only the last N entries in todo_queue (default 15).
Removes the notes array entirely — resume state lives in structured fields
(next_device, last_completed_batch, mode, success_streak); historical context
lives in git and WORKFLOW_CHANGELOG.md.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _default_state_file() -> Path:
    return Path(__file__).resolve().parent.parent / 'production_state_v4.json'


def prune(state_file: Path, keep: int) -> None:
    text = state_file.read_text(encoding='utf-8')
    state = json.loads(text)

    todo_queue = state.get('todo_queue', [])
    original_len = len(todo_queue)
    pruned = 0

    if original_len > keep:
        state['todo_queue'] = todo_queue[-keep:]
        pruned = original_len - keep

    notes_removed = 'notes' in state
    state.pop('notes', None)

    state_file.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + '\n',
        encoding='utf-8',
    )

    print(f'todo_queue: kept {len(state["todo_queue"])}/{original_len} entries (pruned {pruned})')
    if notes_removed:
        print('notes: removed')
    else:
        print('notes: not present')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--state-file',
        type=Path,
        default=_default_state_file(),
        help='Path to production_state_v4.json',
    )
    parser.add_argument(
        '--keep',
        type=int,
        default=15,
        help='Number of tail entries to retain in todo_queue (default: 15)',
    )
    args = parser.parse_args()

    if not args.state_file.exists():
        print(f'Error: state file not found: {args.state_file}', file=sys.stderr)
        sys.exit(1)

    prune(args.state_file, args.keep)


if __name__ == '__main__':
    main()
