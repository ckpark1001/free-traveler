#!/usr/bin/env python3
"""validate_inputs.py — Traveler Task Pipeline input gate.

Run BEFORE any task generation (/gen-tasklist calls this first). Validates
that the canonical inputs for the traveler-project-pipeline Skill exist and
are internally consistent:

  - design-reference/SCREEN_ROUTE_CONTRACT.json matches HARNESS_SCHEMA,
    has exactly 5 screens with unique routes/page_entries and a 4-core/
    1-auxiliary split.
  - app/docs/UIUX_TRACEABILITY.md accounts for all 114 requirements
    (REQ-FUNC-001..080, REQ-NF-001..034), each with a recognizable
    Implementation Status.
  - The other canonical documents exist and are non-empty.
  - app/src/app is scanned so downstream steps can write honest
    "Expected Files" sections (new vs. existing) instead of guessing.

No third-party dependencies — standard library only. Writes a machine-
readable report to TASKS/_generated/validate_inputs_report.json and prints
a human-readable summary. Exit code 0 = OK to proceed, 1 = hard failure.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HARNESS_SCHEMA = "traveler-screen-route-v1"
EXPECTED_FRAMEWORK = "nextjs-app-router"
EXPECTED_SCREEN_COUNT = 5
EXPECTED_FUNC_COUNT = 80
EXPECTED_NF_COUNT = 34
EXPECTED_TOTAL = EXPECTED_FUNC_COUNT + EXPECTED_NF_COUNT

ROOT = Path(__file__).resolve().parent.parent

PATHS = {
    "srs_revised": ROOT / "app/docs/06_SRS_UIUX_REVISED.md",
    "project_scope": ROOT / "app/docs/PROJECT_SCOPE.md",
    "traceability": ROOT / "app/docs/UIUX_TRACEABILITY.md",
    "design_canon": ROOT / "design-reference/D-001/DESIGN.md",
    "ui_contract": ROOT / "design-reference/UI_CONTRACT.md",
    "screen_route_contract": ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json",
    "package_json": ROOT / "app/package.json",
}
SRC_APP_DIR = ROOT / "app/src/app"
OUT_DIR = ROOT / "TASKS/_generated"
OUT_JSON = OUT_DIR / "validate_inputs_report.json"

REQ_ID_RE = re.compile(r"^(REQ-(?:FUNC|NF)-\d{3})\b")
REQ_TOKEN_RE = re.compile(r"REQ-(?:FUNC|NF)-\d{3}")
VALID_STATUS_RE = re.compile(r"^(IMPLEMENT \(NOT_STARTED\)|EXCLUDED)$")


def rel(path: Path) -> str:
    """Path relative to ROOT for display; falls back to the absolute path
    if given a path outside ROOT (e.g. in tests)."""
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.data: dict = {}

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    @property
    def ok(self) -> bool:
        return not self.errors


def check_files_exist(report: Report) -> None:
    for key, path in PATHS.items():
        if not path.exists():
            report.error(f"missing required input: {rel(path)}")
        elif path.is_file() and path.stat().st_size == 0:
            report.error(f"input is empty: {rel(path)}")
    if not SRC_APP_DIR.exists():
        report.error(f"missing required directory: {rel(SRC_APP_DIR)}")


def load_json(path: Path, report: Report):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        report.error(f"{rel(path)} is not valid JSON: {exc}")
        return None


def check_screen_route_contract(report: Report) -> dict:
    path = PATHS["screen_route_contract"]
    data = load_json(path, report)
    summary: dict = {"screens": [], "technical_routes": [], "required_navigation_count": 0}
    if data is None:
        return summary

    schema_version = data.get("schema_version")
    if schema_version != HARNESS_SCHEMA:
        report.error(
            f"schema_version mismatch: expected '{HARNESS_SCHEMA}', got {schema_version!r} "
            f"in {rel(path)}"
        )

    framework = data.get("framework")
    if framework != EXPECTED_FRAMEWORK:
        report.warn(f"framework is {framework!r}, expected {EXPECTED_FRAMEWORK!r}")

    screens = data.get("screens")
    if not isinstance(screens, list):
        report.error("screens must be a list")
        screens = []
    if len(screens) != EXPECTED_SCREEN_COUNT:
        report.error(f"expected exactly {EXPECTED_SCREEN_COUNT} screens, found {len(screens)}")

    seen_ids: set[str] = set()
    seen_routes: set[str] = set()
    seen_entries: set[str] = set()
    core_count = 0
    aux_count = 0
    expected_ids = {f"SCR-00{n}" for n in range(1, EXPECTED_SCREEN_COUNT + 1)}

    for i, screen in enumerate(screens):
        if not isinstance(screen, dict):
            report.error(f"screens[{i}] is not an object")
            continue
        required_keys = [
            "screen_id", "route", "page_entry", "classification",
            "page_owner_task_required", "preview_required",
        ]
        for k in required_keys:
            if k not in screen:
                report.error(f"screens[{i}] missing required key '{k}'")

        sid = screen.get("screen_id", f"<index {i}>")
        route = screen.get("route")
        entry = screen.get("page_entry")

        if sid in seen_ids:
            report.error(f"duplicate screen_id: {sid}")
        seen_ids.add(sid)

        if route in seen_routes:
            report.error(f"duplicate route across screens: {route}")
        seen_routes.add(route)

        if entry in seen_entries:
            report.error(f"duplicate page_entry across screens: {entry}")
        seen_entries.add(entry)

        if screen.get("classification") == "core":
            core_count += 1
        elif screen.get("classification") == "auxiliary":
            aux_count += 1
        else:
            report.error(f"{sid}: classification must be 'core' or 'auxiliary', got {screen.get('classification')!r}")

        if screen.get("page_owner_task_required") is not True:
            report.error(f"{sid}: page_owner_task_required must be true")
        if screen.get("preview_required") is not True:
            report.error(f"{sid}: preview_required must be true")

        entry_exists = None
        if isinstance(entry, str):
            resolved = ROOT / "app" / entry
            entry_exists = resolved.exists()
            if not entry.startswith("src/app/") or not entry.endswith(".tsx"):
                report.warn(f"{sid}: page_entry '{entry}' does not look like a Next.js App Router page")

        summary["screens"].append({
            "screen_id": sid,
            "route": route,
            "page_entry": entry,
            "classification": screen.get("classification"),
            "starter_template_forbidden": screen.get("starter_template_forbidden", False),
            "page_entry_exists": entry_exists,
        })

    if seen_ids and seen_ids != expected_ids:
        report.error(f"screen_id set must be exactly {sorted(expected_ids)}, got {sorted(seen_ids)}")

    if core_count != 4 or aux_count != 1:
        report.error(f"expected 4 core + 1 auxiliary screens, got {core_count} core + {aux_count} auxiliary")

    scr1 = next((s for s in summary["screens"] if s["screen_id"] == "SCR-001"), None)
    if scr1 is not None and not scr1["starter_template_forbidden"]:
        report.error("SCR-001 must declare starter_template_forbidden=true")

    technical_routes = data.get("technical_routes", [])
    if not isinstance(technical_routes, list) or not technical_routes:
        report.error("technical_routes must be a non-empty list")
        technical_routes = []
    for i, tr in enumerate(technical_routes):
        if not isinstance(tr, dict) or not {"type", "route", "file"} <= tr.keys():
            report.error(f"technical_routes[{i}] must have type/route/file")
    summary["technical_routes"] = [tr.get("type") for tr in technical_routes if isinstance(tr, dict)]

    nav = data.get("required_navigation", [])
    if not isinstance(nav, list):
        report.error("required_navigation must be a list")
        nav = []
    valid_targets = seen_ids | {"external"}
    for i, edge in enumerate(nav):
        if not isinstance(edge, dict) or not {"from", "to", "trigger"} <= edge.keys():
            report.error(f"required_navigation[{i}] must have from/to/trigger")
            continue
        if edge["from"] not in seen_ids:
            report.error(f"required_navigation[{i}].from '{edge['from']}' is not a known screen_id")
        if edge["to"] not in valid_targets:
            report.error(f"required_navigation[{i}].to '{edge['to']}' is not a known screen_id or 'external'")
    summary["required_navigation_count"] = len(nav)

    return summary


def check_traceability(report: Report) -> dict:
    path = PATHS["traceability"]
    counts = {
        "func_total": 0, "nf_total": 0, "total": 0,
        "implement_count": 0, "excluded_count": 0,
        "missing_status": [], "duplicate_ids": [], "unrecognized_status": [],
    }
    if not path.exists():
        return counts

    text = path.read_text(encoding="utf-8")
    seen: dict[str, int] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        cells = parts[1:-1]
        if not cells:
            continue
        m = REQ_ID_RE.match(cells[0])
        if not m:
            continue
        req_id = m.group(1)
        seen[req_id] = seen.get(req_id, 0) + 1
        status = cells[1] if len(cells) > 1 else ""
        if not status:
            counts["missing_status"].append(req_id)
        elif VALID_STATUS_RE.match(status):
            if status.startswith("IMPLEMENT"):
                counts["implement_count"] += 1
            else:
                counts["excluded_count"] += 1
        else:
            counts["unrecognized_status"].append(f"{req_id}: {status!r}")

    counts["duplicate_ids"] = sorted(k for k, v in seen.items() if v > 1)
    counts["func_total"] = sum(1 for k in seen if "-FUNC-" in k)
    counts["nf_total"] = sum(1 for k in seen if "-NF-" in k)
    counts["total"] = len(seen)

    if counts["func_total"] != EXPECTED_FUNC_COUNT:
        report.error(
            f"UIUX_TRACEABILITY.md has {counts['func_total']} unique REQ-FUNC ids, "
            f"expected {EXPECTED_FUNC_COUNT}"
        )
    if counts["nf_total"] != EXPECTED_NF_COUNT:
        report.error(
            f"UIUX_TRACEABILITY.md has {counts['nf_total']} unique REQ-NF ids, "
            f"expected {EXPECTED_NF_COUNT}"
        )
    if counts["duplicate_ids"]:
        report.error(f"duplicate requirement rows in UIUX_TRACEABILITY.md: {counts['duplicate_ids']}")
    if counts["missing_status"]:
        report.error(f"requirements with no Implementation Status: {counts['missing_status']}")
    if counts["unrecognized_status"]:
        report.error(f"requirements with unrecognized Implementation Status: {counts['unrecognized_status']}")

    return counts


def check_package_json(report: Report) -> None:
    path = PATHS["package_json"]
    data = load_json(path, report)
    if data is None:
        return
    deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    for name in ("next", "react", "typescript", "tailwindcss"):
        if name not in deps:
            report.warn(f"app/package.json missing expected dependency: {name}")


def scan_src_app_tree() -> list[str]:
    if not SRC_APP_DIR.exists():
        return []
    files = sorted(
        p.relative_to(SRC_APP_DIR).as_posix()
        for p in SRC_APP_DIR.rglob("*")
        if p.is_file()
    )
    return files


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    report = Report()
    check_files_exist(report)
    screen_route_contract = check_screen_route_contract(report)
    requirement_counts = check_traceability(report)
    check_package_json(report)
    src_app_tree = scan_src_app_tree()

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ok": report.ok,
        "harness_schema": HARNESS_SCHEMA,
        "errors": report.errors,
        "warnings": report.warnings,
        "screen_route_contract": screen_route_contract,
        "requirement_counts": requirement_counts,
        "src_app_tree": src_app_tree,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[validate_inputs] report written to {rel(OUT_JSON)}")
    print(f"[validate_inputs] HARNESS_SCHEMA={HARNESS_SCHEMA}")
    print(f"[validate_inputs] screens={len(screen_route_contract.get('screens', []))}")
    print(
        "[validate_inputs] requirements: "
        f"func={requirement_counts.get('func_total')} nf={requirement_counts.get('nf_total')} "
        f"total={requirement_counts.get('total')} "
        f"implement={requirement_counts.get('implement_count')} "
        f"excluded={requirement_counts.get('excluded_count')}"
    )
    print(f"[validate_inputs] src/app files found: {len(src_app_tree)}")

    if report.warnings:
        print(f"\n[validate_inputs] {len(report.warnings)} warning(s):")
        for w in report.warnings:
            print(f"  - WARN: {w}")

    if report.errors:
        print(f"\n[validate_inputs] {len(report.errors)} error(s) -- DO NOT PROCEED:")
        for e in report.errors:
            print(f"  - ERROR: {e}")
        return 1

    print("\n[validate_inputs] OK -- safe to proceed with /gen-tasklist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
