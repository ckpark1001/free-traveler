#!/usr/bin/env python3
"""Build the Task DAG and Wave plan for the Traveler project.

Inputs
  - TASKS/TASK_MANIFEST.csv
  - TASKS/details/TASK-*.md  (falls back to TASKS/TASK-*.md when the details/ directory does not exist)
  - design-reference/SCREEN_ROUTE_CONTRACT.json

Outputs
  - TASKS/TASK_DAG.md
  - TASKS/WAVE_PLAN.md
  - TASKS/WAVE_STATE.json
  - TASKS/TASK_MANIFEST.csv  (a `wave_id` column is added/updated)

Rules
  1. Dependencies are read from the manifest and checked for cycles.
  2. A prerequisite placed in a later wave than its dependent is a failure.
  3. Waves hold 4..7 tasks (a group that has fewer than 4 tasks in total keeps what it has).
  4. A Page Owner is the last integration task of its screen.
  5. Tasks whose Expected Files overlap are never placed in the same wave.
  6. Inside a wave, tasks run one at a time, in dependency order with Task ID as the tie-break.

Wave IDs are generated here (W01, W02, ...). WAVE_PLAN.md / WAVE_STATE.json are the source of truth afterwards.
This script never creates branches, PRs or merges, and never retries or auto-fixes anything.

Usage:  python scripts/build_waves.py [--force]
  --force  overwrite WAVE_STATE.json even when it records progress (any wave not `pending`).

Exit code 0 on success, 1 on any validation error.
"""
from __future__ import annotations

import csv
import heapq
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "TASKS"
MANIFEST = TASKS_DIR / "TASK_MANIFEST.csv"
DETAILS_DIR = TASKS_DIR / "details" if (TASKS_DIR / "details").is_dir() else TASKS_DIR
CONTRACT = ROOT / "design-reference" / "SCREEN_ROUTE_CONTRACT.json"
DAG_MD = TASKS_DIR / "TASK_DAG.md"
PLAN_MD = TASKS_DIR / "WAVE_PLAN.md"
STATE_JSON = TASKS_DIR / "WAVE_STATE.json"

MAX_WAVE = 7
MIN_WAVE = 4
STATE_SCHEMA = "traveler-wave-state-v1"

GROUPS = {
    1: "Scaffold·문서·Harness 확인",
    2: "공통 UI·정적 데이터·Layout",
    3: "Supabase Auth·6개 Table·기본 RLS",
    4: "SCR-001 메인",
    5: "SCR-002 대표 소개",
    6: "SCR-003 여행 입력·외부 이동·동행글 입력",
    7: "SCR-004 동행 목록·상세·신청",
    8: "SCR-005 계정·내 활동·관리자",
    9: "Unit·Playwright·접근성·CI",
    10: "Vercel Preview·Release 확인",
}
SCREEN_GROUP = {"SCR-001": 4, "SCR-002": 5, "SCR-003": 6, "SCR-004": 7, "SCR-005": 8}
# Auth is a prerequisite of SCR-003/004 components, so it belongs to the Supabase Auth group.
GROUP_OVERRIDE = {"CMP-SCR005-AUTH": 3}

errors: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


# --------------------------------------------------------------------------- input
def read_manifest() -> tuple[list[dict], list[str]]:
    if not MANIFEST.exists():
        sys.exit(f"[build_waves] {MANIFEST} not found - run scripts/audit_tasks.py first")
    with MANIFEST.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    return rows, fields


