---
name: odoo-cogmenu-export
author: PhurinGZ
description: Add custom export/download actions to the Odoo 17 cog menu and handle binary file downloads reliably from dropdown contexts.
---

You are an Odoo 17 frontend/backend developer who knows how to extend the cog menu (a.k.a. "Actions" dropdown) and deliver binary files from it without silent failures.

## When to Use This Skill

Use this skill when:
- Adding a custom button to the cog menu (gear icon) in list/kanban/form views
- The button must trigger a file download (Excel, PDF, CSV, etc.)
- `ir.actions.act_url` or `window.open` works from a form-view button but **fails silently** inside a `DropdownItem`

---

## The Problem

In Odoo 17 the cog menu uses `DropdownItem`, whose `onSelected` handler is **synchronous**. As soon as the user clicks:

1. The dropdown closes.
2. The `CogMenu` component unmounts.
3. Any async chain (`async onSelected → orm.call → window.open/fetch/actionService.doAction`) is **cut off** or treated as a non-user-initiated navigation, so the browser blocks the download/popup.

Symptom: the server creates the attachment (you see the log), but the browser never starts the download.

---

## The Solution

For **downloads**, never use an async `onSelected` handler. Instead:

1. Expose an HTTP controller that generates the file and returns it with `Content-Disposition: attachment`.
2. In the cog menu template, render a plain `<a>` element with `t-att-href` pointing to that controller URL.
3. The browser treats the click as a direct user-initiated navigation, so the download always works.

---

## Step-by-Step Implementation

### 1. Extract the file-generation logic on the model

Keep the existing `action_export_project` for form-view buttons, but split the actual generation so the controller can reuse it.

```python
# models/my_model.py

def _generate_export_xlsx(self):
    """Return (filename_bytes_str, file_bytes)."""
    self.ensure_one()
    # ... build workbook with openpyxl or any library ...
    bio = io.BytesIO()
    workbook.save(bio)
    bio.seek(0)
    data = bio.read()
    filename = f"{self.name}_export.xlsx"
    return filename, data

def action_export_project(self):
    """Called by form-view buttons; returns an Odoo action dict."""
    self.ensure_one()
    filename, data = self._generate_export_xlsx()
    attachment = self.env["ir.attachment"].create({
        "name": filename,
        "datas": base64.b64encode(data),
        "type": "binary",
    })
    return {
        "type": "ir.actions.act_url",
        "url": f"/web/content/{attachment.id}?download=true",
        "target": "new",
    }
```

### 2. Add an HTTP controller for direct download

```python
# controllers/main.py
from odoo import http
from odoo.http import request, content_disposition


class MyExportController(http.Controller):
    @http.route("/my_module/export/<int:record_id>", type="http", auth="user")
    def export_record(self, record_id, **kw):
        record = request.env["my.model"].browse(record_id)
        if not record.exists():
            return request.not_found()

        filename, data = record._generate_export_xlsx()
        if not data:
            return request.not_found()

        return request.make_response(
            data,
            headers=[
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                ("Content-Disposition", content_disposition(filename)),
            ],
        )
```

Don’t forget to import the controllers package in `__init__.py`:

```python
from . import controllers
```

### 3. Register the cog menu JS component

```javascript
// static/src/js/cog_menu.js
/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;

const cogMenuRegistry = registry.category("cogMenu");

export class MyCogMenu extends Component {
    setup() {
        this.actionService = useService("action");
    }

    // For IMPORT / WIZARD actions (non-download), DropdownItem is fine
    async actionImportSomething() {
        await this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Import Something",
            res_model: "my.import.wizard",
            view_mode: "form",
            views: [[false, "form"]],
            target: "new",
        });
    }

    // Eager getter used by the <a> tag — no async
    get exportUrl() {
        const resId = this.resId;
        return resId ? `/my_module/export/${resId}` : "#";
    }

    get resModel() {
        return (
            this.env.searchModel?.resModel ||
            this.env.model?.root?.resModel ||
            this.env.model?.resModel ||
            this.props?.resModel ||
            this.props?.config?.resModel
        );
    }

    get resId() {
        const direct = (
            this.env.model?.root?.resId ||
            this.env.model?.root?.data?.id ||
            this.env.model?.resId ||
            this.props?.resId ||
            this.props?.config?.resId
        );
        if (direct) return direct;
        try {
            const hash = window.location.hash || "";
            const params = new URLSearchParams(hash.startsWith("#") ? hash.slice(1) : hash);
            const idStr = params.get("id");
            if (idStr) {
                const parsed = parseInt(idStr, 10);
                return Number.isNaN(parsed) ? undefined : parsed;
            }
        } catch (e) {}
        return undefined;
    }
}

MyCogMenu.template = "my_module.cog_menu";
MyCogMenu.components = { DropdownItem };

cogMenuRegistry.add("my-module-cog-menu", {
    Component: MyCogMenu,
    groupNumber: 20,
    isDisplayed: ({ config }) => true,
}, { sequence: 10 });
```

### 4. Template — use `<a>` for downloads, `<DropdownItem>` for everything else

```xml
<!-- static/src/xml/cog_menu.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="my_module.cog_menu" owl="1">
        <!-- EXPORT: plain <a> so the browser handles it as direct navigation -->
        <a class="dropdown-item o_cog_menu"
           t-if="resModel === 'my.model' &amp;&amp; resId"
           t-att-href="exportUrl"
           target="_blank">
            <i class="fa fa-file-excel-o me-1"/> Export
        </a>

        <!-- IMPORT: DropdownItem with async onSelected is OK here -->
        <DropdownItem class="'o_cog_menu'"
                      t-if="resModel === 'my.model'"
                      onSelected.bind="actionImportSomething">
            <i class="fa fa-download me-1"/> Import
        </DropdownItem>
    </t>
</templates>
```

---

## Rules of Thumb

| Action type | Cog-menu element | Why |
|-------------|------------------|-----|
| Open wizard / form view | `<DropdownItem onSelected.bind="...">` | `actionService.doAction` works fine synchronously |
| Download binary file | `<a t-att-href="...">` | Browser treats it as direct user navigation; no popup-blocker or unmount issue |
| Hybrid (generate then download) | HTTP controller + `<a>` | Keep generation server-side, let the browser fetch the bytes directly |

---

## Constraints

- Do NOT use `window.open`, `fetch`, or `actionService.doAction` inside an async `DropdownItem` handler for downloads.
- Do NOT forget `auth="user"` on the controller route; otherwise unauthenticated users may access it.
- Do NOT forget `from . import controllers` in `__init__.py` or the route will not be registered.

---

## Output Expectations

- A working cog-menu button that downloads files reliably.
- Reusable `_generate_*` model methods so both buttons and controllers can share logic.
- Clear separation: `<a>` for downloads, `<DropdownItem>` for wizard/form actions.
