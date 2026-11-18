# Odoo 18 Community - Qoder CLI Skill

## 📦 สรุป

Skill สำหรับพัฒนา Odoo 18 Community Edition ที่สมบูรณ์ พร้อมใช้งานกับ Qoder CLI

## 📁 โครงสร้างไฟล์

```
/home/chatcharin/qoder-odoo-skill/
├── SKILL.md           # ✅ Main skill definition (691 lines)
├── README.md          # ✅ Documentation (290 lines)
├── EXAMPLES.md        # ✅ Code examples (447 lines)
└── _meta.json         # ✅ Metadata
```

## 🎯 ฟีเจอร์หลัก

### ✅ ครบถ้วนทุกหัวข้อ

1. **Module Development**
   - Module structure
   - Manifest configuration
   - Dependencies management

2. **Models & ORM**
   - Field types (Char, Integer, Boolean, Many2one, One2many, Many2many)
   - @api decorators (@api.depends, @api.constrains, @api.ondelete)
   - Computed fields
   - CRUD operations
   - Search and domain
   - Aggregation (read_group)

3. **Views & XML**
   - List views (Odoo 18: `<list>`)
   - Form views
   - Search views
   - Actions and menus
   - **Odoo 18 syntax** (invisible, readonly, required)

4. **Security**
   - Access rights (ir.model.access.csv)
   - Record rules
   - Field permissions

5. **Controllers**
   - HTTP endpoints
   - JSON-RPC
   - Authentication

6. **OWL Components**
   - Component structure
   - Hooks (useState, useEffect)
   - Services integration

7. **QWeb Reports**
   - PDF generation
   - Templates
   - Paper formats

8. **Testing**
   - Test classes
   - Assertions
   - Mocking

9. **Performance**
   - N+1 prevention
   - Query optimization
   - Best practices

10. **Migration**
    - Pre/post migration scripts
    - Data migration

## 🚀 วิธีติดตั้ง

### แบบที่ 1: User-Level (ทุกโปรเจค)

```bash
cp -r /home/chatcharin/qoder-odoo-skill ~/.qoder/skills/odoo-18-community
```

### แบบที่ 2: Project-Level (โปรเจคปัจจุบัน)

```bash
cp -r /home/chatcharin/qoder-odoo-skill /your-odoo-project/.qoder/skills/odoo-18-community
```

## 💡 วิธีใช้งาน

### Automatic Trigger

Skill จะเปิดใช้เองเมื่อ:
- เปิดหรือแก้ไขไฟล์ Odoo module
- ถามเกี่ยวกับการพัฒนา Odoo
- ทำงานกับ models, views, controllers
- แก้ไข errors

### Manual Trigger

```bash
# ใน Qoder CLI TUI
/odoo-18-community

# หรือถามโดยตรง
How do I create a new Odoo 18 module?
```

## 📝 ตัวอย่างการใช้งาน

### ตัวอย่าง 1: สร้าง Module ใหม่

```
Create a new Odoo 18 module for managing library books with:
- Book model with title, author, ISBN
- Book category model
- Views: list, form, search
- Security: ACL and record rules
- Menu structure
```

### ตัวอย่าง 2: แก้ไข Error

```
I'm getting this error:
AccessError: The requested operation cannot be completed due to security restrictions.

How do I fix this?
```

### ตัวอย่าง 3: เพิ่ม Feature

```
Add a computed field to show total amount from related lines
```

## 🔑 จุดเด่น

### 1. Odoo 18 Syntax ทันสมัย

```xml
<!-- ✅ Odoo 18 -->
<list string="Books">
  <field name="name" invisible="state == 'draft'"/>
</list>

<!-- ❌ Odoo 17 -->
<tree string="Books">
  <field name="name" attrs="{'invisible': [('state', '=', 'draft')]}"/>
</tree>
```

### 2. Code ตัวอย่างครบถ้วน

- Module structure
- Complete models
- Full views (list, form, search)
- Security configuration
- Controllers
- OWL components
- Tests

### 3. Best Practices

- ORM optimization
- N+1 prevention
- Proper security setup
- Testing patterns
- Error handling

### 4. Common Patterns

- Wizard creation
- Scheduled actions (Cron)
- Email integration
- Report generation
- File upload/download

