# Output formats

Contents: [Markdown](#markdown-md) · [JSON](#json-per-paragraph-keys) · [Word / PDF](#word--pdf) · [HTML](#html)

Write the content once (as the keyed draft or Markdown), then derive other formats from it.

## Markdown (.md)

One file per module: `manual-<module>.md`.

```markdown
# <Module name> — คู่มือการใช้งาน
เวอร์ชันระบบ: <version> · ผู้อ่าน: <audience> · อัปเดต: <date>

## สารบัญ
(list of task headings)

## <Task name>
**เป้าหมาย:** ...
**ก่อนเริ่ม:** ...
1. ...
2. ...
> ผลลัพธ์ที่ควรเห็น: ...

**ตัวอย่าง:** ...
**ถ้าเจอปัญหา**
- ปัญหา → สาเหตุ → วิธีแก้
```

Screenshot placeholder: `![<what the screen shows>](images/<module>-<task>-<n>.png)`.

## JSON (per-paragraph keys)

Use when the manual is shown inside an app and must be translated. Produce **two things**:

1. **Locale files**, one per language, same key set: `<locales>/th/manual.json`, `<locales>/en/manual.json`. Follow the project's existing path if there is one.
2. **A keyed draft** (`manual-<module>.md`) where every paragraph is preceded by its key, so a human can review wording without opening JSON:

```markdown
## restTables  <!-- section id -->
<!-- restTables.title -->
การจัดการโต๊ะ
<!-- restTables.goal -->
เปิดโต๊ะ เพิ่มรายการ และย้ายโต๊ะ
<!-- restTables.step1 -->
กดปุ่ม **เปิดโต๊ะ** แล้วเลือกหมายเลขโต๊ะ
```

JSON shape: one object per section, one string per paragraph.

```json
{
  "restTables": {
    "title": "การจัดการโต๊ะ",
    "goal": "เปิดโต๊ะ เพิ่มรายการ และย้ายโต๊ะ",
    "step1": "กดปุ่ม **เปิดโต๊ะ** แล้วเลือกหมายเลขโต๊ะ",
    "step2a": "..."
  }
}
```

Rules:

- Keys are stable identifiers (`section.paragraph`, camelCase, e.g. `restTables.step2a`). Name them by role (`goal`, `step1`, `example`, `trouble1`), never by wording, so a text change never forces a key change.
- Every key exists in every language file. If a translation is not ready, copy the source text and mark it `[ต้องแปล]` so the checker can find it.
- Insert a new step between `step2` and `step3` as `step2a`; do not renumber existing keys.
- Keep inline markup minimal and consistent with the existing file (for example `**bold**` for UI labels). No layout HTML.
- Screenshot references: add a key such as `restTables.img1` only if the project's manual page already uses image keys; otherwise note the screenshot in the draft only.
- Valid UTF-8, no trailing commas. Run `scripts/check_manual_json.py` before delivering.

## Word / PDF

Start from the Markdown draft. Read the matching skill first (`docx` for .docx, `pdf` for .pdf) and follow it for creation and rendering. Manual-specific requirements: title block with system name, version, audience and date; a table of contents; headings that match the task names; numbered steps kept intact across page breaks where possible; Thai font that renders correctly (check the output visually after rendering).

## HTML

A single self-contained file (inline CSS, no external requests) so it opens offline.

- Each task section gets an anchor id (`<section id="manual-<task>">`) and a sidebar or top table of contents linking to them.
- Responsive layout; readable base font size; steps as `<ol>`; expected results and warnings as visually distinct callouts.
- Print stylesheet that hides the navigation.
- Light and dark colors via CSS variables if the page may be viewed in both.
