---
name: odoo-skill
description: "Odoo 18 Community Edition development skill with comprehensive references. Triggers: Odoo module, addon, model, view, XML, OWL, QWeb, security, migration, manifest, ORM, controller. Use for developing, debugging, refactoring, or reviewing Odoo 18 custom addons."
globs: "**/*.{py,xml,csv,js}"
---

# Odoo 18 Community Development Skill

Master index for Odoo 18 Community Edition development. Read the appropriate guide from `references/` based on your task.

## Quick Reference

| Topic | File | When to Use |
|-------|------|-------------|
| Actions | `references/odoo-18-actions-guide.md` | Creating actions, menus, scheduled jobs, server actions |
| Controllers | `references/odoo-18-controller-guide.md` | Writing HTTP endpoints, routes, web controllers |
| Data Files | `references/odoo-18-data-guide.md` | XML/CSV data files, records, shortcuts |
| Decorators | `references/odoo-18-decorator-guide.md` | Using @api decorators, compute fields, validation |
| Development | `references/odoo-18-development-guide.md` | Creating modules, manifest, reports, security, wizards |
| Field Types | `references/odoo-18-field-guide.md` | Defining model fields, choosing field types |
| Manifest | `references/odoo-18-manifest-guide.md` | __manifest__.py configuration, dependencies, hooks |
| Migration | `references/odoo-18-migration-guide.md` | Upgrading modules, data migration, version changes |
| Mixins | `references/odoo-18-mixins-guide.md` | mail.thread, activities, email aliases, tracking |
| Model Methods | `references/odoo-18-model-guide.md` | Writing ORM queries, CRUD operations, domain filters |
| OWL Components | `references/odoo-18-owl-guide.md` | Building OWL UI components, hooks, services |
| Performance | `references/odoo-18-performance-guide.md` | Optimizing queries, fixing slow code, preventing N+1 |
| Reports | `references/odoo-18-reports-guide.md` | QWeb reports, PDF/HTML, templates, paper formats |
| Security | `references/odoo-18-security-guide.md` | Access rights, record rules, field permissions |
| Testing | `references/odoo-18-testing-guide.md` | Writing tests, mocking, assertions, browser testing |
| Transactions | `references/odoo-18-transaction-guide.md` | Handling database errors, savepoints, UniqueViolation |
| Translation | `references/odoo-18-translation-guide.md` | Adding translations, localization, i18n |
| Views & XML | `references/odoo-18-view-guide.md` | Writing XML views, actions, menus, QWeb templates |

## File Structure

```
odoo-18-community/
├── SKILL.md                          # This file - master index
├── README.md                         # Skill overview and installation
├── EXAMPLES.md                       # Code examples
├── SUMMARY.md                        # Summary documentation
├── _meta.json                        # Skill metadata
└── references/                       # Detailed guides
    ├── odoo-18-actions-guide.md
    ├── odoo-18-controller-guide.md
    ├── odoo-18-data-guide.md
    ├── odoo-18-decorator-guide.md
    ├── odoo-18-development-guide.md
    ├── odoo-18-field-guide.md
    ├── odoo-18-manifest-guide.md
    ├── odoo-18-migration-guide.md
    ├── odoo-18-mixins-guide.md
    ├── odoo-18-model-guide.md
    ├── odoo-18-owl-guide.md
    ├── odoo-18-performance-guide.md
    ├── odoo-18-reports-guide.md
    ├── odoo-18-security-guide.md
    ├── odoo-18-testing-guide.md
    ├── odoo-18-transaction-guide.md
    ├── odoo-18-translation-guide.md
    └── odoo-18-view-guide.md
```

## Odoo 18 Key Changes from v17

| Feature | Odoo 17 | Odoo 18 |
|---------|---------|---------|
| List view tag | `<tree>` | `<list>` |
| Dynamic attributes | `attrs="{'invisible': [...]}"` | `invisible="..."`, `readonly="..."`, `required="..."` |
| Delete validation | Override `unlink()` | `@api.ondelete(at_uninstall=False)` |
| Field aggregation | `group_operator=` | `aggregator=` |
| SQL queries | `cr.execute()` | `self.env.cr.execute()` or `SQL` class |
| Boolean fields | Default False | Must specify `default=False` explicitly |

## Quick Start Workflow

### 1. Create Module Structure

```bash
mkdir -p my_module/{models,views,security,data,controllers,static/src,report,tests}
touch my_module/__init__.py
touch my_module/__manifest__.py
touch my_module/models/__init__.py
```