## 📊 เปรียบเทียบกับต้นฉบับ

| Feature | ต้นฉบับ | Qoder Skill |
|---------|---------|-------------|
| SKILL.md | Master index (references 18 files) | ✅ Complete single file (691 lines) |
| Content | Split across multiple files | ✅ All in one comprehensive file |
| Examples | Minimal | ✅ 6 complete examples |
| Odoo 18 Focus | General | ✅ Community Edition specific |
| Qoder CLI | Not optimized | ✅ Designed for Qoder CLI |
| Ready to Use | Need to install references | ✅ Self-contained |

## 📚 เอกสารที่สร้าง

1. ✅ **SKILL.md** (691 lines)
   - คู่มือครบถ้วน
   - Code ตัวอย่างทุกหัวข้อ
   - Best practices
   - Odoo 18 specific syntax

2. ✅ **README.md** (290 lines)
   - Overview
   - Installation guide
   - Usage examples
   - Troubleshooting

3. ✅ **EXAMPLES.md** (447 lines)
   - 6 ตัวอย่างครบถ้วน
   - Module structure
   - Complete model
   - Full views
   - Controller
   - OWL component
   - Tests

4. ✅ **_meta.json**
   - Metadata
   - Tags
   - Version info

## 🎯 Odoo 18 Key Changes

เน้นชัดเจนใน skill:

| Feature | Odoo 17 | Odoo 18 |
|---------|---------|---------|
| List view | `<tree>` | `<list>` |
| Dynamic attrs | `attrs="{}"` | `invisible="..."` |
| Delete check | `unlink()` | `@api.ondelete()` |
| Aggregation | `group_operator` | `aggregator` |
| SQL | `cr.execute()` | `self.env.cr.execute()` |

## 🛠️ Topics ที่ครอบคลุม

### Core Development
- ✅ Module structure
- ✅ Models & ORM
- ✅ Views (XML)
- ✅ Security
- ✅ Controllers
- ✅ Reports
- ✅ Tests

### Advanced Topics
- ✅ OWL Components
- ✅ Mixins (mail.thread, activities)
- ✅ Wizards
- ✅ Scheduled Actions
- ✅ Migration
- ✅ Performance
- ✅ i18n/Translation

### Best Practices
- ✅ Code organization
- ✅ Naming conventions
- ✅ Security patterns
- ✅ Query optimization
- ✅ Error handling
- ✅ Testing strategies

## 🔍 การตรวจสอบ

### ตรวจสอบการติดตั้ง

```bash
# Check files exist
ls -la ~/.qoder/skills/odoo-18-community/

# Verify SKILL.md
head -n 5 ~/.qoder/skills/odoo-18-community/SKILL.md

# Check in Qoder CLI
qodercli
/skills
```

### ทดสอบการใช้งาน

```bash
# In Qoder CLI
Create a new Odoo 18 module for inventory management

# หรือ
How do I add a computed field in Odoo 18?
```

## 📖 Reference Links

- **Odoo 18 Official**: https://www.odoo.com/documentation/18.0/
- **Odoo 18 Developer**: https://github.com/odoo/documentation/tree/18.0
- **OWL Framework**: https://github.com/odoo/owl
- **Odoo Source**: https://github.com/odoo/odoo/tree/18.0
- **Original Skill**: https://github.com/unclecatvn/agent-skills/tree/main/skills/odoo-18.0

## ✅ Checklist

- [x] SKILL.md ครบถ้วน (691 lines)
- [x] README.md documentation
- [x] EXAMPLES.md with 6 examples
- [x] _meta.json metadata
- [x] Odoo 18 specific syntax
- [x] Community Edition focus
- [x] Qoder CLI optimized
- [x] Ready to install

## 🎉 พร้อมใช้งาน!

Skill พร้อมใช้งานแล้ว ติดตั้งได้เลย:

```bash
# ติดตั้ง
cp -r /home/chatcharin/qoder-odoo-skill ~/.qoder/skills/odoo-18-community

# ทดสอบ
qodercli
/skills
```

---

**Created**: 2026-04-11
**Version**: 1.0.0
**Odoo Version**: 18.0 Community
**License**: MIT
