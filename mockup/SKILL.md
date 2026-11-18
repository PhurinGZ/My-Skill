---
name: mockup
description: >
  สร้าง interactive HTML mockup ที่เหมือน Odoo 17/18/19 จริงๆ เพื่อใช้ present งานโดยไม่ต้องมี Odoo จริง ใช้ skill นี้ทุกครั้งที่ user พูดถึง: "mockup odoo", "จำลอง odoo", "ทำหน้า odoo", "odoo demo", "present odoo", "odoo prototype", หรือขอสร้างหน้าจอ ERP ใดๆ ที่คล้าย Odoo skill นี้ครอบคลุมทุก module: Sales, CRM, Inventory, Accounting, HR, Manufacturing, Purchase, Project
---

# Odoo Mockup Skill

สร้าง HTML interactive mockup ที่เหมือน Odoo 17/18/19 สำหรับใช้ present งานโดยไม่ต้องมี Odoo จริง

---

## ขั้นตอนการทำงาน

### 1. ถามข้อมูลจาก User (ถ้ายังไม่มี)

หากผู้ใช้ไม่ได้ระบุรายละเอียด ให้ถามด้วย ask_user_input tool:

- **Module** ที่ต้องการ (Sales, CRM, Inventory, Accounting, HR, Manufacturing, Purchase, Project หรือหลายตัว)
- **View** ที่ต้องการ (List view, Form view, Dashboard, Kanban หรือทั้งหมด)
- **ภาษา** (ไทย / English / ทั้งสอง)
- **ชื่อบริษัท/โลโก้** (หรือใช้ dummy "บริษัท ABC จำกัด" / "ABC Company Ltd.")
- **ข้อมูลพิเศษ** ที่อยากใส่ หรือใช้ dummy

### 2. อ่าน Reference Files

อ่านตามที่จำเป็น:
- `references/design-system.md` — สี, font, component styles ของ Odoo 17–19
- `references/interactions.md` — วิธีทำ navigation, workflow, form interactions
- `references/modules/<module>.md` — โครงสร้างข้อมูลและ UI patterns แต่ละ module

### 3. สร้าง HTML Mockup

สร้างไฟล์ HTML เดียวที่ครบทุกอย่าง (self-contained, ไม่ต้องการ internet):
- ใช้ CSS ที่ defined ใน design-system.md
- ใส่ dummy data ที่สมจริงและแก้ไขได้ง่าย
- มี interaction ครบ: navigate, form edit, workflow status

### 4. Output

- บันทึกไฟล์ไปที่ `/mnt/user-data/outputs/<module>-mockup.html`
- ใช้ `present_files` tool แสดงให้ user download
- บอก user ว่าแก้ข้อมูลได้ที่ส่วนไหนของโค้ด (DATA SECTION)

---

## กฎสำคัญในการสร้าง Mockup

### ความเหมือนจริง (Odoo 17–19 Style)
- Primary color: `#714B67` (Odoo purple)
- Top navbar: สีม่วง, มี logo "odoo", search bar, icons (notification, settings, user avatar)
- Left sidebar: สีขาว, กว้าง 220px, มี menu icons + labels, active item highlight สีม่วงอ่อน
- Content area: `#F5F5F5` background
- Cards/panels: สีขาว, border-radius 8px, shadow เบา
- Font: Inter, Roboto หรือ system-ui
- Buttons: primary = สีม่วง, secondary = outline

### Interactions ที่ต้องมีทุก mockup
1. **Navigate**: คลิก list row → เปิด form view, คลิก Back/Breadcrumb → กลับ list
2. **Form edit**: คลิกปุ่ม Edit → fields กลายเป็น inputs, คลิก Save → success toast
3. **Workflow status bar**: แสดง pipeline (Draft → Confirmed → Done) คลิกเปลี่ยน status
4. **Sidebar navigation**: คลิก menu item → เปลี่ยน active highlight + content
5. **Create new**: ปุ่ม "New" เปิด blank form
6. **Search/Filter**: search bar ใน list view (UI เท่านั้น, ไม่ต้องทำงานจริง)

### Dummy Data
- ใส่ข้อมูลในส่วน `/* ===== DATA SECTION ===== */` ต้นไฟล์ เป็น JavaScript const
- ใช้ชื่อภาษาไทยถ้า user เลือกภาษาไทย (เช่น นายสมชาย, บริษัท ไทยเทค)
- ข้อมูลต้องสมจริงและหลากหลาย (ไม่ใช่ "Test 1", "Test 2")
- อย่างน้อย 5–8 records ใน list view

---

## Module Reference

อ่าน reference ที่ตรงกับ module ที่ user ต้องการ:

| Module | Reference File |
|--------|---------------|
| Sales / CRM | `references/modules/sales-crm.md` |
| Inventory | `references/modules/inventory.md` |
| Accounting | `references/modules/accounting.md` |
| HR / Payroll | `references/modules/hr.md` |
| Manufacturing | `references/modules/manufacturing.md` |
| Purchase | `references/modules/purchase.md` |
| Project | `references/modules/project.md` |

ถ้าต้องการหลาย module ให้สร้าง navigation ระหว่าง module ได้ใน mockup เดียว

---

## ตัวอย่าง User Prompts ที่ควร Trigger Skill นี้

- "ช่วยทำ mockup odoo module sales ให้หน่อย"
- "อยากได้หน้าจอ odoo inventory สำหรับ present ลูกค้า"
- "จำลองหน้า odoo HR payroll"
- "ทำ odoo demo ให้ดูเหมือนจริง"
- "สร้าง prototype odoo accounting"
- "ขอหน้า odoo ที่ navigate ได้"