def split_ids(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def expected_files(task_id: str) -> set[str]:
    path = DETAILS_DIR / f"TASK-{task_id}.md"
    if not path.exists():
        fail(f"{task_id}: 상세 파일 없음 ({path.relative_to(ROOT)})")
        return set()
    text = path.read_text(encoding="utf-8")
    m = re.search(r"## Expected Files\s*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        fail(f"{task_id}: '## Expected Files' 절 없음")
        return set()
    body = m.group(1).split("**")[0]
    files = set()
    for part in re.split(r"[;\n]", body):
        part = part.split("(")[0].strip().strip("`- ").strip()
        if part and ("/" in part or "." in part):
            files.add(part)
    return files


def check_contract(rows: list[dict]) -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    screens = data.get("screens", [])
    entries = {}
    for s in screens:
        sid = s.get("screen_id") or s.get("id")
        entries[sid] = s.get("page_entry")
    owners = {r["screen"]: r for r in rows if r["category"] == "PAGE_OWNER"}
    for sid, entry in entries.items():
        owner = owners.get(sid)
        if not owner:
            fail(f"{sid}: Page Owner Task 없음")
        elif entry and owner["page_entry"] != entry:
            fail(f"{owner['task_id']}: Page Entry 불일치 (manifest={owner['page_entry']}, contract={entry})")
    if len(entries) != 5:
        fail(f"Screen Contract의 Screen 수가 5가 아님: {len(entries)}")


# --------------------------------------------------------------------------- graph
def find_cycle_nodes(deps: dict[str, list[str]]) -> set[str]:
    indeg = {t: 0 for t in deps}
    users = defaultdict(list)
    for t, ds in deps.items():
        for d in ds:
            indeg[t] += 1
            users[d].append(t)
    queue = [t for t, n in indeg.items() if n == 0]
    seen = 0
    while queue:
        t = queue.pop()
        seen += 1
        for u in users[t]:
            indeg[u] -= 1
            if indeg[u] == 0:
                queue.append(u)
    return {t for t, n in indeg.items() if n > 0}


def base_group(row: dict) -> int | None:
    tid, cat = row["task_id"], row["category"]
    if tid in GROUP_OVERRIDE:
        return GROUP_OVERRIDE[tid]
    if cat in ("SHARED", "DATA"):
        return 2
    if cat in ("DB", "API"):
        return 3
    if cat in ("PAGE_OWNER", "COMPONENT"):
        screen = row["screen"] if row["screen"] in SCREEN_GROUP else None
        if screen is None:
            m = re.search(r"SCR00(\d)", tid)
            screen = f"SCR-00{m.group(1)}" if m else None
        return SCREEN_GROUP.get(screen)
    if cat in ("UNIT_TEST", "INTEGRATION_TEST", "E2E_TEST", "CI", "MANUAL_CHECK"):
        return 9
    if cat == "RELEASE_CHECK":
        return 10
    return None


def order_group(ids: list[str], deps: dict[str, list[str]], is_page: dict[str, bool]) -> list[str]:
    """Topological order inside one group; Task ID is the tie-break and Page Owners go last."""
    members = set(ids)
    indeg = {t: sum(1 for d in deps[t] if d in members) for t in ids}
    users = defaultdict(list)
    for t in ids:
        for d in deps[t]:
            if d in members:
                users[d].append(t)
    heap = [(is_page[t], t) for t in ids if indeg[t] == 0]
    heapq.heapify(heap)
    out = []
    while heap:
        _, t = heapq.heappop(heap)
        out.append(t)
        for u in users[t]:
            indeg[u] -= 1
            if indeg[u] == 0:
                heapq.heappush(heap, (is_page[u], u))
    return out


def chunk(ordered: list[str], files: dict[str, set[str]]) -> list[list[str]]:
    """Greedy split into waves of <= MAX_WAVE tasks with no Expected Files overlap inside a wave."""
    waves: list[list[str]] = []
    cur: list[str] = []
    cur_files: set[str] = set()
    for t in ordered:
        if cur and (len(cur) >= MAX_WAVE or files[t] & cur_files):
            waves.append(cur)
            cur, cur_files = [], set()
        cur.append(t)
        cur_files |= files[t]
    if cur:
        waves.append(cur)
    # a short tail wave borrows from the end of the previous wave (order is preserved)
    while len(waves) > 1 and len(waves[-1]) < MIN_WAVE and len(waves[-2]) > MIN_WAVE:
        moved = waves[-2][-1]
        if files[moved] & set().union(*(files[x] for x in waves[-1])):
            break
        waves[-1].insert(0, waves[-2].pop())
    return waves


# --------------------------------------------------------------------------- main
def main() -> int:
    force = "--force" in sys.argv[1:]
    rows, fields = read_manifest()
    by_id = {r["task_id"]: r for r in rows}
    if len(by_id) != len(rows):
        fail("manifest에 중복 Task ID가 있음")
    deps = {r["task_id"]: split_ids(r["depends_on"]) for r in rows}
    for t, ds in deps.items():
        for d in ds:
            if d not in by_id:
                fail(f"{t}: 존재하지 않는 Depends On '{d}'")
    check_contract(rows)

    cyc = find_cycle_nodes({t: [d for d in ds if d in by_id] for t, ds in deps.items()})
    if cyc:
        fail(f"순환 의존성 {len(cyc)}개 Task: {sorted(cyc)}")
    if errors:
        return report_errors(len(cyc))

    files = {t: expected_files(t) for t in by_id}
    is_page = {t: by_id[t]["category"] == "PAGE_OWNER" for t in by_id}

    group = {}
    for r in rows:
        g = base_group(r)
        if g is None:
            fail(f"{r['task_id']}: 그룹을 정할 수 없음 (category={r['category']}, screen={r['screen']})")
        else:
            group[r["task_id"]] = g
    if errors:
        return report_errors(0)

    # a prerequisite may never sit in a later group than its dependent: pull it earlier
    changed = True
    while changed:
        changed = False
        for t, ds in deps.items():
            for d in ds:
                if group[d] > group[t]:
                    notes.append(f"{d}: 그룹 {group[d]} -> {group[t]} ({t}의 선행 Task라 앞 그룹으로 이동)")
                    group[d] = group[t]
                    changed = True

    waves: list[dict] = []
    for g in sorted(set(group.values())):
        ids = [t for t in by_id if group[t] == g]
        ordered = order_group(ids, deps, is_page)
        if len(ordered) != len(ids):
            fail(f"그룹 {g}: 위상 정렬 실패")
            continue
        parts = chunk(ordered, files)
        for i, part in enumerate(parts, 1):
            title = GROUPS[g] + (f" ({i}/{len(parts)})" if len(parts) > 1 else "")
            waves.append({"group": g, "title": title, "task_ids": part})
    for n, w in enumerate(waves, 1):
        w["wave_id"] = f"W{n:02d}"
    skipped = [GROUPS[g] for g in GROUPS if g not in set(group.values())]

    wave_of = {t: w["wave_id"] for w in waves for t in w["task_ids"]}
    pos = {t: (w["wave_id"], i) for w in waves for i, t in enumerate(w["task_ids"])}

    # rule 2: prerequisites never come later
    for t, ds in deps.items():
        for d in ds:
            if pos[d] >= pos[t]:
                fail(f"선행 Task가 뒤에 배치됨: {d} ({wave_of[d]}) -> {t} ({wave_of[t]})")
    # rule 4: Page Owner is the last integration task of its screen
    for r in rows:
        if r["category"] != "PAGE_OWNER":
            continue
        for o in rows:
            if o["screen"] == r["screen"] and o["task_id"] != r["task_id"] and o["category"] == "COMPONENT":
                if pos[o["task_id"]] >= pos[r["task_id"]]:
                    fail(f"{r['task_id']}가 같은 화면의 {o['task_id']}보다 먼저 배치됨")
    # rule 5: no Expected Files overlap inside a wave
    for w in waves:
        seen: dict[str, str] = {}
        for t in w["task_ids"]:
            for f in files[t]:
                if f in seen:
                    fail(f"{w['wave_id']}: Expected Files 충돌 {f} ({seen[f]}, {t})")
                seen[f] = t
    if errors:
        return report_errors(0)

    for w in waves:
        pages = [t for t in w["task_ids"] if is_page[t]]
        if pages:
            w["checkpoint"] = ", ".join(f"{by_id[p]['screen']} {by_id[p]['route']}" for p in pages) + " Preview 확인"
        elif w is waves[-1]:
            w["checkpoint"] = "FINAL Preview 확인"
        else:
            w["checkpoint"] = "없음"
        w["checkpoint_required"] = w["checkpoint"] != "없음"

    existing_progress = False
    if STATE_JSON.exists() and not force:
        try:
            old = json.loads(STATE_JSON.read_text(encoding="utf-8"))
            existing_progress = any(w.get("status") != "pending" for w in old.get("waves", []))
        except (OSError, ValueError):
            existing_progress = False
    if existing_progress:
        print("[build_waves] WAVE_STATE.json에 진행 기록이 있어 덮어쓰지 않습니다. 의도한 경우 --force를 사용하세요.")
        return 1

    write_dag(rows, deps, wave_of)
    write_plan(waves, by_id, skipped)
    write_state(waves)
    write_manifest(rows, fields, wave_of)
    print_summary(waves, by_id, cyc, skipped)
    return 0


def report_errors(cycle_count: int) -> int:
    print("[build_waves] FAIL")
    for e in errors:
        print(f"  - {e}")
    print(f"[build_waves] 순환 의존성 Task 수: {cycle_count}")
    return 1


# --------------------------------------------------------------------------- writers
def write_dag(rows: list[dict], deps: dict[str, list[str]], wave_of: dict[str, str]) -> None:
    users = defaultdict(list)
    for t, ds in deps.items():
        for d in ds:
            users[d].append(t)
    lines = [
        "# Task DAG",
        "",
        "`scripts/build_waves.py`가 `TASKS/TASK_MANIFEST.csv`의 Depends On으로 생성한 파일이다. 직접 수정하지 않는다.",
        "",
        f"- Task {len(rows)}개, 의존 간선 {sum(len(v) for v in deps.values())}개, 순환 의존성 0",
        "",
        "| Seq | Task ID | Wave | Depends On | Required By |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        t = r["task_id"]
        d = ", ".join(f"`{x}`" for x in deps[t]) or "-"
        u = ", ".join(f"`{x}`" for x in sorted(users[t])) or "-"
        lines.append(f"| {r['seq']} | `{t}` | {wave_of[t]} | {d} | {u} |")
    DAG_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_plan(waves: list[dict], by_id: dict[str, dict], skipped: list[str]) -> None:
    lines = [
        "# Wave Plan",
        "",
        "`scripts/build_waves.py`가 생성했다. Wave ID는 이 파일이 정본이며 직접 수정하지 않는다(수정이 필요하면 스크립트를 다시 실행한다).",
        "한 Wave 안에서는 아래 순서대로 Task를 한 번에 하나씩만 실행한다.",
        "",
        "| Wave | 제목 | Task (실행 순서) | Preview Checkpoint |",
        "|---|---|---|---|",
    ]
    for w in waves:
        tasks = " → ".join(f"`{t}`" for t in w["task_ids"])
        lines.append(f"| {w['wave_id']} | {w['title']} | {tasks} | {w['checkpoint']} |")
    if skipped:
        lines += ["", "Task가 없어 Wave를 만들지 않은 그룹: " + ", ".join(skipped)]
    PLAN_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(waves: list[dict]) -> None:
    state = {
        "schema_version": STATE_SCHEMA,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "active_wave": None,
        "waves": [
            {
                "wave_id": w["wave_id"],
                "title": w["title"],
                "task_ids": w["task_ids"],
                "status": "pending",
                "checkpoint_required": w["checkpoint_required"],
                "checkpoint_result": None,
            }
            for w in waves
        ],
    }
    STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_manifest(rows: list[dict], fields: list[str], wave_of: dict[str, str]) -> None:
    cols = [c for c in fields if c != "wave_id"] + ["wave_id"]
    with MANIFEST.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            r["wave_id"] = wave_of[r["task_id"]]
            writer.writerow(r)


def print_summary(waves: list[dict], by_id: dict[str, dict], cyc: set[str], skipped: list[str]) -> None:
    print("[build_waves] OK")
    print(f"[build_waves] 순환 의존성 수: {len(cyc)}")
    print(f"[build_waves] Task {len(by_id)}개 / Wave {len(waves)}개")
    for w in waves:
        flag = "" if MIN_WAVE <= len(w["task_ids"]) <= MAX_WAVE else "  (4~7 범위 밖)"
        print(f"  {w['wave_id']} {len(w['task_ids'])}개  {w['title']}{flag}")
    print("[build_waves] Page Owner 위치")
    for t, r in by_id.items():
        if r["category"] == "PAGE_OWNER":
            w = next(x for x in waves if t in x["task_ids"])
            print(f"  {t}: {w['wave_id']} ({w['task_ids'].index(t) + 1}/{len(w['task_ids'])}번째)")
    for n in notes:
        print(f"[build_waves] note: {n}")
    if skipped:
        print("[build_waves] Task 없는 그룹(Wave 미생성): " + ", ".join(skipped))
    print("[build_waves] wrote TASK_DAG.md, WAVE_PLAN.md, WAVE_STATE.json, TASK_MANIFEST.csv(wave_id)")


if __name__ == "__main__":
    sys.exit(main())
