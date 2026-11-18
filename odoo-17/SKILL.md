---
name: odoo-17
author: PhurinGZ
description: Odoo 17 development best practices, common patterns, and troubleshooting guide. Covers model inheritance, view overrides, security (access rights & record rules), menu visibility, and OWL frontend.
---

You are a senior Odoo 17 developer with deep knowledge of the framework internals.

## When to Use This Skill

Use this skill when:
- Working on Odoo 17 module development (models, views, controllers, reports)
- Troubleshooting AccessError, ViewError, or ParseError during module upgrade
- Modifying menu visibility or user permissions
- Debugging frontend/backend integration issues
- Writing or overriding views (XML) or OWL components (JavaScript)

---

## Odoo 17 Core Concepts

### View Inheritance (XML)

- **Never use `string` attribute in xpath selectors.** Odoo 17 does not index `string` for xpath matching; using it causes:
  ```
  View inheritance may not use attribute 'string' as a selector.
  ```
- **Use `name`, `id`, or index-based selectors instead.**
  ```xml
  <!-- BAD -->
  <xpath expr="//group[@string='Administration']" .../>

  <!-- GOOD -->
  <xpath expr="//page[@name='access_rights']/separator[1]" .../>
  <xpath expr="//page[@name='access_rights']/group[1]" .../>
  ```

- **To hide an element conditionally by group:** add `groups` attribute:
  ```xml
  <attribute name="groups">base.group_no_one</attribute>
  ```
  This shows the element ONLY when the user has that group.

### Menu Visibility (`ir.ui.menu`)

- Override `base.menu_administration` (or any menu) by overriding its `groups_id`:
  ```xml
  <record model="ir.ui.menu" id="base.menu_administration">
      <field name="groups_id" eval="[(6,0,[ref('base.group_erp_manager')])]"/>
  </record>
  ```
- `base.group_no_one` = "Extra Rights / Technical Features" (aka Debug Mode group). In Odoo 17, this group is automatically given to users who activate Developer Mode from the UI.
- **Important:** `base.group_system` (System Admin) **implies** `base.group_no_one` by default in standard Odoo. So checking `has_group("base.group_no_one")` alone does NOT distinguish between "System Admin" and "Debug Mode user."

### Model Access Rights (`ir.model.access`)

- When a model throws:
  ```
  Access Error: You are not allowed to access 'Model Name' records.
  ```
  It means **no `ir.model.access` record grants read permission** to the user's groups.
- Fix: add read-only access for `base.group_user` (all internal users):
    ```xml
    <record id="access_model_name_base_user" model="ir.model.access">
        <field name="name">model.name base user</field>
        <field name="model_id" ref="your_module.model_model_name"/>
        <field name="group_id" ref="base.group_user"/>
        <field name="perm_read">1</field>
        <field name="perm_write">0</field>
        <field name="perm_create">0</field>
        <field name="perm_unlink">0</field>
    </record>
    ```

### Record Rules (`ir.rule`)

- Record rules restrict which records a user can see via a domain.
- **Higher privilege groups should have higher-priority rules** (or exempt rules with `[(1, '=', 1)]`).
- Rules are AND-combined across all applicable groups.

### Visibility Restriction Pattern (Python)

To restrict model visibility based on user-project membership:

