# Odoo 18 Security Guide

Complete guide for configuring security in Odoo 18 modules.

## Access Control Lists (ACL)

### ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0
access_my_model_manager,my.model.manager,model_my_model,base.group_system,1,1,1,1
access_my_model_admin,my.model.admin,model_my_model,my_module.group_admin,1,1,1,1
```

### Format

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

- **id**: Unique identifier
- **name**: Descriptive name
- **model_id:id**: Model reference (model_ + model.name with dots replaced by underscores)
- **group_id:id**: User group (optional, leave empty for global)
- **perm_read**: Read permission (0 or 1)
- **perm_write**: Write permission (0 or 1)
- **perm_create**: Create permission (0 or 1)
- **perm_unlink**: Delete permission (0 or 1)

### Common Patterns

```csv
# User can read and create, but not delete
access_my_model_user,my.model.user,model_my_model,base.group_user,1,1,1,0

# Manager has full access
access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1

# Public read-only
access_my_model_public,my.model.public,model_my_model,,1,0,0,0

# Accounting team only
access_my_model_accountant,my.model.accountant,model_my_model,account.group_account_user,1,1,1,1
```

## Record Rules

### Basic Record Rule

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="rule_my_model_user" model="ir.rule">
        <field name="name">My Model: User can see own records</field>
        <field name="model_id" ref="model_my_model"/>
        <field name="domain_force">[('create_uid', '=', user.id)]</field>
        <field name="groups" eval="[(4, ref('base.group_user'))]"/>
        <field name="perm_read" eval="True"/>
        <field name="perm_write" eval="True"/>
        <field name="perm_create" eval="True"/>
        <field name="perm_unlink" eval="True"/>
    </record>
</odoo>
```

### Common Record Rules

```xml
<!-- Multi-company rule -->
<record id="rule_my_model_company" model="ir.rule">
    <field name="name">My Model: Multi-company</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('company_id', 'in', company_ids)]</field>
    <field name="global" eval="True"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="True"/>
</record>

<!-- Personal documents only -->
<record id="rule_personal_documents" model="ir.rule">
    <field name="name">Personal Documents Only</field>
    <field name="model_id" ref="model_my_document"/>
    <field name="domain_force">[('user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>

<!-- Department based -->
<record id="rule_department_expenses" model="ir.rule">
    <field name="name">Department Expenses</field>
    <field name="model_id" ref="model_hr_expense"/>
    <field name="domain_force">[('employee_id.department_id', 'in', user.employee_id.department_id.ids)]</field>
</record>

<!-- State based -->
<record id="rule_draft_documents" model="ir.rule">
    <field name="name">Draft Documents</field>
    <field name="model_id" ref="model_my_document"/>
    <field name="domain_force">[('state', '=', 'draft')]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
    <field name="perm_read" eval="True"/>
    <field name="perm_write" eval="True"/>
    <field name="perm_create" eval="True"/>
    <field name="perm_unlink" eval="False"/>
</record>

<!-- Global rule (all users) -->
<record id="rule_active_only" model="ir.rule">
    <field name="name">Active Records Only</field>
    <field name="model_id" ref="model_my_model"/>
    <field name="domain_force">[('active', '=', True)]</field>
    <field name="global" eval="True"/>
</record>
```

## User Groups

### Define Groups

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Category -->
    <record id="module_category_my_module" model="ir.module.category">
        <field name="name">My Module</field>
        <field name="description">My Module Access Rights</field>
        <field name="sequence">20</field>
    </record>

    <!-- Group: User -->
    <record id="group_my_user" model="res.groups">
        <field name="name">User</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    </record>

    <!-- Group: Manager -->
    <record id="group_my_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('group_my_user'))]"/>
        <field name="users" eval="[(4, ref('base.user_admin'))]"/>
    </record>

    <!-- Group: Administrator -->
    <record id="group_my_admin" model="res.groups">
        <field name="name">Administrator</field>
        <field name="category_id" ref="module_category_my_module"/>
        <field name="implied_ids" eval="[(4, ref('group_my_manager'))]"/>
    </record>
</odoo>
```

## Field Level Security

### Using Groups

```xml
<record id="view_my_model_form" model="ir.ui.view">
    <field name="name">my.model.form</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <form>
            <group>
                <!-- Visible to all -->
                <field name="name"/>
                
                <!-- Restricted to managers -->
                <field name="cost_price" groups="my_module.group_my_manager"/>
                
                <!-- Restricted to multiple groups -->
                <field name="secret_field" groups="base.group_system,my_module.group_my_admin"/>
            </group>
        </form>
    </field>
</record>
```

### Readonly Fields

```xml
<!-- Readonly for specific group -->
<field name="state" readonly="1" groups="my_module.group_my_user"/>

<!-- Editable for managers -->
<field name="state" readonly="state != 'draft'" groups="my_module.group_my_manager"/>
```

## Security Best Practices

### ✅ DO

```csv
# Principle of least privilege
access_my_model_user,my.model.user,model_my_model,base.group_user,1,0,0,0
access_my_model_manager,my.model.manager,model_my_model,my_module.group_manager,1,1,1,1
```

```xml
<!-- Multi-company support -->
<record id="rule_multi_company" model="ir.rule">
    <field name="domain_force">[('company_id', 'in', company_ids)]</field>
    <field name="global" eval="True"/>
</record>
```

### ❌ DON'T

```csv
# Don't give everyone full access
access_my_model_all,my.model.all,model_my_model,,1,1,1,1
```

## Complete Security Example

### security/ir.model.access.csv

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_library_book_user,library.book.user,model_library_book,library_group_user,1,1,1,0
access_library_book_manager,library.book.manager,model_library_book,library_group_manager,1,1,1,1
access_library_borrow_user,library.borrow.user,model_library_borrow,library_group_user,1,1,1,0
access_library_borrow_manager,library.borrow.manager,model_library_borrow,library_group_manager,1,1,1,1
```

### security/security.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- User can see own borrows -->
    <record id="rule_borrow_user" model="ir.rule">
        <field name="name">Personal Borrows</field>
        <field name="model_id" ref="model_library_borrow"/>
        <field name="domain_force">[('user_id', '=', user.id)]</field>
        <field name="groups" eval="[(4, ref('library_group_user'))]"/>
    </record>

    <!-- Manager can see all borrows -->
    <record id="rule_borrow_manager" model="ir.rule">
        <field name="name">All Borrows</field>
        <field name="model_id" ref="model_library_borrow"/>
        <field name="domain_force">[(1, '=', 1)]</field>
        <field name="groups" eval="[(4, ref('library_group_manager'))]"/>
    </record>

    <!-- Multi-company for books -->
    <record id="rule_book_company" model="ir.rule">
        <field name="name">Multi-Company Books</field>
        <field name="model_id" ref="model_library_book"/>
        <field name="domain_force">['|', ('company_id', '=', False), ('company_id', 'in', company_ids)]</field>
        <field name="global" eval="True"/>
    </record>
</odoo>
```

---

**Reference**: Based on Odoo 18 security implementation
**Full Guide**: [Original Odoo 18 Security Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-security-guide.md)
