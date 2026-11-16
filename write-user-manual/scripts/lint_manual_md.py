#!/usr/bin/env python3
"""Lint manual .md files against the mechanical audit rules.

Usage: python lint_manual_md.py <file-or-dir> [more paths...]

Checks (each finding is a prompt to review, not proof of a bug):
  LONG     numbered procedure with more than 7 steps
  MULTI    numbered step that chains actions with 2+ arrows (split it)
  NOSTEPS  task section (has a goal line) with no numbered steps
  NOWARN   section has a destructive step (delete/cancel/void/close/reset/adjust)
           but no warning callout in the same section
  VERSION  missing version line, or a placeholder instead of a real version
  EMAIL    e-mail address on a non-example domain (use example.com)
  MARKER   leftover [ต้องตรวจ] / [ต้องแปล] / TODO
Exit code 0 when nothing is found, 1 otherwise.
"""
import os
import re
import sys

DESTRUCTIVE = re.compile(
    r"ลบ|ยกเลิก|ปิดบิล|ปิดยอด|รีเซ็ต|ปรับแต้ม|ปรับสต็อก|"
    r"\b(delete|remove|cancel|void|close|reset|adjust)\b",
    re.I,
)
WARN = re.compile(r"^>\s*\*\*(ข้อควรระวัง|คำเตือน|Warning|Caution)", re.M | re.I)
GOAL = re.compile(r"\*\*(เป้าหมาย|Goal)")
NUMBERED = re.compile(r"^\s{0,3}\d+\.\s")
PLACEHOLDER_VERSION = re.compile(
    r"ปัจจุบัน|development|dev build|latest|current|ล่าสุด|n/a|tbd|unknown", re.I
)
SAFE_DOMAINS = ("example.com", "example.org", "example.net", "localhost", "test")


def files(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, _, names in os.walk(p):
                for n in sorted(names):
                    if n.endswith(".md"):
                        yield os.path.join(root, n)
        else:
            yield p


def lint(path):
    out = []
    text = open(path, encoding="utf-8").read()
    parts = re.split(r"\n(?=## )", text)
    head, sections = parts[0], parts[1:]

    m = re.search(r"(เวอร์ชันระบบ|System version)\s*[:：]\s*([^·\n]+)", head)
    if not m:
        out.append(("VERSION", "no version line in the header"))
    elif PLACEHOLDER_VERSION.search(m.group(2)):
        out.append(("VERSION", f"placeholder instead of a real version: {m.group(2).strip()}"))

    for sec in sections:
        title = sec.split("\n")[0].strip()
        if re.match(r"##\s*(สารบัญ|table of contents|contents)", title, re.I):
            continue
        lines = sec.split("\n")
        steps = [l for l in lines if NUMBERED.match(l) and "](#" not in l]

        run = best = 0
        for l in lines:
            if NUMBERED.match(l) and "](#" not in l:
                run += 1
                best = max(best, run)
            elif l.strip() and not re.match(r"^\s{2,}", l):
                run = 0
        if best > 7:
            out.append(("LONG", f"{title}: {best} steps in one procedure"))

        for l in steps:
            if l.count("→") >= 2:
                out.append(("MULTI", f"{title}: {l.strip()[:90]}"))

        if GOAL.search(sec) and not steps:
            out.append(("NOSTEPS", f"{title}: task section without numbered steps"))

        destructive = [l for l in steps if DESTRUCTIVE.search(l.replace('ติดลบ', ''))]
        if destructive and not WARN.search(sec):
            out.append(("NOWARN", f"{title}: {destructive[0].strip()[:90]}"))

    for email in sorted(set(re.findall(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)", text))):
        if not any(email == d or email.endswith("." + d) or email == d for d in SAFE_DOMAINS):
            out.append(("EMAIL", f"non-example domain used: @{email}"))

    for mk in ("[ต้องตรวจ]", "[ต้องแปล]", "TODO"):
        n = text.count(mk)
        if n:
            out.append(("MARKER", f"{n} x {mk}"))
    return out


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    total = 0
    for f in files(paths):
        found = lint(f)
        if found:
            print(f"\n{f}")
            for code, msg in found:
                print(f"  {code:8} {msg}")
            total += len(found)
    print(f"\nFindings: {total}")
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
