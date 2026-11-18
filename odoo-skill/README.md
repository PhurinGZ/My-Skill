# Odoo 18 Community Edition - Qoder CLI Skill

Complete development skill for Odoo 18 Community Edition custom modules and addons.

## Overview

This skill provides comprehensive guidance for developing Odoo 18 Community Edition modules, including:

- ✅ Module structure and manifest configuration
- ✅ Model development with ORM operations
- ✅ XML views (Odoo 18 syntax)
- ✅ Security (ACL, record rules)
- ✅ Controllers and HTTP endpoints
- ✅ OWL components and JavaScript
- ✅ QWeb reports
- ✅ Testing and debugging
- ✅ Migration and upgrades
- ✅ Performance optimization

## Installation

### Option 1: User-Level (All Projects)

```bash
# Copy to Qoder skills directory
cp -r /home/chatcharin/qoder-odoo-skill ~/.qoder/skills/odoo-18-community
```

### Option 2: Project-Level (Current Project Only)

```bash
# Copy to project skills directory
cp -r /home/chatcharin/qoder-odoo-skill /your-odoo-project/.qoder/skills/odoo-18-community
```

## Usage

### Automatic Trigger

The skill automatically activates when you:
- Open or edit Odoo module files
- Ask about Odoo development
- Work with models, views, or controllers
- Debug Odoo errors
- Create or modify addons

### Manual Trigger

```bash
# In Qoder CLI TUI
/odoo-18-community

# Or ask directly
How do I create a new Odoo 18 module?
```

### Verify Installation

```bash
# In Qoder CLI
What skills are available?

# Or
/skills
```

## Examples

### Example 1: Create New Module

```
Create a new Odoo 18 module for managing library books with:
- Book model with title, author, ISBN, publish date
- Book category model
- Borrowing model with member reference
- Views: list, form, search
- Security: ACL and record rules
- Menu structure
```

### Example 2: Fix Error

```
I'm getting this error in Odoo 18:
AccessError: ('The requested operation cannot be completed due to security restrictions.

Please contact your system administrator.

(Document type: my.model, Operation: read)')

How do I fix this?
```

### Example 3: Add Feature

```
Add a computed field to show total amount from related lines
in my Odoo 18 module
```

### Example 4: Code Review

```
Review my Odoo 18 model code for best practices and performance issues
```

## Skill Structure

```
odoo-18-community/
├── SKILL.md              # Main skill definition
├── README.md             # This file
└── examples/             # Example modules (optional)
    └── library/          # Sample library module
```

## Key Topics Covered

### 1. Module Development
- Module structure
- Manifest configuration
- Dependencies
- Data files
- Demo data

### 2. Models & ORM
- Field types and parameters
- @api decorators
- Computed fields
- Constraints
- CRUD operations
- Search and domain
- Aggregation (read_group)

### 3. Views & XML
- List views (Odoo 18: `<list>`)
- Form views
- Search views
- Kanban views
- Actions and menus
- Dynamic attributes (Odoo 18 syntax)

### 4. Security
- Access rights (ir.model.access.csv)
- Record rules
- Field permissions
- User groups

### 5. Controllers
- HTTP endpoints
- JSON-RPC
- Route decorators
- Authentication

### 6. OWL Components
- Component structure
- Hooks (useState, useEffect)
- Services
- Templates

### 7. Reports
- QWeb templates
- PDF generation
- Paper formats
- Custom reports

### 8. Testing
- Test classes
- Test decorators
- Mocking
- Assertions

### 9. Performance
- N+1 query prevention
- Query optimization
- Caching
- Best practices

### 10. Migration
- Pre/post migration scripts
- Data migration
- Module upgrades
- Version hooks

## Odoo 18 Key Changes

| Feature | Odoo 17 | Odoo 18 |
|---------|---------|---------|
| List view | `<tree>` | `<list>` |
| Invisible | `attrs="{'invisible': [...]}"` | `invisible="..."` |
| Delete check | Override `unlink()` | `@api.ondelete()` |
| Aggregation | `group_operator=` | `aggregator=` |
| SQL | `cr.execute()` | `self.env.cr.execute()` |

## Best Practices

1. **Use Odoo 18 syntax** - `<list>` not `<tree>`
2. **Add proper security** - ACL + Record Rules
3. **Write tests** - Cover critical logic
4. **Optimize queries** - Avoid N+1
5. **Follow naming conventions** - `my.model`, `view_my_model_list`
6. **Use mixins** - `mail.thread` for messaging
7. **Handle errors** - Use proper exception types
8. **Document code** - Add docstrings
9. **Specify defaults** - `default=False` for Boolean
10. **Test before deploy** - Run tests in staging

## Common Workflows

### Creating a New Module

1. Define module structure
2. Create `__manifest__.py`
3. Define models
4. Create views
5. Add security
6. Write tests
7. Install and test

### Adding a Feature

1. Update model (fields, methods)
2. Update views (XML)
3. Update security (if needed)
4. Add tests
5. Update module
6. Verify functionality

### Fixing a Bug

1. Read error traceback
2. Identify root cause
3. Check relevant guide in skill
4. Implement fix
5. Test the fix
6. Update module

## Troubleshooting

### Skill Not Triggering

```bash
# Check installation
ls ~/.qoder/skills/odoo-18-community/SKILL.md

# Verify frontmatter
head -n 5 ~/.qoder/skills/odoo-18-community/SKILL.md
```

### Common Odoo Errors

| Error | Solution |
|-------|----------|
| AccessError | Check ir.model.access.csv |
| ValidationError | Check @api.constrains |
| RecursionError | Check infinite loops |
| QWeb Error | Check template ID |
| ImportError | Check __init__.py |

## Resources

- **Skill Documentation**: See SKILL.md for complete reference
- **Odoo 18 Official**: https://www.odoo.com/documentation/18.0/
- **Odoo 18 Developer**: https://github.com/odoo/documentation/tree/18.0
- **OWL Framework**: https://github.com/odoo/owl
- **Odoo Source**: https://github.com/odoo/odoo/tree/18.0

## Version History

- **v1.0.0** (2026-04-11): Initial release
  - Complete Odoo 18 Community coverage
  - All major topics included
  - Examples and best practices
  - Odoo 18 specific syntax

## License

MIT

## Author

Created for Qoder CLI based on Odoo 18 Community Edition development best practices.

---

**Skill Name**: odoo-18-community
**Version**: 1.0.0
**Odoo Version**: 18.0 Community
**Compatible With**: Odoo 18.0+
