#!/usr/bin/env python3
"""check_screen_contract.py -- Traveler Screen/Route Contract gate.

Reads:
  - design-reference/SCREEN_ROUTE_CONTRACT.json (Screen/Route/Page Entry 정본)
  - TASKS/TASK_MANIFEST.csv                     (audit_tasks.py가 생성한 flat 매니페스트)
  - app/src/app/**                              (실제 구현된 Next.js App Router 파일)

Modes (--mode, 기본값 plan):

  plan     Page Owner와 경로 "계획"만 검사한다(1/2/3/5). TASK_MANIFEST.csv와
           SCREEN_ROUTE_CONTRACT.json만 읽고, app/src/app 파일 시스템은 보지
           않는다 -- Wave 구현이 시작되기 전에도 항상 실행 가능하다.
  ci       plan의 4개 검사 + 4번(새 Page 미생성) + 5개 Page 실제 구현 여부 +
           SCR-001 스타터 템플릿 제거 여부를 추가한다("구현된 Page 파일과
           공개 경로를 검사").
  release  ci의 모든 검사 + 6번(Preview Checkpoint 문서 존재 여부)을 추가한다.

Checks (질문에 명시된 번호와 그대로 대응):

  1  고정 화면 5개(SCR-001~005)가 SCREEN_ROUTE_CONTRACT.json에 정확히 존재한다.
  2  각 화면의 Page Owner Task(category=PAGE_OWNER)가 정확히 1개다.
  3  technical_routes(auth/callback, api/*, not-found)를 사용자 화면으로
     세지 않는다 -- counted_as_screen=false 선언 및 Task route 값 검증.
  4  여행지 상세·안전정보 등을 고정 5개 Screen 밖의 새 Page로 만들지 않았다
     (app/src/app을 재귀 스캔해 page.tsx/ts/jsx/js 파일을 대조).
  5  SCR-003 Task가 여행 입력(항공/호텔 Form)과 동행 작성 양쪽을 모두
     포함한다.
  6  release 모드에서 app/docs/preview-checks/SCR-001.md ~ SCR-005.md가
     모두 존재하고 비어 있지 않다.

오류는 파일·화면 ID·수정 힌트를 함께 출력한다. 통과 시 SCREEN_CONTRACT_PASS와
exit code 0, 실패 시 SCREEN_CONTRACT_FAIL과 exit code 1을 낸다.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent

SCREEN_CONTRACT_PATH = ROOT / "design-reference/SCREEN_ROUTE_CONTRACT.json"
TASK_MANIFEST_PATH = ROOT / "TASKS/TASK_MANIFEST.csv"
APP_SRC_APP_DIR = ROOT / "app/src/app"
PREVIEW_CHECKS_DIR = ROOT / "app/docs/preview-checks"

# 질문에서 지정한 고정 화면 5개. SCREEN_ROUTE_CONTRACT.json이 이와 다르면
# 정본이 기대값과 어긋난 것으로 보고 오류를 낸다(정본이 이겨야 하는 값이
# 아니라, 정본이 반드시 이 값을 담고 있어야 하는 불변 계약이다).
FIXED_SCREENS: dict[str, str] = {
    "SCR-001": "/",
    "SCR-002": "/about",
    "SCR-003": "/travel-tools",
    "SCR-004": "/mates",
    "SCR-005": "/account",
}

# 기술 경로로 허용되는 값(사용자 화면으로 세지 않는다).
ALLOWED_TECHNICAL_ROUTE_PREFIXES = ("/auth/callback", "/api/")
ALLOWED_TECHNICAL_ROUTE_EXACT = {"not-found", "*"}

# SHARED-LAYOUT-NAV-FOOTER, SHARED-ERROR-NOTFOUND처럼 특정 화면이 아니라
# 모든 Route에 걸쳐 적용되는 공용 Task가 쓰는 route 칸 sentinel 값.
COMMON_ROUTE_VALUE = "공통(모든 Route)"

PAGE_FILE_NAMES = ("page.tsx", "page.ts", "page.jsx", "page.js")

FORBIDDEN_PAGE_KEYWORDS = ("destination", "safety", "flight", "hotel", "/my/", "/admin/")

STARTER_TEMPLATE_MARKERS = (
    "create-next-app",
    "To get started",
    "Deploy Now",
    "next.svg",
    "vercel.svg",
)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


@dataclass
class Issue:
    file: str
    screen_id: str
    message: str
    hint: str

    def render(self) -> str:
        return (
            f"[check_screen_contract] ERROR file={self.file} screen={self.screen_id}\n"
            f"    문제: {self.message}\n"
            f"    힌트: {self.hint}"
        )


class Report:
    def __init__(self) -> None:
        self.issues: list[Issue] = []

    def error(self, file: str, screen_id: str, message: str, hint: str) -> None:
        self.issues.append(Issue(file=file, screen_id=screen_id, message=message, hint=hint))

    @property
    def ok(self) -> bool:
        return not self.issues


def parse_screen_field(value: Optional[str]) -> list[str]:
    """TASK_MANIFEST.csv의 screen 칸("-", "SCR-003", "SCR-001, SCR-002",
    "ALL(SCR-001~005)")을 화면 ID 리스트로 정규화한다."""
    value = (value or "").strip()
    if not value or value == "-":
        return []
    if value.upper().startswith("ALL"):
        return list(FIXED_SCREENS.keys())
    return [tok.strip() for tok in value.split(",") if tok.strip()]


def load_screen_contract(report: Report) -> Optional[dict]:
    if not SCREEN_CONTRACT_PATH.exists():
        report.error(
            rel(SCREEN_CONTRACT_PATH), "-",
            "SCREEN_ROUTE_CONTRACT.json 파일이 없다.",
            "design-reference/SCREEN_ROUTE_CONTRACT.json을 생성한다(Screen/Route/Page Entry 정본).",
        )
        return None
    try:
        return json.loads(SCREEN_CONTRACT_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.error(
            rel(SCREEN_CONTRACT_PATH), "-",
            f"JSON 파싱 실패: {exc}",
            "SCREEN_ROUTE_CONTRACT.json의 JSON 문법 오류를 수정한다.",
        )
        return None


def load_task_manifest(report: Report) -> Optional[list[dict]]:
    if not TASK_MANIFEST_PATH.exists():
        report.error(
            rel(TASK_MANIFEST_PATH), "-",
            "TASK_MANIFEST.csv 파일이 없다.",
            "scripts/audit_tasks.py(npm run task:contract)를 먼저 실행해 매니페스트를 생성한다.",
        )
        return None
    with TASK_MANIFEST_PATH.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return rows


# ---------------------------------------------------------------------------
# plan 단계 검사 (1/2/3/5) -- TASK_MANIFEST.csv + SCREEN_ROUTE_CONTRACT.json만 사용
# ---------------------------------------------------------------------------

def check_fixed_screens(report: Report, contract: dict) -> None:
    screens = contract.get("screens", [])
    by_id = {s.get("screen_id"): s for s in screens}

    for screen_id, expected_route in FIXED_SCREENS.items():
        s = by_id.get(screen_id)
        if s is None:
            report.error(
                rel(SCREEN_CONTRACT_PATH), screen_id,
                f"고정 화면 {screen_id}이 screens 배열에 없다.",
                f"screens 배열에 screen_id={screen_id}, route={expected_route!r} 항목을 추가한다.",
            )
            continue
        actual_route = s.get("route")
        if actual_route != expected_route:
            report.error(
                rel(SCREEN_CONTRACT_PATH), screen_id,
                f"route가 {actual_route!r}이며 고정값 {expected_route!r}과 다르다.",
                f"{screen_id}의 route를 {expected_route!r}로 고정한다.",
            )

    extra_ids = sorted(set(by_id) - set(FIXED_SCREENS))
    if extra_ids:
        report.error(
            rel(SCREEN_CONTRACT_PATH), ",".join(extra_ids),
            f"고정 화면 5개(SCR-001~005) 밖의 Screen이 선언되어 있다: {extra_ids}.",
            "화면은 정확히 5개(핵심 4개 + 보조 1개)만 허용된다 -- 추가 Screen을 제거하거나 "
            "기존 5개 중 하나로 통합한다.",
        )


def check_page_owner_uniqueness(report: Report, manifest_rows: list[dict]) -> None:
    owners: dict[str, list[str]] = {sid: [] for sid in FIXED_SCREENS}
    for row in manifest_rows:
        if (row.get("category") or "").strip() != "PAGE_OWNER":
            continue
        for sid in parse_screen_field(row.get("screen")):
            if sid in owners:
                owners[sid].append(row.get("task_id") or "?")

    for screen_id, task_ids in owners.items():
        if len(task_ids) == 0:
            slug = screen_id.replace("-", "")
            report.error(
                rel(TASK_MANIFEST_PATH), screen_id,
                "Page Owner Task(category=PAGE_OWNER)가 하나도 없다.",
                f"TASKS/TASK-PAGE-{slug}.md 같은 PAGE_OWNER Task를 만들고 "
                f"TASK_MANIFEST.csv에서 category=PAGE_OWNER, screen={screen_id}로 지정한다.",
            )
        elif len(task_ids) > 1:
            report.error(
                rel(TASK_MANIFEST_PATH), screen_id,
                f"Page Owner Task가 {len(task_ids)}개다({', '.join(task_ids)}) -- 정확히 1개여야 한다.",
                "중복된 PAGE_OWNER Task 중 하나만 남기고, 나머지는 COMPONENT 등 다른 category로 "
                "재분류하거나 제거한다.",
            )


def check_technical_routes(report: Report, contract: dict, manifest_rows: list[dict]) -> None:
    for tr in contract.get("technical_routes", []):
        route = tr.get("route")
        if tr.get("counted_as_screen") is not False:
            report.error(
                rel(SCREEN_CONTRACT_PATH), "-",
                f"기술 경로 {route!r}의 counted_as_screen이 false로 선언되어 있지 않다.",
                "technical_routes 항목은 counted_as_screen: false로 선언해 화면 수(5개) 계산에서 "
                "제외한다.",
            )

    allowed_route_values = set(FIXED_SCREENS.values()) | {"-", "", COMMON_ROUTE_VALUE}
    for row in manifest_rows:
        route = (row.get("route") or "").strip()
        if not route or route in allowed_route_values:
            continue
        task_id = row.get("task_id") or "?"
        screen_field = row.get("screen") or "-"
        is_technical = route == "*" or route in ALLOWED_TECHNICAL_ROUTE_EXACT or route.startswith(
            ALLOWED_TECHNICAL_ROUTE_PREFIXES
        )
        if is_technical:
            report.error(
                rel(TASK_MANIFEST_PATH), screen_field,
                f"Task {task_id}의 route={route!r}가 기술 경로를 사용자 화면 route로 세고 있다.",
                "기술 경로(/auth/callback, /api/**, not-found)는 Screen route가 아니다 -- "
                "route 칸을 '-'로 비우고 technical_routes 항목으로만 관리한다.",
            )
        else:
            report.error(
                rel(TASK_MANIFEST_PATH), screen_field,
                f"Task {task_id}의 route={route!r}가 고정 화면 5개 {sorted(FIXED_SCREENS.values())} "
                "중 어디에도 속하지 않는다.",
                "route를 고정 화면 5개 중 하나로 맞춘다. 새 Screen이 정말 필요하면 코드를 먼저 만들지 "
                "말고 design-reference/SCREEN_ROUTE_CONTRACT.json 갱신과 사용자 승인을 먼저 받는다.",
            )


def check_scr003_dual_coverage(report: Report, manifest_rows: list[dict]) -> None:
    scr003_task_ids = [
        (row.get("task_id") or "").upper()
        for row in manifest_rows
        if "SCR-003" in parse_screen_field(row.get("screen"))
    ]
    has_travel_input = any("FLIGHT" in tid or "HOTEL" in tid for tid in scr003_task_ids)
    has_mate_write = any("MATE" in tid for tid in scr003_task_ids)

    if not has_travel_input:
        report.error(
            rel(TASK_MANIFEST_PATH), "SCR-003",
            "SCR-003에 항공/호텔 여행 입력(Flight/Hotel Form) Task가 없다.",
            "CMP-SCR003-FLIGHT-FORM / CMP-SCR003-HOTEL-FORM 같은 Task를 screen=SCR-003으로 추가한다.",
        )
    if not has_mate_write:
        report.error(
            rel(TASK_MANIFEST_PATH), "SCR-003",
            "SCR-003에 동행 작성(Mate Write) Task가 없다.",
            "CMP-SCR003-MATE-WRITE 같은 Task를 screen=SCR-003으로 추가한다.",
        )


# ---------------------------------------------------------------------------
# ci 단계 검사 (4번 + Page 구현 여부 + 공개 경로) -- app/src/app 파일 시스템 사용
# ---------------------------------------------------------------------------

def find_page_files() -> list[Path]:
    if not APP_SRC_APP_DIR.exists():
        return []
    found: set[Path] = set()
    for name in PAGE_FILE_NAMES:
        found.update(APP_SRC_APP_DIR.rglob(name))
    return sorted(found)


def check_no_extra_pages(report: Report, contract: dict) -> None:
    allowed: set[Path] = set()
    for s in contract.get("screens", []):
        page_entry = s.get("page_entry")
        if page_entry:
            allowed.add((ROOT / "app" / page_entry).resolve())

    for page_file in find_page_files():
        resolved = page_file.resolve()
        if resolved in allowed:
            continue
        rel_path = rel(resolved)
        lower = rel_path.lower()
        keyword_hit = next(
            (kw for kw in FORBIDDEN_PAGE_KEYWORDS if kw.strip("/") in lower), None
        )
        if keyword_hit:
            hint = (
                f"'{keyword_hit}' 관련 화면은 새 Page/Route가 아니라 해당 Screen(주로 SCR-001)의 "
                "Drawer/Modal/Tab 컴포넌트로 통합해야 한다(app/docs/06_SRS_UIUX_REVISED.md §3.5, "
                "05_UIUX_APPROVED.md §2 대응표 참고)."
            )
        else:
            hint = (
                "고정 5개 Screen의 page_entry 목록 밖에 있는 Page다. 새 Screen이 실제로 필요하면 "
                "코드를 먼저 만들지 말고 design-reference/SCREEN_ROUTE_CONTRACT.json 갱신과 "
                "사용자 승인을 먼저 받는다. 아니면 기존 Screen의 하위 컴포넌트로 옮긴다."
            )
        report.error(
            rel_path, "-",
            "고정 5개 Screen 밖에 새 Page 파일이 존재한다.",
            hint,
        )


def check_pages_implemented(report: Report, contract: dict) -> None:
    for s in contract.get("screens", []):
        screen_id = s.get("screen_id")
        page_entry = s.get("page_entry")
        if not page_entry:
            report.error(
                rel(SCREEN_CONTRACT_PATH), screen_id,
                "page_entry가 SCREEN_ROUTE_CONTRACT.json에 지정되어 있지 않다.",
                f"{screen_id}의 page_entry 값을 채운다.",
            )
            continue
        page_path = ROOT / "app" / page_entry
        if not page_path.exists():
            report.error(
                rel(page_path), screen_id,
                "mode=ci 기준으로 이 화면의 Page 파일이 아직 구현되지 않았다.",
                f"{screen_id}의 Page Owner Task(PAGE-{screen_id.replace('-', '')})를 완료해 "
                f"{rel(page_path)}를 생성한다.",
            )


def check_starter_template_removed(report: Report, contract: dict) -> None:
    for s in contract.get("screens", []):
        if not s.get("starter_template_forbidden"):
            continue
        screen_id = s.get("screen_id")
        page_entry = s.get("page_entry")
        if not page_entry:
            continue
        page_path = ROOT / "app" / page_entry
        if not page_path.exists():
            continue  # check_pages_implemented가 이미 보고함
        text = page_path.read_text(encoding="utf-8", errors="replace")
        hits = [m for m in STARTER_TEMPLATE_MARKERS if m in text]
        if hits:
            report.error(
                rel(page_path), screen_id,
                f"create-next-app 기본 스타터 잔재가 남아있다({', '.join(hits)}).",
                "CLAUDE.md 규칙 10에 따라 Next.js 로고·'To get started' 문구·Vercel Deploy/Docs "
                "버튼 등을 완전히 제거한다.",
            )


# ---------------------------------------------------------------------------
# release 단계 검사 (6번) -- Preview Checkpoint 문서
# ---------------------------------------------------------------------------

def check_preview_checkpoints(report: Report) -> None:
    for screen_id in FIXED_SCREENS:
        f = PREVIEW_CHECKS_DIR / f"{screen_id}.md"
        if not f.exists():
            report.error(
                rel(f), screen_id,
                "release 검사에 필요한 Preview Checkpoint 문서가 없다.",
                f"사람이 Vercel Preview로 {screen_id}를 확인한 뒤 {rel(f)}를 작성한다"
                "(CLAUDE.md 규칙 22: Preview 확인 후 다음 Wave).",
            )
        elif f.stat().st_size == 0:
            report.error(
                rel(f), screen_id,
                "Preview Checkpoint 문서가 비어 있다.",
                f"{rel(f)}에 실제 확인 내용(확인자, 일시, 확인한 화면 상태)을 기록한다.",
            )


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=["plan", "ci", "release"],
        default="plan",
        help=(
            "plan(기본값)=Page Owner/경로 계획만, "
            "ci=구현된 Page 파일+공개 경로 추가 검사, "
            "release=ci+Preview Checkpoint 추가 검사"
        ),
    )
    args = parser.parse_args()

    report = Report()

    contract = load_screen_contract(report)
    manifest_rows = load_task_manifest(report)

    if contract is not None and manifest_rows is not None:
        check_fixed_screens(report, contract)
        check_page_owner_uniqueness(report, manifest_rows)
        check_technical_routes(report, contract, manifest_rows)
        check_scr003_dual_coverage(report, manifest_rows)

        if args.mode in ("ci", "release"):
            check_no_extra_pages(report, contract)
            check_pages_implemented(report, contract)
            check_starter_template_removed(report, contract)

        if args.mode == "release":
            check_preview_checkpoints(report)
    else:
        print("[check_screen_contract] 입력 파일을 읽지 못해 이후 검사를 건너뜀.")

    if report.ok:
        print(f"[check_screen_contract] SCREEN_CONTRACT_PASS (mode={args.mode})")
        return 0

    print(f"[check_screen_contract] {len(report.issues)}개 오류 발견 (mode={args.mode}):\n")
    for issue in report.issues:
        print(issue.render())
        print()

    print(f"[check_screen_contract] SCREEN_CONTRACT_FAIL ({len(report.issues)} errors, mode={args.mode})")
    return 1


if __name__ == "__main__":
    sys.exit(main())
