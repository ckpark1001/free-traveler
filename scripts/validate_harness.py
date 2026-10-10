#!/usr/bin/env python3
"""validate_harness.py -- Traveler harness completeness gate.

Checks that the governance layer itself (root CLAUDE.md, the
traveler-project-pipeline Skill, and the 7 pipeline Commands) exists and
declares the rules/markers every other script and command in this
pipeline assumes are present. This does NOT check TASKS/** or app/src/**
(that is validate_inputs.py's and audit_tasks.py's job) -- it checks the
harness configuration that governs how those are produced.

Checks:

  1  CLAUDE.md exists (repository root)
  2  Claude Code Skill file exists (.claude/skills/traveler-project-pipeline/SKILL.md)
  3  7 Command files exist (.claude/commands/*.md)
  4  traveler-screen-route-v1 Marker exists (CLAUDE.md HARNESS_SCHEMA=...)
  5  D-001 DESIGN path in the marker matches an existing file
  6  Screen Contract path in the marker matches an existing file whose
     schema_version equals the HARNESS_SCHEMA marker value
  7  Page Owner 5-per-screen rule text exists
  8  DB 6-table baseline rule text exists (all 6 table names named)
  9  External input non-persistence rule text exists (flight/hotel)
  10 Playwright Chromium Smoke rule text exists
  11 AUTO_MERGE=false marker exists
  12 AWS_ENABLED=false marker exists
  13 EXCLUDED-protection rule text exists

No third-party dependencies. Prints VALIDATE_HARNESS_PASS and exits 0 when
all 13 checks pass. Otherwise prints the missing files/rules and exits 1.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"
SKILL_MD = ROOT / ".claude/skills/traveler-project-pipeline/SKILL.md"
COMMANDS_DIR = ROOT / ".claude/commands"

EXPECTED_COMMANDS = {
    "gen-tasklist.md",
    "gen-task-details.md",
    "audit-tasks.md",
    "prepare-task.md",
    "implement-task.md",
    "run-wave.md",
    "release-check.md",
}
EXPECTED_HARNESS_SCHEMA = "traveler-screen-route-v1"
EXPECTED_DB_TABLES = [
    "profiles", "mate_posts", "mate_applications",
    "blocks", "reports", "app_settings",
]

MARKER_BLOCK_RE = re.compile(r"##\s*Harness Marker\s*```(.*?)```", re.DOTALL)


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_marker_block(text: str) -> dict[str, str]:
    m = MARKER_BLOCK_RE.search(text)
    if not m:
        return {}
    out: dict[str, str] = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        out[key.strip()] = value.strip()
    return out


class Result:
    def __init__(self) -> None:
        self.checks: list[tuple[str, str, bool, list[str]]] = []

    def add(self, num: str, title: str, passed: bool, details: list[str] | None = None) -> None:
        self.checks.append((num, title, passed, details or []))

    @property
    def all_passed(self) -> bool:
        return all(p for *_, p, _ in self.checks)


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    r = Result()

    # 1. CLAUDE.md exists
    claude_exists = CLAUDE_MD.exists()
    r.add("1", "CLAUDE.md 존재", claude_exists,
          [] if claude_exists else [f"{rel(CLAUDE_MD)} 없음"])

    # 2. Skill file exists
    skill_exists = SKILL_MD.exists()
    r.add("2", "Claude Code Skill 파일 존재", skill_exists,
          [] if skill_exists else [f"{rel(SKILL_MD)} 없음"])

    # 3. 7 Command files exist
    cmd_files = {p.name for p in COMMANDS_DIR.glob("*.md")} if COMMANDS_DIR.exists() else set()
    missing_cmds = sorted(EXPECTED_COMMANDS - cmd_files)
    extra_cmds = sorted(cmd_files - EXPECTED_COMMANDS)
    passed3 = not missing_cmds and len(cmd_files) == 7
    details3 = []
    if not COMMANDS_DIR.exists():
        details3.append(f"{rel(COMMANDS_DIR)} 디렉터리 없음")
    if missing_cmds:
        details3.append(f"누락된 Command 파일: {missing_cmds}")
    if len(cmd_files) != 7:
        details3.append(f"Command 파일 {len(cmd_files)}개 발견(기대 7개){' , 예상 밖 파일: ' + str(extra_cmds) if extra_cmds else ''}")
    r.add("3", "7개 Command 존재", passed3, details3)

    claude_text = CLAUDE_MD.read_text(encoding="utf-8") if claude_exists else ""
    skill_text = SKILL_MD.read_text(encoding="utf-8") if skill_exists else ""
    combined = claude_text + "\n" + skill_text
    marker = parse_marker_block(claude_text)

    if not marker:
        r.add("marker-block", "CLAUDE.md Harness Marker 블록 파싱", False,
              ["CLAUDE.md에서 '## Harness Marker' 코드 블록을 찾지 못함 -- 이후 4/5/6/11/12번 검사가 전부 실패로 처리됨"])

    # 4. traveler-screen-route-v1 marker
    schema_value = marker.get("HARNESS_SCHEMA")
    passed4 = schema_value == EXPECTED_HARNESS_SCHEMA
    r.add("4", f"{EXPECTED_HARNESS_SCHEMA} Marker 존재", passed4,
          [] if passed4 else [f"HARNESS_SCHEMA={schema_value!r} (기대값: {EXPECTED_HARNESS_SCHEMA!r})"])

    # 5. D-001 DESIGN path matches
    design_marker = marker.get("DESIGN_PATH")
    details5 = []
    passed5 = False
    if not design_marker:
        details5.append("CLAUDE.md에 DESIGN_PATH marker 없음")
    else:
        design_file = ROOT / design_marker
        if design_marker != "design-reference/D-001/DESIGN.md":
            details5.append(f"DESIGN_PATH={design_marker!r} (기대값: 'design-reference/D-001/DESIGN.md')")
        elif not design_file.exists():
            details5.append(f"{rel(design_file)} 파일 없음")
        else:
            passed5 = True
    r.add("5", "D-001 DESIGN 경로 일치", passed5, details5)

    # 6. Screen Contract path matches + schema_version cross-check
    screen_marker = marker.get("SCREEN_CONTRACT")
    details6 = []
    passed6 = False
    if not screen_marker:
        details6.append("CLAUDE.md에 SCREEN_CONTRACT marker 없음")
    else:
        screen_file = ROOT / screen_marker
        if screen_marker != "design-reference/SCREEN_ROUTE_CONTRACT.json":
            details6.append(f"SCREEN_CONTRACT={screen_marker!r} (기대값: 'design-reference/SCREEN_ROUTE_CONTRACT.json')")
        elif not screen_file.exists():
            details6.append(f"{rel(screen_file)} 파일 없음")
        else:
            try:
                data = json.loads(screen_file.read_text(encoding="utf-8"))
                sv = data.get("schema_version")
                if sv != schema_value:
                    details6.append(f"{rel(screen_file)}의 schema_version={sv!r}가 HARNESS_SCHEMA={schema_value!r}와 불일치")
                else:
                    passed6 = True
            except json.JSONDecodeError as exc:
                details6.append(f"{rel(screen_file)} JSON 파싱 실패: {exc}")
    r.add("6", "Screen Contract 경로 일치", passed6, details6)

    # 7. Page Owner 5-per-screen rule text
    passed7 = "Page Owner" in combined and "정확히 5개" in combined
    r.add("7", "Page Owner 5개 규칙 존재", passed7,
          [] if passed7 else ["CLAUDE.md/SKILL.md 어디에도 'Page Owner'와 '정확히 5개'가 함께 나타나지 않음"])

    # 8. DB 6-table baseline rule text
    missing_tables = [t for t in EXPECTED_DB_TABLES if t not in combined]
    passed8 = "6개" in combined and "테이블" in combined and not missing_tables
    details8 = []
    if "6개" not in combined or "테이블" not in combined:
        details8.append("'6개'와 '테이블'이 함께 언급된 규칙을 찾지 못함")
    if missing_tables:
        details8.append(f"언급되지 않은 테이블명: {missing_tables}")
    r.add("8", "DB Table 6개 기본 범위 존재", passed8, details8)

    # 9. external input non-persistence rule text
    non_transmit_phrases = ["보내지 않는다", "전달하지 않는다", "비전송"]
    passed9 = "항공" in combined and "숙소" in combined and any(p in combined for p in non_transmit_phrases)
    r.add("9", "외부 입력 비저장 규칙 존재", passed9,
          [] if passed9 else ["'항공'·'숙소' 및 비전송/비전달 문구가 함께 나타나는 규칙을 찾지 못함"])

    # 10. Playwright Chromium Smoke rule text
    passed10 = all(kw in combined for kw in ("Playwright", "Chromium", "Smoke"))
    r.add("10", "Playwright Chromium Smoke 규칙 존재", passed10,
          [] if passed10 else ["'Playwright'·'Chromium'·'Smoke'가 모두 나타나는 규칙을 찾지 못함"])

    # 11. AUTO_MERGE=false
    passed11 = marker.get("AUTO_MERGE") == "false"
    r.add("11", "AUTO_MERGE=false", passed11,
          [] if passed11 else [f"AUTO_MERGE={marker.get('AUTO_MERGE')!r} (기대값: 'false')"])

    # 12. AWS_ENABLED=false
    passed12 = marker.get("AWS_ENABLED") == "false"
    r.add("12", "AWS_ENABLED=false", passed12,
          [] if passed12 else [f"AWS_ENABLED={marker.get('AWS_ENABLED')!r} (기대값: 'false')"])

    # 13. EXCLUDED-protection rule text
    exclude_phrases = ["임의로 구현하지 않는다", "임의 구현 금지", "삭제하지 않는다"]
    passed13 = "EXCLUDED" in combined and any(p in combined for p in exclude_phrases)
    r.add("13", "EXCLUDED 보호 규칙 존재", passed13,
          [] if passed13 else ["'EXCLUDED'와 임의구현 금지/삭제 금지 문구가 함께 나타나는 규칙을 찾지 못함"])

    for num, title, passed, details in r.checks:
        status = "PASS" if passed else "FAIL"
        print(f"[validate_harness] {num:>2}. {status} -- {title}")
        for d in details:
            print(f"       {d}")

    if r.all_passed:
        print(f"\nVALIDATE_HARNESS_PASS ({len(r.checks)} checks)")
        return 0

    failed = sum(1 for *_, p, _ in r.checks if not p)
    print(f"\nVALIDATE_HARNESS_FAIL ({failed}/{len(r.checks)} checks failed)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