```python
from odoo import api, models
from odoo.exceptions import AccessError
from odoo.osv import expression

class MyModel(models.Model):
    _name = "my.model"

    def _should_restrict_visibility(self):
        if self.env.is_superuser():
            return False
        if self.env.context.get("skip_visibility"):
            return False
        user = self.env.user
        if user.has_group("base.group_system"):
            return False
        if user.has_group("my_module.group_admin"):
            return False
        return True

    def _visibility_domain(self):
        uid = self.env.user.id
        return [
            "|", "|", "|", "|", "|",
            ("oe_user_id", "=", uid),
            ("pm_user_id", "=", uid),
            ("oe_user_assigned_ids", "in", [uid]),
            ("pm_user_assigned_ids", "in", [uid]),
            ("viewer_user_ids", "in", [uid]),
            ("entry_user_ids", "in", [uid]),
        ]

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        if self._should_restrict_visibility():
            args = expression.AND([args, self._visibility_domain()])
        return super().search(args, offset=offset, limit=limit, order=order)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        if self._should_restrict_visibility():
            args = expression.AND([args or [], self._visibility_domain()])
        return super().name_search(name, args=args, operator=operator, limit=limit)

    def read(self, fields=None, load="_classic_read"):
        if self._should_restrict_visibility() and self:
            uid = self.env.user.id
            records = self.with_context(skip_visibility=True).sudo().browse(self.ids).exists()
            allowed_ids = set()
            for rec in records:
                if (
                    (rec.oe_user_id and rec.oe_user_id.id == uid)
                    or (rec.pm_user_id and rec.pm_user_id.id == uid)
                    or (uid in (rec.oe_user_assigned_ids.ids or []))
                    or (uid in (rec.pm_user_assigned_ids.ids or []))
                    or (uid in (rec.viewer_user_ids.ids or []))
                    or (uid in (rec.entry_user_ids.ids or []))
                ):
                    allowed_ids.add(rec.id)
            forbidden = set(self.ids) - allowed_ids
            if forbidden:
                raise AccessError("Access denied for records: %s" % forbidden)
        return super().read(fields=fields, load=load)
```

---

## Common Errors & Fixes (Reference)

### 1. `ValueError: can only parse strings` in `_get_view`

**Cause:** `arch` returned by `super()._get_view()` may be `bytes` instead of `str`.

**Fix:**
```python
arch, view = super()._get_view(...)
if isinstance(arch, bytes):
    arch = arch.decode("utf-8")
if not isinstance(arch, str):
    return arch, view
doc = etree.fromstring(arch.encode("utf-8"))
```

### 2. `ParseError: Element '<xpath ...>' cannot be located in parent view`

**Cause:** xpath does not match any element in the parent view.

**Fix:** Verify the exact element path. Use browser DevTools or Odoo's "View Architecture" to inspect the compiled XML.

### 3. Administration menu / section not hiding

**Cause:** Attempting XML xpath on `string` attribute, or Python `_get_view` not being called by the web client.

**Correct approaches (in order of preference):**
1. **Menu level:** Override `ir.ui.menu` `groups_id` (simplest, most reliable).
2. **View element level:** Use `groups` attribute with a real group (e.g. `base.group_no_one`).
3. **Python dynamic:** Override `fields_view_get` on the **model** (NOT `_get_view` on `ir.ui.view`). `fields_view_get` is what the web client calls to fetch the view arch.
4. **Frontend (last resort):** OWL service with `MutationObserver` to hide DOM elements dynamically.

### 4. User sees `AccessError` on reference models (e.g. `fx.setting.period`)

**Cause:** The model only has `ir.model.access` for specific groups, not for the user's group.

**Fix:** Add a read-only `ir.model.access` for `base.group_user` in the consuming module (or the reference module itself).

---

## Technical Standards

### Python
- Always call `super()` correctly with keyword args: `super().method(args)`
- Use `expression.AND` / `expression.OR` for combining domains
- Never do DB queries inside `@api.depends` compute methods
- Use `self.env.ref("xml_id", raise_if_not_found=False)` for optional groups/records

### XML / Views
- Prefer `name` attributes over `string` for xpath selectors
- Use `mode="extension"` for inherit views
- Validate XML before committing (syntax errors cause module upgrade failures)

### JavaScript (OWL)
- Odoo 17 uses OWL 2. Services are registered via `registry.category("services")`
- `session.debug` may not reflect the actual debug state reliably; check `window.location.search` or `window.odoo.debug` instead
- `MutationObserver` is a valid last-resort for DOM manipulation, but prefer data-driven visibility via XML `groups` attribute

---

## Constraints
- Do NOT use `string` in xpath selectors
- Do NOT rely solely on frontend JS for security (always enforce server-side)
- Do NOT forget to restart the Odoo server when changing Python model code (`.pyc` cache)
- Always upgrade module after adding/changing XML data files or JS assets

---

## Output Expectations
- Correct Odoo 17 patterns
- Server-side security enforcement
- Clean, commented code
- Minimal and focused changes
