#!/usr/bin/env python3
"""audit_tasks.py -- Traveler Task Pipeline final auditor.

Reads:
  - TASKS/00_TASK_LIST.md      (Task List table + Requirement Coverage table)
  - TASKS/TASK-*.md            (per-task detail files)
  - app/docs/PROJECT_SCOPE.md  (authoritative REQ-FUNC/REQ-NF IMPLEMENT/EXCLUDED classification)
  - design-reference/SCREEN_ROUTE_CONTRACT.json (authoritative Screen/Route/Page Entry)

Writes:
  - TASKS/TASK_MANIFEST.csv     (flat machine-readable manifest of every task)
  - TASKS/TASK_AUDIT_REPORT.md  (human-readable pass/fail report)

Checks (numbered to match the audit spec this script implements):

  1  Task List 구현 ID와 상세 Task 파일 1:1
  2  중복 Task ID 0
  3  Depends On 누락 0 (참조 무결성)
  4  Dependency Cycle 0
  5  Screen 5개 모두 Page Owner 정확히 1개
  6  Route/Page Entry/Expected Files 일치 (SCREEN_ROUTE_CONTRACT.json 대조)
  7  Component-only Screen 0 (Component만 있고 Page Owner가 없는 Screen 없음)
  8  SCR-001 Starter 제거 AC 존재
  9  SCR-003 세 탭(항공/숙소/동행) 조립 AC 존재
  10 SCR-005 역할별(Guest/Member/Admin) 상태 조립 AC 존재
  11 DB Schema/RLS/Access/Seed Task 존재
  12 DB Table 개수가 6개 기본 테이블을 크게 넘지 않음 (기준: 6개, 허용 오차 +2 = 최대 8개)
  13 외부 입력(항공/숙소) 비저장 AC 존재
  14 Auth/성인확인/기본 RLS AC 존재
  15 Playwright Chromium Smoke Task 존재
  16 AWS/EC2/자동 Merge 구현 Task 0
  17 REQ-FUNC 80개 + REQ-NF 34개 전부가 Task 또는 EXCLUDED 표에 존재
  18 EXCLUDED 요구사항에 대한 상세 구현 파일이 생성되지 않음

Exit code 0 + prints "AUDIT_PASS" and the check count when every check
passes. Exit code 1 (no "AUDIT_PASS" line) when any check fails.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = ROOT / "TASKS"
TASK_LIST_PATH = TASKS_DIR / "00_TASK_LIST.md"
PROJECT_SCOPE_PATH = ROOT / "app/docs/PROJECT_SCOPE.md"
SCREEN_ROUTE_CONTRACT_PATH = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"
MANIFEST_CSV = TASKS_DIR / "TASK_MANIFEST.csv"
REPORT_MD = TASKS_DIR / "TASK_AUDIT_REPORT.md"

EXPECTED_SCREEN_IDS = [f"SCR-00{n}" for n in range(1, 6)]
EXPECTED_FUNC_COUNT = 80
EXPECTED_NF_COUNT = 34
DB_TABLE_BASE = 6
DB_TABLE_TOLERANCE = 2  # "크게 넘지 않음" -> fail only when count > base + tolerance

FORBIDDEN_KEYWORDS = ["EC2", "AWS", "자동 병합", "auto-merge", "automerge", "auto merge"]
FLIGHT_HOTEL_KEYWORDS = ["항공", "숙소", "호텔", "flight", "hotel"]
NON_TRANSMIT_VERBS = ["전달하지 않는다", "저장하지 않는다", "보내지 않는다", "전송하지 않는다", "첨부하지 않는다"]
NON_TRANSMIT_TARGETS = ["서버", "DB", "URL", "로그"]
DB_ROLE_KEYWORDS = {"SCHEMA": "SCHEMA", "RLS": "RLS", "ACCESS": "ACCESS", "SEED": "SEED"}
DB_FORBIDDEN_TABLE_HINTS = ["destination", "country_safety", "representative", "region", "media_asset", "safety"]
TABLES_LINE_RE = re.compile(r"Tables\s*:\s*(.+)")
BACKTICK_RE = re.compile(r"`([^`]+)`")
REQ_ID_RE = re.compile(r"REQ-(?:FUNC|NF)-\d{3}")
NUMBERED_LIST_RE = re.compile(r"\d+\)\s+")
MIN_COUNT_RE = re.compile(r"\d+\s*(개\s*이상|장\s*이상|개국\s*이상|개\b|장\b)")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


# ---------------------------------------------------------------------------
# Parsing: TASKS/00_TASK_LIST.md
# ---------------------------------------------------------------------------

TASK_LIST_COLUMNS = [
    "seq", "task_id", "title", "category", "impl_status", "req_ref",
    "screen", "route", "page_entry", "depends_on_raw", "expected_files",
    "functional_ac", "visual_ac", "security_ac", "verify", "priority",
]


def split_table_row(line: str) -> list[str] | None:
    line = line.strip()
    if not line.startswith("|"):
        return None
    parts = [p.strip() for p in line.split("|")]
    return parts[1:-1]


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def split_csv_cell(cell: str) -> list[str]:
    cell = cell.strip()
    if cell in ("", "-", "–"):
        return []
    return [x.strip().strip("`") for x in cell.split(",") if x.strip()]


def parse_task_list(path: Path, errors: list[str]) -> tuple[list[dict], list[dict]]:
    tasks: list[dict] = []
    disposition: list[dict] = []
    if not path.exists():
        errors.append(f"{rel(path)} does not exist")
        return tasks, disposition

    lines = path.read_text(encoding="utf-8").splitlines()
    i, n = 0, len(lines)
    while i < n:
        cells = split_table_row(lines[i])
        if cells is None:
            i += 1
            continue

        if cells and cells[0] == "Seq":
            i += 1
            if i < n and split_table_row(lines[i]) and is_separator_row(split_table_row(lines[i])):
                i += 1
            while i < n:
                row = split_table_row(lines[i])
                if row is None:
                    break
                if len(row) < 16:
                    errors.append(f"task list row has {len(row)} columns, expected 16: {row[:3]}")
                    i += 1
                    continue
                d = dict(zip(TASK_LIST_COLUMNS, row[:16]))
                d["task_id"] = d["task_id"].strip("`")
                d["page_entry"] = d["page_entry"].strip("`") if d["page_entry"] != "-" else "-"
                d["depends_on"] = split_csv_cell(d["depends_on_raw"])
                d["requirements"] = REQ_ID_RE.findall(d["req_ref"])
                tasks.append(d)
                i += 1
            continue

        if cells and cells[0] == "Requirement" and len(cells) >= 2 and cells[1] in ("Status", "Scope"):
            i += 1
            if i < n and split_table_row(lines[i]) and is_separator_row(split_table_row(lines[i])):
                i += 1
            while i < n:
                row = split_table_row(lines[i])
                if row is None:
                    break
                if len(row) < 3:
                    errors.append(f"coverage row has {len(row)} columns, expected 3: {row}")
                    i += 1
                    continue
                req_cell, scope, task_ids_cell = row[:3]
                m = REQ_ID_RE.search(req_cell)
                if not m:
                    i += 1
                    continue
                disposition.append({
                    "requirement": m.group(0),
                    "scope": scope.strip(),
                    "task_ids": split_csv_cell(task_ids_cell),
                })
                i += 1
            continue

        i += 1

    if not tasks:
        errors.append("no Task List table found (expected a table whose first column header is 'Seq')")
    if not disposition:
        errors.append("no Requirement Coverage table found (expected header starting 'Requirement | Status')")
    return tasks, disposition


def parse_body_sections(text: str) -> dict:
    sections: dict[str, str] = {}
    current = None
    buf: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m:
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = m.group(1).strip().lower()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def parse_detail_files(directory: Path) -> dict[str, dict]:
    details: dict[str, dict] = {}
    if not directory.exists():
        return details
    for path in sorted(directory.glob("TASK-*.md")):
        text = path.read_text(encoding="utf-8")
        sections = parse_body_sections(text)
        task_id = path.stem[len("TASK-"):]
        details[task_id] = {
            "file": path,
            "context": sections.get("context", ""),
            "project_scope": sections.get("project scope", ""),
            "req_ref": sections.get("requirement ref", ""),
            "screen_route_entry": sections.get("screen / route / page entry", ""),
            "design_ref": sections.get("design ref", ""),
            "depends_on": sections.get("depends on", ""),
            "expected_files": sections.get("expected files", ""),
            "functional_ac": sections.get("functional ac", ""),
            "visual_ac": sections.get("visual ac", ""),
            "security_ac": sections.get("security/privacy ac", ""),
            "test_cases": sections.get("test cases", ""),
            "verify": sections.get("verify", ""),
            "dod": sections.get("definition of done", ""),
            "forbidden": sections.get("forbidden", ""),
        }
    return details


def parse_project_scope(path: Path) -> dict[str, str]:
    """{req_id: 'IMPLEMENT'|'EXCLUDED'|other} from app/docs/PROJECT_SCOPE.md."""
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        cells = split_table_row(line)
        if not cells or len(cells) < 3:
            continue
        m = re.match(r"^(REQ-(?:FUNC|NF)-\d{3})\b", cells[0])
        if not m:
            continue
        result[m.group(1)] = cells[2].strip()
    return result


def parse_screen_route_contract(path: Path) -> dict[str, dict]:
    """{screen_id: {route, page_entry}}"""
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    out = {}
    for s in data.get("screens", []):
        sid = s.get("screen_id")
        if sid:
            out[sid] = {"route": s.get("route"), "page_entry": s.get("page_entry")}
    return out


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

class Checks:
    def __init__(self):
        self.results: list[tuple[str, str, bool, list[str]]] = []

    def add(self, num: str, title: str, passed: bool, details: list[str] | None = None):
        self.results.append((num, title, passed, details or []))

    @property
    def all_passed(self) -> bool:
        return all(passed for _, _, passed, _ in self.results)


def task_text(task: dict, details: dict[str, dict], include_forbidden: bool = True) -> str:
    d = details.get(task["task_id"])
    chunks = [task.get("title", ""), task.get("functional_ac", ""), task.get("visual_ac", ""),
              task.get("security_ac", "")]
    if d:
        chunks += [d["context"], d["functional_ac"], d["visual_ac"], d["security_ac"],
                   d["test_cases"], d["dod"], d["expected_files"]]
        if include_forbidden:
            chunks.append(d["forbidden"])
    return "\n".join(chunks)


def find_cycles(tasks: list[dict]) -> list[list[str]]:
    graph = {t["task_id"]: [d for d in t["depends_on"]] for t in tasks}
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {k: WHITE for k in graph}
    cycles: list[list[str]] = []

    def dfs(node: str, stack: list[str]):
        color[node] = GRAY
        stack.append(node)
        for nxt in graph.get(node, []):
            if nxt not in graph:
                continue
            if color.get(nxt) == GRAY:
                idx = stack.index(nxt)
                cycles.append(stack[idx:] + [nxt])
            elif color.get(nxt) == WHITE:
                dfs(nxt, stack)
        stack.pop()
        color[node] = BLACK

    for node in list(graph.keys()):
        if color[node] == WHITE:
            dfs(node, [])
    return cycles


def run_checks(tasks: list[dict], disposition: list[dict], details: dict[str, dict],
                scope_map: dict[str, str], contract_screens: dict[str, dict]) -> Checks:
    c = Checks()
    by_id = {t["task_id"]: t for t in tasks}

    # 1. Task List <-> detail files 1:1
    task_ids = set(by_id.keys())
    detail_ids = set(details.keys())
    missing_details = sorted(task_ids - detail_ids)
    orphan_details = sorted(detail_ids - task_ids)
    msgs = []
    if missing_details:
        msgs.append(f"상세 파일 없는 Task: {missing_details}")
    if orphan_details:
        msgs.append(f"Task List에 없는 상세 파일: {orphan_details}")
    c.add("1", "Task List 구현 ID와 상세 Task 파일 1:1", not msgs, msgs)

    # 2. duplicate Task ID
    seen: dict[str, int] = {}
    for t in tasks:
        seen[t["task_id"]] = seen.get(t["task_id"], 0) + 1
    dupes = sorted(k for k, v in seen.items() if v > 1)
    c.add("2", "중복 Task ID 0", not dupes, [f"중복 ID: {dupes}"] if dupes else [])

    # 3. Depends On 누락 0 (referential integrity)
    msgs = []
    for t in tasks:
        for d in t["depends_on"]:
            if d not in task_ids:
                msgs.append(f"{t['task_id']}: 존재하지 않는 Depends On '{d}'")
    c.add("3", "Depends On 누락 0", not msgs, msgs)

    # 4. Dependency Cycle 0
    cycles = find_cycles(tasks)
    msgs = [f"순환 참조: {' -> '.join(cy)}" for cy in cycles]
    c.add("4", "Dependency Cycle 0", not cycles, msgs)

    # 5. Screen 5개 모두 Page Owner 정확히 1개
    owners = [t for t in tasks if t.get("category") == "PAGE_OWNER"]
    owner_screens = sorted(t.get("screen") for t in owners)
    passed = len(owners) == 5 and owner_screens == EXPECTED_SCREEN_IDS
    msgs = [] if passed else [f"Page Owner {len(owners)}개, screens={owner_screens} "
                               f"(기대값: {EXPECTED_SCREEN_IDS} 각 1개)"]
    c.add("5", "Screen 5개 모두 Page Owner 정확히 1개", passed, msgs)
    owners_by_screen = {t["screen"]: t for t in owners}

    # 6. Route / Page Entry / Expected Files 일치
    msgs = []
    if not contract_screens:
        msgs.append(f"{rel(SCREEN_ROUTE_CONTRACT_PATH)}를 읽을 수 없음")
    for owner in owners:
        canon = contract_screens.get(owner["screen"])
        if canon is None:
            msgs.append(f"{owner['task_id']}: SCREEN_ROUTE_CONTRACT.json에 {owner['screen']} 정의 없음")
            continue
        if owner["route"] != canon["route"]:
            msgs.append(f"{owner['task_id']}: Route 불일치 (Task List='{owner['route']}', 정본='{canon['route']}')")
        if owner["page_entry"] != canon["page_entry"]:
            msgs.append(f"{owner['task_id']}: Page Entry 불일치 (Task List='{owner['page_entry']}', "
                         f"정본='{canon['page_entry']}')")
        d = details.get(owner["task_id"])
        expected_files_text = (owner.get("expected_files", "") + " " + (d["expected_files"] if d else ""))
        if canon["page_entry"] not in expected_files_text:
            msgs.append(f"{owner['task_id']}: Expected Files에 Page Entry '{canon['page_entry']}'가 없음")
    c.add("6", "Route/Page Entry/Expected Files 일치", not msgs, msgs)

    # 7. Component-only Screen 0
    all_screen_values = {t["screen"] for t in tasks if re.fullmatch(r"SCR-\d{3}", t.get("screen", ""))}
    msgs = []
    for scr in sorted(all_screen_values):
        if scr not in contract_screens:
            msgs.append(f"{scr}: SCREEN_ROUTE_CONTRACT.json에 없는 Screen ID가 Task에 사용됨(오타 의심)")
            continue
        if scr not in owners_by_screen:
            msgs.append(f"{scr}: Component/기타 Task는 있지만 Page Owner가 없음")
    c.add("7", "Component-only Screen 0", not msgs, msgs)

    # 8. SCR-001 starter removal AC
    scr1 = owners_by_screen.get("SCR-001")
    msgs = []
    passed = False
    if scr1 is None:
        msgs.append("SCR-001 Page Owner 없음")
    else:
        text = task_text(scr1, details).lower()
        passed = "starter" in text or "스타터" in text
        if not passed:
            msgs.append(f"{scr1['task_id']}: Starter 제거 AC 없음")
    c.add("8", "SCR-001 Starter 제거 AC 존재", passed, msgs)

    # 9. SCR-003 세 탭 조립 AC
    tt = owners_by_screen.get("SCR-003")
    msgs = []
    passed = False
    if tt is None:
        msgs.append("SCR-003 Page Owner 없음")
    else:
        text = task_text(tt, details)
        has_flight = bool(re.search(r"항공|flight", text, re.IGNORECASE))
        has_hotel = bool(re.search(r"숙소|호텔|hotel", text, re.IGNORECASE))
        has_mate = bool(re.search(r"동행|mate", text, re.IGNORECASE))
        passed = has_flight and has_hotel and has_mate
        if not passed:
            msgs.append(f"{tt['task_id']}: 항공/숙소/동행 언급 부족 (flight={has_flight}, hotel={has_hotel}, mate={has_mate})")
    c.add("9", "SCR-003 세 탭 조립 AC 존재", passed, msgs)

    # 10. SCR-005 역할별 상태 조립 AC
    acc = owners_by_screen.get("SCR-005")
    msgs = []
    passed = False
    if acc is None:
        msgs.append("SCR-005 Page Owner 없음")
    else:
        text = task_text(acc, details)
        has_guest = bool(re.search(r"guest|게스트|비로그인", text, re.IGNORECASE))
        has_member = bool(re.search(r"member|회원|프로필|내 활동", text, re.IGNORECASE))
        has_admin = bool(re.search(r"admin|관리자", text, re.IGNORECASE))
        passed = has_guest and has_member and has_admin
        if not passed:
            msgs.append(f"{acc['task_id']}: Guest/Member/Admin 언급 부족 (guest={has_guest}, member={has_member}, admin={has_admin})")
    c.add("10", "SCR-005 역할별 상태 조립 AC 존재", passed, msgs)

    # 11. DB Schema/RLS/Access/Seed Task 존재
    db_tasks = [t for t in tasks if t.get("category") == "DB"]
    msgs = []
    for role, kw in DB_ROLE_KEYWORDS.items():
        if not any(kw in t["task_id"].upper() for t in db_tasks):
            msgs.append(f"DB-{role} 역할의 Task가 없음")
    c.add("11", "DB Schema/RLS/Access/Seed Task 존재", not msgs, msgs)

    # 12. DB table count within tolerance of base 6
    all_tables: list[str] = []
    found_line = False
    for t in db_tasks:
        d = details.get(t["task_id"])
        if not d:
            continue
        for section_text in (d["functional_ac"], d["context"]):
            m = TABLES_LINE_RE.search(section_text)
            if m:
                found_line = True
                all_tables.extend(b.lower() for b in BACKTICK_RE.findall(m.group(1)))
    distinct_tables = sorted(set(all_tables))
    msgs = []
    if not found_line:
        msgs.append("DB Task 어디에도 'Tables: ...' 선언이 없음")
    limit = DB_TABLE_BASE + DB_TABLE_TOLERANCE
    if len(distinct_tables) > limit:
        msgs.append(f"테이블 {len(distinct_tables)}개 선언됨(기준 {DB_TABLE_BASE}개, 허용 한도 {limit}개 초과): {distinct_tables}")
    forbidden_hits = [tbl for tbl in distinct_tables if any(h in tbl for h in DB_FORBIDDEN_TABLE_HINTS)]
    if forbidden_hits:
        msgs.append(f"정적 데이터 도메인과 겹치는 테이블명: {forbidden_hits}")
    c.add("12", f"DB Table 개수가 기본 {DB_TABLE_BASE}개를 크게 넘지 않음(선언 {len(distinct_tables)}개, 한도 {limit}개)",
          not msgs, msgs)

    # 13. flight/hotel non-transmission AC
    msgs = []
    for t in tasks:
        haystack = (t["task_id"] + " " + t.get("title", "")).lower()
        if not any(kw.lower() in haystack for kw in FLIGHT_HOTEL_KEYWORDS):
            continue
        if t.get("category") not in ("PAGE_OWNER", "COMPONENT", "API"):
            continue
        text = task_text(t, details)
        has_verb = any(v in text for v in NON_TRANSMIT_VERBS)
        has_target = any(tg in text for tg in NON_TRANSMIT_TARGETS)
        if not (has_verb and has_target):
            msgs.append(f"{t['task_id']}: 서버/DB/URL 비저장 문구 없음")
    c.add("13", "외부 입력(항공/숙소) 비저장 AC 존재", not msgs, msgs)

    # 14. Auth/adult-verification/RLS AC
    msgs = []
    auth_tasks = [t for t in tasks if "AUTH" in t["task_id"].upper()]
    if not auth_tasks:
        msgs.append("AUTH 관련 Task가 없음")
    elif not any("성인" in task_text(t, details) for t in auth_tasks):
        msgs.append("AUTH Task 중 '성인 확인'을 언급하는 Task가 없음")
    rls_tasks = [t for t in tasks if "RLS" in t["task_id"].upper()]
    if not rls_tasks:
        msgs.append("RLS 관련 Task가 없음")
    elif not any(re.search(r"RLS|정책", task_text(t, details)) for t in rls_tasks):
        msgs.append("RLS Task 중 RLS/정책을 언급하는 Task가 없음")
    c.add("14", "Auth/성인확인/기본 RLS AC 존재", not msgs, msgs)

    # 15. Playwright Chromium Smoke Task 존재
    e2e_tasks = [t for t in tasks if t.get("category") == "E2E_TEST"]
    msgs = []
    if not e2e_tasks:
        msgs.append("E2E_TEST 카테고리 Task가 없음")
    for t in e2e_tasks:
        text = task_text(t, details)
        text_no_forbidden = task_text(t, details, include_forbidden=False)
        if "chromium" not in text.lower():
            msgs.append(f"{t['task_id']}: Chromium 언급 없음")
        for browser in ("firefox", "webkit", "safari"):
            if browser in text_no_forbidden.lower():
                msgs.append(f"{t['task_id']}: Forbidden 절 밖에서 '{browser}' 언급됨")
        if not (re.search(r"SM-\d{2}", text) or "smoke" in text.lower()):
            msgs.append(f"{t['task_id']}: Smoke 시나리오(SM-xx) 또는 'smoke' 언급 없음")
    c.add("15", f"Playwright Chromium Smoke Task 존재({len(e2e_tasks)}개)", not msgs, msgs)

    # 16. AWS/EC2/auto-merge 0 (Forbidden 절에서 이 키워드를 금지 대상으로 언급하는 것은
    # 정당한 authoring이므로 제외하고, 그 밖의 절에서 실제로 구현/사용하려는 언급만 검사한다)
    msgs = []
    for t in tasks:
        text = task_text(t, details, include_forbidden=False)
        hits = [kw for kw in FORBIDDEN_KEYWORDS if kw.lower() in text.lower()]
        if hits:
            msgs.append(f"{t['task_id']}: 금지 키워드 발견: {hits}")
    c.add("16", "AWS/EC2/자동 Merge 구현 Task 0", not msgs, msgs)

    # 17. REQ-FUNC 80 + REQ-NF 34 all present in Task-or-EXCLUDED table
    disp_ids = {row["requirement"] for row in disposition}
    scope_func = {k for k in scope_map if "-FUNC-" in k}
    scope_nf = {k for k in scope_map if "-NF-" in k}
    missing_func = sorted(scope_func - disp_ids)
    missing_nf = sorted(scope_nf - disp_ids)
    unknown = sorted(disp_ids - set(scope_map.keys()))
    bad_scope = sorted(r["requirement"] for r in disposition if r["scope"] not in ("IMPLEMENT", "EXCLUDED"))
    msgs = []
    if len(scope_func) != EXPECTED_FUNC_COUNT:
        msgs.append(f"PROJECT_SCOPE.md에서 REQ-FUNC {len(scope_func)}개 발견(기대 {EXPECTED_FUNC_COUNT}개)")
    if len(scope_nf) != EXPECTED_NF_COUNT:
        msgs.append(f"PROJECT_SCOPE.md에서 REQ-NF {len(scope_nf)}개 발견(기대 {EXPECTED_NF_COUNT}개)")
    if missing_func:
        msgs.append(f"Coverage 표에 없는 REQ-FUNC {len(missing_func)}개: {missing_func[:10]}{' ...' if len(missing_func) > 10 else ''}")
    if missing_nf:
        msgs.append(f"Coverage 표에 없는 REQ-NF {len(missing_nf)}개: {missing_nf}")
    if unknown:
        msgs.append(f"PROJECT_SCOPE.md에 없는 Requirement이 Coverage 표에 있음: {unknown}")
    if bad_scope:
        msgs.append(f"Status가 IMPLEMENT/EXCLUDED가 아닌 행: {bad_scope}")
    c.add("17", f"REQ-FUNC {EXPECTED_FUNC_COUNT}개 + REQ-NF {EXPECTED_NF_COUNT}개 전부 Task/EXCLUDED 표에 존재",
          not msgs, msgs)

    # 18. EXCLUDED requirements have no detail implementation file
    excluded_reqs = {k for k, v in scope_map.items() if v == "EXCLUDED"}
    msgs = []
    for row in disposition:
        if row["scope"] == "EXCLUDED" and row["task_ids"]:
            msgs.append(f"{row['requirement']}은 EXCLUDED인데 Task ID가 연결됨: {row['task_ids']}")
    for t in tasks:
        leaked = [r for r in t["requirements"] if r in excluded_reqs]
        if leaked:
            msgs.append(f"{t['task_id']}의 Requirement Ref에 EXCLUDED 항목이 포함됨: {leaked}")
    stray_files = [tid for tid in details if REQ_ID_RE.fullmatch(tid) and tid in excluded_reqs]
    if stray_files:
        msgs.append(f"EXCLUDED Requirement 이름으로 생성된 상세 파일 발견: {stray_files}")
    c.add("18", "EXCLUDED 요구사항에 대한 상세 구현 파일 미생성", not msgs, msgs)

    return c


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_manifest(tasks: list[dict], details: dict[str, dict]) -> None:
    # keep the wave_id column that scripts/build_waves.py adds
    wave_ids: dict[str, str] = {}
    if MANIFEST_CSV.exists():
        with MANIFEST_CSV.open(encoding="utf-8-sig", newline="") as f:
            wave_ids = {r["task_id"]: r.get("wave_id", "") for r in csv.DictReader(f)}
    with MANIFEST_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        header = ["seq", "task_id", "category", "screen", "route", "page_entry",
                  "depends_on", "requirements", "priority", "detail_file_exists", "verify"]
        keep_waves = any(wave_ids.values())
        writer.writerow(header + (["wave_id"] if keep_waves else []))
        for t in tasks:
            row = [
                t["seq"], t["task_id"], t["category"], t["screen"], t["route"], t["page_entry"],
                "; ".join(t["depends_on"]), "; ".join(t["requirements"]), t["priority"],
                "Y" if t["task_id"] in details else "N", t["verify"],
            ]
            writer.writerow(row + ([wave_ids.get(t["task_id"], "")] if keep_waves else []))


def write_report(checks: Checks, tasks: list[dict], disposition: list[dict], parse_errors: list[str]) -> None:
    lines = ["# Traveler Task Pipeline -- Final Audit Report", ""]
    lines.append(f"- Task List: `{rel(TASK_LIST_PATH)}`")
    lines.append(f"- Tasks parsed: {len(tasks)}")
    lines.append(f"- Requirement coverage rows parsed: {len(disposition)}")
    lines.append(f"- Overall: {'AUDIT_PASS' if (not parse_errors and checks.all_passed) else 'AUDIT_FAIL'}")
    lines.append("")

    if parse_errors:
        lines.append("## Parse errors (blocking)")
        for e in parse_errors:
            lines.append(f"- {e}")
        lines.append("")

    lines.append("## Checks")
    lines.append("")
    lines.append("| # | Rule | Result |")
    lines.append("|---|---|---|")
    for num, title, passed, _ in checks.results:
        lines.append(f"| {num} | {title} | {'PASS' if passed else 'FAIL'} |")
    lines.append("")

    failing = [r for r in checks.results if not r[2]]
    if failing:
        lines.append("## Failure details")
        for num, title, _, msgs in failing:
            lines.append(f"### {num}. {title}")
            for m in msgs:
                lines.append(f"- {m}")
            lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parse_errors: list[str] = []

    if not TASK_LIST_PATH.exists():
        print(f"[audit_tasks] {rel(TASK_LIST_PATH)} not found.")
        TASKS_DIR.mkdir(parents=True, exist_ok=True)
        REPORT_MD.write_text(
            f"# Traveler Task Pipeline -- Final Audit Report\n\n`{rel(TASK_LIST_PATH)}` not found.\nAUDIT_FAIL\n",
            encoding="utf-8",
        )
        print("AUDIT_FAIL")
        return 1

    tasks, disposition = parse_task_list(TASK_LIST_PATH, parse_errors)
    details = parse_detail_files(TASKS_DIR)
    scope_map = parse_project_scope(PROJECT_SCOPE_PATH)
    contract_screens = parse_screen_route_contract(SCREEN_ROUTE_CONTRACT_PATH)

    if not scope_map:
        parse_errors.append(f"{rel(PROJECT_SCOPE_PATH)}에서 REQ 분류를 읽지 못함")
    if not contract_screens:
        parse_errors.append(f"{rel(SCREEN_ROUTE_CONTRACT_PATH)}에서 Screen 정의를 읽지 못함")

    if parse_errors:
        checks = Checks()
        write_manifest(tasks, details)
        write_report(checks, tasks, disposition, parse_errors)
        print("[audit_tasks] parse errors:")
        for e in parse_errors:
            print(f"  - {e}")
        print("AUDIT_FAIL")
        return 1

    checks = run_checks(tasks, disposition, details, scope_map, contract_screens)
    write_manifest(tasks, details)
    write_report(checks, tasks, disposition, parse_errors)

    print(f"[audit_tasks] wrote {rel(MANIFEST_CSV)} and {rel(REPORT_MD)}")
    for num, title, passed, msgs in checks.results:
        status = "PASS" if passed else "FAIL"
        print(f"[audit_tasks] {num:>2}. {status} -- {title}")
        if not passed:
            for m in msgs:
                print(f"       {m}")

    if checks.all_passed:
        print(f"\nAUDIT_PASS ({len(checks.results)} checks)")
        return 0
    else:
        failed = sum(1 for *_, passed, _ in checks.results if not passed)
        print(f"\nAUDIT_FAIL ({failed}/{len(checks.results)} checks failed)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
