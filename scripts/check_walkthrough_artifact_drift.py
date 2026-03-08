#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_FILES = {
    "walkthrough-pass.summary.json": "PASS",
    "walkthrough-pass.summary.md": "PASS",
    "walkthrough-fail.summary.json": "FAIL",
    "walkthrough-fail.summary.md": "FAIL",
    "word-count-range.summary.json": "FAIL",
    "word-count-range.summary.md": "FAIL",
}

EXPECTED_MARKDOWN_TITLES = {
    "walkthrough-pass.summary.md": "## prompt-regression-min summary",
    "walkthrough-fail.summary.md": "## prompt-regression-min summary",
    "word-count-range.summary.md": "## word-count release-note gate",
}

REQUIRED_MARKDOWN_MARKERS = (
    "- Summary schema version: `1`",
    "- Selected dataset IDs:",
    "- Active case IDs:",
)


def _run_regeneration(root: Path, out_dir: Path) -> None:
    env = dict(**__import__("os").environ, PRM_WALKTHROUGH_ARTIFACT_DIR=str(out_dir))
    subprocess.run([str(root / "scripts" / "regenerate_walkthrough_artifacts.sh")], check=True, cwd=root, env=env)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json_schema_version(path: Path) -> int | None:
    if path.suffix != ".json":
        return None
    payload = json.loads(_read(path))
    return payload.get("summary_schema_version")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check committed walkthrough artifacts against regenerated copies")
    parser.add_argument('--root', default=Path(__file__).resolve().parents[1], type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    committed_dir = root / 'examples' / 'artifacts'

    with tempfile.TemporaryDirectory() as tmpdir:
        regen_dir = Path(tmpdir)
        _run_regeneration(root, regen_dir)

        diffs: list[str] = []
        for name, expected_status in EXPECTED_FILES.items():
            committed = committed_dir / name
            regenerated = regen_dir / name
            if not committed.exists() or not regenerated.exists():
                diffs.append(f'missing artifact: {name}')
                continue
            if committed.suffix == '.json':
                committed_payload = json.loads(_read(committed))
                regenerated_payload = json.loads(_read(regenerated))
                if committed_payload.get('status') != expected_status or regenerated_payload.get('status') != expected_status:
                    diffs.append(f'{name}: expected status {expected_status}')
                if committed_payload.get('summary_schema_version') != regenerated_payload.get('summary_schema_version'):
                    diffs.append(
                        f"{name}: summary_schema_version drift committed={committed_payload.get('summary_schema_version')} regenerated={regenerated_payload.get('summary_schema_version')}"
                    )
                if committed_payload != regenerated_payload:
                    diff = '\n'.join(difflib.unified_diff(
                        json.dumps(committed_payload, ensure_ascii=False, indent=2).splitlines(),
                        json.dumps(regenerated_payload, ensure_ascii=False, indent=2).splitlines(),
                        fromfile=f'committed/{name}',
                        tofile=f'regenerated/{name}',
                        lineterm=''
                    ))
                    diffs.append(diff or f'{name}: JSON payload drift detected')
            else:
                committed_text = _read(committed)
                regenerated_text = _read(regenerated)
                for marker in REQUIRED_MARKDOWN_MARKERS:
                    if marker not in committed_text:
                        diffs.append(f'{name}: committed markdown missing marker {marker!r}')
                    if marker not in regenerated_text:
                        diffs.append(f'{name}: regenerated markdown missing marker {marker!r}')
                expected_title = EXPECTED_MARKDOWN_TITLES.get(name)
                if expected_title is not None:
                    if expected_title not in committed_text:
                        diffs.append(f'{name}: committed markdown missing title {expected_title!r}')
                    if expected_title not in regenerated_text:
                        diffs.append(f'{name}: regenerated markdown missing title {expected_title!r}')
                status_marker = f'- Status: **{expected_status}**'
                if status_marker not in committed_text:
                    diffs.append(f'{name}: committed markdown missing status marker {status_marker!r}')
                if status_marker not in regenerated_text:
                    diffs.append(f'{name}: regenerated markdown missing status marker {status_marker!r}')
                if committed_text != regenerated_text:
                    diff = '\n'.join(difflib.unified_diff(
                        committed_text.splitlines(),
                        regenerated_text.splitlines(),
                        fromfile=f'committed/{name}',
                        tofile=f'regenerated/{name}',
                        lineterm=''
                    ))
                    diffs.append(diff or f'{name}: markdown drift detected')

        schema_version = _json_schema_version(committed_dir / 'walkthrough-pass.summary.json')
        if diffs:
            print(f'walkthrough artifact drift: FAIL (summary_schema_version={schema_version})')
            for item in diffs:
                print(item)
            return 1

        print(f'walkthrough artifact drift: PASS (summary_schema_version={schema_version})')
        return 0


if __name__ == '__main__':
    sys.exit(main())
