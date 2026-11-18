# Odoo 18 References - Complete Index

This directory contains comprehensive guides for Odoo 18 Community Edition development.

## Available Guides

### ✅ Local Guides (Created)

1. [Model Methods & ORM Guide](odoo-18-model-guide.md) - **638 lines**
   - CRUD operations, search, domain, RecordSets
   - Computed fields, constraints, related fields
   - Aggregation, inheritance patterns

2. [Field Types Guide](odoo-18-field-guide.md) - **499 lines**
   - All field types (Char, Integer, Float, Boolean, Date, etc.)
   - Relational fields (Many2one, One2many, Many2many)
   - Special fields (Selection, Monetary, Binary, Image, etc.)
   - Odoo 18 changes (aggregator, Boolean defaults)

3. [API Decorators Guide](odoo-18-decorator-guide.md) - **374 lines**
   - @api.model, @api.depends, @api.constrains
   - @api.onchange, @api.ondelete (Odoo 18)
   - Method patterns and best practices

4. [Security Guide](odoo-18-security-guide.md) - **263 lines**
   - Access Control Lists (ACL)
   - Record Rules
   - User Groups
   - Field level security

### 📖 External Guides (Original Repository)

For detailed guides on the following topics, please refer to the original repository:

5. [Actions Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-actions-guide.md)
   - Window actions, server actions, scheduled jobs
   - URL actions, client actions

6. [Controller Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-controller-guide.md)
   - HTTP routes, request handling
   - JSON-RPC, authentication
   - File uploads, downloads

7. [Data Files Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-data-guide.md)
   - XML data files, CSV imports
   - Record creation, field updates
   - Many2many commands, noupdate flag

8. [Development Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-development-guide.md)
   - Complete module structure
   - Manifest configuration
   - Module lifecycle, hooks

9. [Manifest Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-manifest-guide.md)
   - __manifest__.py configuration
   - Dependencies, data files
   - Install/upgrade hooks

10. [Migration Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-migration-guide.md)
    - Module migration patterns
    - Data migration scripts
    - Version upgrade strategies

11. [Mixins Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-mixins-guide.md)
    - mail.thread, mail.activity.mixin
    - Email aliases, message posting
    - Activity management

12. [OWL Components Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-owl-guide.md)
    - Component creation, hooks
    - State management, services
    - Event handling

13. [Performance Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-performance-guide.md)
    - Query optimization
    - Preventing N+1 queries
    - Caching strategies

14. [Reports Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-reports-guide.md)
    - QWeb report templates
    - PDF generation
    - Paper formats, custom reports

15. [Testing Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-testing-guide.md)
    - Test cases, test suites
    - TransactionCase, SavepointCase
    - Mocking, assertions

16. [Transaction Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-transaction-guide.md)
    - Transaction management
    - Savepoints, UniqueViolation
    - Error handling

17. [Translation Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-translation-guide.md)
    - Translation workflow
    - PO files, localization
    - Multi-language support

18. [Views & XML Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-view-guide.md)
    - Form, list, search views
    - Actions, menus
    - QWeb templates, Odoo 18 syntax

## Quick Reference

### Most Used Guides
1. **Model Methods** - Local ✅
2. **Field Types** - Local ✅
3. **API Decorators** - Local ✅
4. **Security** - Local ✅
5. **Views & XML** - [External](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-view-guide.md)

### For Module Creation
- [Development Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-development-guide.md)
- [Manifest Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-manifest-guide.md)
- [Security Guide](odoo-18-security-guide.md) - Local ✅

### For Views
- [Views & XML Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-view-guide.md)
- [Actions Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-actions-guide.md)
- [Data Files Guide](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-data-guide.md)

### For Advanced Topics
- [OWL Components](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-owl-guide.md)
- [Performance](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-performance-guide.md)
- [Testing](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-testing-guide.md)
- [Migration](https://github.com/unclecatvn/agent-skills/blob/main/skills/odoo-18.0/references/odoo-18-migration-guide.md)

## Usage

When working on Odoo 18 development:

1. **Check local guides first** - They cover the most common tasks
2. **Reference external guides** - For detailed information on specific topics
3. **Use EXAMPLES.md** - For complete working examples
4. **Check SKILL.md** - For quick reference and best practices

---

**Note**: Local guides are optimized for quick reference. External guides contain more comprehensive examples and edge cases.

**Original Repository**: [unclecatvn/agent-skills](https://github.com/unclecatvn/agent-skills/tree/main/skills/odoo-18.0)
