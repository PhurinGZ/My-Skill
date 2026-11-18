---
name: odoo-fx-project-reports
description: Fix and improve QWeb PDF reports for FX Project including totals, table alignment, and XML validation.
---

You are an Odoo QWeb and reporting expert.

## Common Report Files
- `fx_project_entry_report.xml`
- `fx_project_entry_deduction_material_document`
- `fx_project_entry_deduction_lodging_document`

## Common Issues & Fixes

### XML Syntax
- `<t t-else>` must be `<t t-else="">`
- Ensure all tags are properly closed

### Table Alignment
- Every `<tr>` must have the same number of `<td>`
- Use empty `<td>` instead of removing columns
- Avoid conditional column removal

### Totals
- Totals must match backend compute logic
- Never re-calculate business logic differently in QWeb

---

## Constraints
- Do NOT change column meaning
- Do NOT duplicate calculation logic
