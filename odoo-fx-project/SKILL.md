---
name: odoo-fx-project-domain
author: PhurinGZ
description: Understand and modify FX Project domain logic including models, calculations, state flow, and permissions in Odoo 17.
---

You are a senior Odoo 17 developer with deep knowledge of the FX Project module.

## When to Use This Skill
Use this skill when:
- Working on FX Project models or business logic
- Modifying calculation of totals or deductions
- Debugging incorrect amounts or state transitions
- Reviewing permissions or approval flows

---

## Domain Model Overview

### Core Models
- `fx.project`  
  Represents a construction/project entity.

- `fx.project.entry`  
  Work entry documents (Input 1 / Input 2).

- `fx.project.entry.line`  
  Individual work lines inside an entry.

- `fx.project.area.total`  
  Aggregated BOQ totals grouped by area.

- `fx.setting.category`  
  Work categories (main, sub1, sub2 hierarchy).

- `fx.setting.item`  
  Master list of work items.

---

## Business Logic Rules

### Amount Calculation
- `total_work_amount`
  - Sum of work amounts from `fx.project.entry.line`

- `deduction_material_amount`
  - Cost deductions with `type = material`

- `deduction_lodging_amount`
  - Cost deductions with `type = lodging`

- `total_amount`
  - Net total  
    `total_work_amount - deduction_material_amount - deduction_lodging_amount`

All totals should be calculated using `@api.depends` compute methods.

---

### State Flow
The document state must follow this exact order:

draft
→ submitted
→ approved_oe
→ approved_pm
→ pending_acc
→ done

yaml
Copy code

State transitions must:
- Respect user permissions
- Never skip intermediate states
- Be enforced at both UI and backend levels

---

## Permissions & Approval

### Groups
- `group_fx_project_oe`
  - OE approval

- `group_fx_project_manager`
  - PM approval

- `group_fx_project_accounting`
  - Accounting approval

### Rules
- Permissions must be enforced server-side
- Views may hide buttons, but backend must validate access
- Never rely on frontend-only permission checks

---

## Technical Standards (Odoo 17)

### Python
- Use `@api.depends` for computed fields
- Avoid side effects in compute methods
- Use proper `One2many` / `Many2one` relations

### XML & Views
- Always validate XML structure
- `<label>` tags must include `for`
- Use domains and context explicitly
- Avoid deprecated `attrs`

---

## Constraints
- Do NOT change business meaning of calculations
- Do NOT rename states without migration
- Do NOT bypass permission groups
- Always read existing files before editing

---

## Output Expectations
- Correct business calculations
- Stable approval workflow
- Code aligned with Odoo 17 best practices
- Clear explanation if logic is non-obvious