### 2. Basic Module Files

See `references/odoo-18-development-guide.md` for complete module creation guide.

### 3. Define Model

See `references/odoo-18-model-guide.md` for ORM operations.
See `references/odoo-18-field-guide.md` for field types.
See `references/odoo-18-decorator-guide.md` for @api decorators.

### 4. Create Views

See `references/odoo-18-view-guide.md` for XML views.

### 5. Add Security

See `references/odoo-18-security-guide.md` for ACL and record rules.

### 6. Write Tests

See `references/odoo-18-testing-guide.md` for testing patterns.

## Common Tasks

### Working with Models
- Read guide: `references/odoo-18-model-guide.md`
- Field types: `references/odoo-18-field-guide.md`
- Decorators: `references/odoo-18-decorator-guide.md`
- Mixins: `references/odoo-18-mixins-guide.md`

### Working with Views
- XML views: `references/odoo-18-view-guide.md`
- Data files: `references/odoo-18-data-guide.md`
- Actions: `references/odoo-18-actions-guide.md`

### Working with Controllers
- HTTP endpoints: `references/odoo-18-controller-guide.md`

### Working with OWL
- Components: `references/odoo-18-owl-guide.md`

### Working with Reports
- QWeb reports: `references/odoo-18-reports-guide.md`

### Working with Security
- Access rights: `references/odoo-18-security-guide.md`

### Working with Performance
- Optimization: `references/odoo-18-performance-guide.md`

### Working with Migration
- Upgrade guide: `references/odoo-18-migration-guide.md`

### Working with Transactions
- Error handling: `references/odoo-18-transaction-guide.md`

### Working with Translations
- i18n guide: `references/odoo-18-translation-guide.md`

## Best Practices

1. **Use Odoo 18 syntax** - `<list>` not `<tree>`, `invisible="..."` not `attrs`
2. **Specify field defaults** - `default=False` for Boolean
3. **Use @api.ondelete** - Instead of overriding `unlink()`
4. **Add proper security** - ACL + Record Rules
5. **Write tests** - Cover critical business logic
6. **Optimize queries** - Avoid N+1, use `mapped()`, `search_read()`
7. **Follow naming** - `my.model`, `view_my_model_list`, `action_my_model`
8. **Use mixins** - `mail.thread` for messaging
9. **Handle errors** - Use `ValidationError`, `UserError` appropriately
10. **Document code** - Add docstrings and comments

## Performance Tips

### ✅ DO
```python
# Use search_read for simple queries
data = self.env['my.model'].search_read([('state', '=', 'draft')], ['name', 'state'])

# Prefetch related fields
partners = records.mapped('partner_id')

# Bulk operations
records.write({'state': 'confirmed'})
```

### ❌ DON'T
```python
# N+1 query problem
for record in records:
    partner = record.partner_id  # Query per record!

# Unnecessary loops
for record in records:
    record.write({'state': 'confirmed'})
```

## Debugging

### Common Errors
- **AccessError**: Check `ir.model.access.csv`
- **ValidationError**: Check `@api.constrains`
- **RecursionError**: Check infinite loops in `write()` or `create()`
- **QWeb Error**: Check template ID matches

### Enable Debug Mode
```ini
[options]
debug_mode = True
log_level = debug
```

## Module Structure

Standard Odoo 18 addon:

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── my_model.py
├── views/
│   └── my_model_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── data/
│   └── demo_data.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── static/
│   └── src/
│       ├── js/
│       ├── css/
│       └── xml/
├── report/
│   └── my_report.xml
└── tests/
    ├── __init__.py
    └── test_my_model.py
```

## Useful Commands

```bash
# Update module
./odoo-bin -d dbname -u my_module

# Install module
./odoo-bin -d dbname -i my_module

# Run tests
./odoo-bin -d dbname --test-enable --stop-after-init

# View logs
tail -f /var/log/odoo/odoo.log
```

## External Documentation

- [Odoo 18 Official Documentation](https://www.odoo.com/documentation/18.0/)
- [Odoo 18 Developer Reference](https://github.com/odoo/documentation/tree/18.0)
- [OWL Documentation](https://github.com/odoo/owl)
- [Odoo 18 Source Code](https://github.com/odoo/odoo/tree/18.0)

---

**Skill Version**: 2.0.0
**Odoo Version**: 18.0 Community Edition
**Last Updated**: 2026-04-11
**Structure**: Master index with detailed reference guides
