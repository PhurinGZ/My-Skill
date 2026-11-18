---
name: odoo18-report
author: PhurinGZ
description: >
  Create, customize, and debug QWeb PDF Reports in Odoo 18 at any level — from basic templates
  to advanced topics. Use this skill whenever the user mentions: "create a report", "PDF report",
  "QWeb template", "ir.actions.report", "quotation PDF", "tax invoice", "Thai font in report",
  "barcode in report", "report inheritance", "custom report values", "wkhtmltopdf",
  "page break in report", "build Odoo report", or any task involving generating PDF documents
  from Odoo 18 — even if the user does not explicitly say "report".
---

# Odoo 18 QWeb PDF Report Skill

## Overview

A PDF report in Odoo 18 has four main components:

| Component | File | Purpose |
|-----------|------|---------|
| QWeb Template | `report/xxx_template.xml` | Defines document layout and content |
| Report Action | `report/xxx_report.xml` | Binds the report to a model |
| Python Model | `models/report_xxx.py` | Prepares/computes custom data (optional) |
| Paper Format | XML record | Sets paper size and margins |

PDF rendering is performed by **wkhtmltopdf** — some CSS properties are unsupported (see wkhtmltopdf Limitations).

---

## Module Structure

```
my_module/
├── report/
│   ├── my_report.xml           # ir.actions.report declaration
│   └── my_report_template.xml  # QWeb template
├── models/
│   └── report_my_report.py     # custom values (optional)
├── security/
│   └── ir.model.access.csv
└── __manifest__.py
```

In `__manifest__.py`:
```python
'data': [
    'report/my_report.xml',
    'report/my_report_template.xml',
],
```

---

## 1. Report Action (ir.actions.report)

```xml
<record id="action_report_my_document" model="ir.actions.report">
    <field name="name">My Document</field>
    <field name="model">sale.order</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">my_module.report_my_document</field>
    <field name="report_file">my_module.report_my_document</field>
    <field name="binding_model_id" ref="sale.model_sale_order"/>
    <field name="binding_type">report</field>
    <field name="paperformat_id" ref="my_module.paperformat_custom"/>  <!-- optional -->
</record>
```

**Key fields:**
- `report_type`: `qweb-pdf` | `qweb-html` | `qweb-text`
- `report_name`: must match the template `id` — format is `module.template_id`
- `binding_model_id`: automatically adds report to the Print menu of that model
- `binding_type`: `report` = bound to record, `action` = triggered from action

---

## 2. Basic QWeb Template

```xml
<template id="report_my_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2 t-field="o.name"/>

                    <div class="row">
                        <div class="col-6">
                            <strong>Customer:</strong>
                            <span t-field="o.partner_id"/>
                        </div>
                        <div class="col-6">
                            <strong>Date:</strong>
                            <span t-field="o.date_order" t-options='{"widget": "date"}'/>
                        </div>
                    </div>

                    <table class="table table-sm o_main_table">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th class="text-right">Qty</th>
                                <th class="text-right">Unit Price</th>
                                <th class="text-right">Subtotal</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr t-foreach="o.order_line" t-as="line">
                                <td><span t-field="line.product_id"/></td>
                                <td class="text-right"><span t-field="line.product_uom_qty"/></td>
                                <td class="text-right"><span t-field="line.price_unit"/></td>
                                <td class="text-right"><span t-field="line.price_subtotal"/></td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr>
                                <td colspan="3" class="text-right"><strong>Total</strong></td>
                                <td class="text-right">
                                    <span t-field="o.amount_total"/>
                                </td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </t>
        </t>
    </t>
</template>
```

**Notes:**
- `web.external_layout` = includes company header, footer, logo, and page numbers automatically
- `web.internal_layout` = no company header
- `<div class="page">` = required wrapper for page content

---

## 3. QWeb Syntax Reference

### Rendering field values
```xml
<span t-field="o.name"/>                          <!-- widget rendering — recommended -->
<span t-esc="o.name"/>                            <!-- plain text, HTML-escaped -->
<span t-raw="o.description_html"/>                <!-- raw HTML output — use with caution (XSS risk) -->
```

### Field widgets (t-options)
```xml
<span t-field="o.date_order" t-options='{"widget": "date"}'/>
<span t-field="o.amount_total" t-options='{"widget": "monetary", "display_currency": o.currency_id}'/>
<span t-field="o.partner_id" t-options='{"widget": "contact", "fields": ["name", "address"]}'/>
<div t-field="o.description" t-options='{"widget": "html"}'/>
```

### Loop (t-foreach)
```xml
<t t-foreach="o.order_line" t-as="line">
    <!-- Available loop variables: line_index, line_size, line_first, line_last, line_parity -->
    <tr t-att-class="'bg-light' if line_index % 2 == 0 else ''">
        <td t-esc="line_index + 1"/>
    </tr>
</t>
```

### Conditionals
```xml
<t t-if="o.amount_total > 10000">
    <p class="text-danger">VIP Customer</p>
</t>
<t t-elif="o.amount_total > 5000">
    <p>Standard</p>
</t>
<t t-else="">
    <p>Regular</p>
</t>
```

### Variables
```xml
<t t-set="tax_amount" t-value="o.amount_total - o.amount_untaxed"/>
<span t-esc="tax_amount"/>
```

### Dynamic attributes
```xml
<div t-att-class="'highlight' if o.state == 'done' else 'normal'"/>
<img t-att-src="'/web/image/res.partner/%s/image_128' % o.partner_id.id"/>
```

### Calling a sub-template
```xml
<t t-call="my_module.report_my_subtemplate">
    <t t-set="my_var" t-value="some_value"/>
</t>
```

---

## 4. Template Context Variables

These variables are available in every report template by default:

| Variable | Type | Description |
|----------|------|-------------|
| `docs` | recordset | Records being printed |
| `doc_ids` | list[int] | IDs of the records |
| `doc_model` | str | Model name string |
| `time` | module | Python `time` module |
| `user` | res.users | User who triggered the print |
| `res_company` | res.company | Company of the current user |
| `website` | ir.website | Website record (if applicable) |

---

## 5. CSS for PDF (wkhtmltopdf)

Commonly used inline CSS:
```css
/* Force new page before element */
.page-break { page-break-before: always; }

/* Prevent element from splitting across pages */
.no-break { page-break-inside: avoid; }

/* Standard bordered table */
.table { width: 100%; border-collapse: collapse; }
.table td, .table th { border: 1px solid #dee2e6; padding: 4px 8px; }

/* Alignment */
.text-right { text-align: right; }
.text-center { text-align: center; }
```

### wkhtmltopdf Limitations

| Feature | Status | Alternative |
|---------|--------|-------------|
| Flexbox | ❌ Unreliable | Use `table` or `float` |
| CSS Grid | ❌ Not supported | Use `table` layout |
| JavaScript | ❌ Does not run | N/A |
| `position: fixed` | ❌ Avoid | Use wkhtmltopdf header/footer |
| Bootstrap 3 classes | ✅ Supported | Bundled by Odoo |
| FontAwesome icons | ✅ Supported | Bundled by Odoo |
| `page-break-*` CSS | ✅ Supported | — |

---

## 6. Paper Format

```xml
<record id="paperformat_a4_custom" model="report.paperformat">
    <field name="name">A4 Custom</field>
    <field name="format">A4</field>
    <field name="orientation">Portrait</field>  <!-- Portrait | Landscape -->
    <field name="margin_top">20</field>          <!-- in mm -->
    <field name="margin_bottom">20</field>
    <field name="margin_left">10</field>
    <field name="margin_right">10</field>
    <field name="header_line">False</field>
    <field name="header_spacing">10</field>
</record>
```

Link to a report via `paperformat_id` in the report action, or set globally under Settings > Technical > Reports.

---

## 7. Custom Python Report Values

Use when: special calculations, data from other models, grouping, subtotals.

```python
# models/report_my_report.py
from odoo import models, api

class ReportMyDocument(models.AbstractModel):
    _name = 'report.my_module.report_my_document'
    _description = 'My Document Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)

        # Group lines by product category
        report_lines = []
        for doc in docs:
            lines_by_category = {}
            for line in doc.order_line:
                cat = line.product_id.categ_id.name
                lines_by_category.setdefault(cat, []).append(line)
            report_lines.append({
                'doc': doc,
                'grouped_lines': lines_by_category,
            })

        return {
            'docs': docs,
            'report_lines': report_lines,
            'company': self.env.company,
        }
```

In the template:
```xml
<t t-foreach="report_lines" t-as="report">
    <t t-set="o" t-value="report['doc']"/>
    <t t-foreach="report['grouped_lines'].items()" t-as="category_data">
        <h4 t-esc="category_data[0]"/>
        <!-- render lines here -->
    </t>
</t>
```

---

## 8. Report Inheritance / Override

### Extend an existing template (e.g. invoice)
```xml
<template id="report_invoice_custom" inherit_id="account.report_invoice_document">
    <!-- Add a new field after an existing element -->
    <xpath expr="//div[@name='payment_term']" position="after">
        <div t-if="o.note">
            <strong>Note:</strong>
            <span t-field="o.note"/>
        </div>
    </xpath>

    <!-- Replace an element -->
    <xpath expr="//span[@name='invoice_origin']" position="replace">
        <span t-field="o.invoice_origin"/> / <span t-field="o.ref"/>
    </xpath>

    <!-- Inject custom CSS -->
    <xpath expr="//div[@class='page']" position="inside">
        <style>
            .custom-header { background: #f5f5f5; }
        </style>
    </xpath>
</template>
```

### XPath position values

| Position | Effect |
|----------|--------|
| `before` | Insert before the matched node |
| `after` | Insert after the matched node |
| `inside` | Append inside the matched node |
| `replace` | Replace the matched node entirely |
| `attributes` | Modify attributes of the matched node |

### Override a report action (e.g. change paper format)
```xml
<record id="account.action_report_account_invoice" model="ir.actions.report">
    <field name="paperformat_id" ref="my_module.paperformat_a4_custom"/>
</record>
```

---

## 9. Barcode and QR Code

```xml
<!-- QR Code -->
<img t-att-src="'/report/barcode/QR/%s' % o.name" style="width:80px;height:80px;"/>

<!-- Code128 barcode -->
<img t-att-src="'/report/barcode/Code128/%s' % o.name" style="height:50px;"/>

<!-- QR Code with full parameters -->
<img t-att-src="'/report/barcode/?barcode_type=%s&amp;value=%s&amp;width=%s&amp;height=%s' % ('QR', o.name, 200, 200)"/>

<!-- Base64 image (e.g. PromptPay QR generated in Python) -->
<img t-att-src="'data:image/png;base64,%s' % o._get_promptpay_qr()"/>
```

Supported barcode types: `QR`, `Code128`, `Code39`, `EAN13`, `EAN8`, `Aztec`, `DataMatrix`

---

## 10. Thai Language / Custom Fonts in PDF

### Add font via CSS in template
```xml
<style>
    * {
        font-family: 'THSarabunNew', 'Garuda', 'Norasi', sans-serif !important;
    }
</style>
```

### Install font on server (Ubuntu/Debian)
```bash
# Install Thai font package
apt-get install -y fonts-thai-tlwg

# Or manually copy a font file
cp THSarabunNew.ttf /usr/share/fonts/truetype/
fc-cache -f -v
```

### Bundle font inside the module
In `__manifest__.py`:
```python
'assets': {
    'web.report_assets_common': [
        'my_module/static/fonts/THSarabunNew.ttf',
        'my_module/static/css/report_fonts.css',
    ],
},
```

`report_fonts.css`:
```css
@font-face {
    font-family: 'THSarabunNew';
    src: url('/my_module/static/fonts/THSarabunNew.ttf') format('truetype');
}
body, * {
    font-family: 'THSarabunNew', sans-serif;
}
```

---

## 11. Multi-language / Translation

Requires two templates: a wrapper (sets language) and the translatable body.

```xml
<!-- Main template: sets the language per partner -->
<template id="report_my_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="o">
            <t t-call="my_module.report_my_document_lang"
               t-lang="o.partner_id.lang"/>
        </t>
    </t>
</template>

<!-- Translatable template body -->
<template id="report_my_document_lang">
    <t t-call="web.external_layout">
        <div class="page">
            <!-- Re-browse record in the correct language context -->
            <t t-set="o" t-value="o.with_context(lang=o.partner_id.lang)"/>
            <h2 t-field="o.name"/>
            <!-- content here will render in partner's language -->
        </div>
    </t>
</template>
```

**Important:** Re-browsing via `with_context(lang=...)` is required when using translatable field values (e.g. country names, product names with translations). Skip it only if no translatable fields are used — it has a performance cost.

---

## 12. Debugging Reports

```bash
# View as HTML (much easier to inspect than PDF)
http://localhost:8069/report/html/my_module.report_my_document/1

# View as PDF
http://localhost:8069/report/pdf/my_module.report_my_document/1

# Enable developer mode
http://localhost:8069/web?debug=1
```

In developer mode: Settings > Technical > Reports — select a report to edit its template directly in the UI without restarting the server.

---

## 13. Trigger Report from Python (Button)

```python
def action_print_report(self):
    return self.env.ref('my_module.action_report_my_document').report_action(self)

# With extra data passed to the template
def action_print_report(self):
    data = {'custom_key': 'value'}
    return self.env.ref('my_module.action_report_my_document').report_action(self, data=data)
```

---

## 14. Images in Reports

```xml
<!-- Company logo (base64) -->
<img t-if="o.company_id.logo"
     t-att-src="'data:image/png;base64,%s' % o.company_id.logo.decode('utf-8')"
     style="max-height:50px;"/>

<!-- Partner image via URL -->
<img t-att-src="'/web/image/res.partner/%s/image_128' % o.partner_id.id"
     style="width:60px;height:60px;object-fit:cover;"/>

<!-- Static asset from module -->
<img src="/my_module/static/img/logo.png" style="height:40px;"/>
```

---

## 15. Filtered Report Preview Page (HTML)

Use a custom HTTP controller to render a report preview page with a filter bar at the top and the report at the bottom.

### 15.1 Controller (`controllers/report_preview_controller.py`)

```python
from odoo import http
from odoo.http import request


class ReportPreviewController(http.Controller):

    @http.route('/my_module/report_preview', type='http', auth='user', website=False)
    def report_preview(self, **kw):
        domain = [('state', '!=', 'cancel')]

        if kw.get('partner_id'):
            domain.append(('partner_id', '=', int(kw['partner_id'])))
        if kw.get('date_from'):
            domain.append(('date_order', '>=', kw['date_from']))
        if kw.get('date_to'):
            domain.append(('date_order', '<=', kw['date_to']))

        records = request.env['sale.order'].search(domain)
        html = request.env['ir.actions.report']._render_qweb_html(
            'my_module.report_my_document',
            records.ids,
            data={},
        )[0]

        return request.render('my_module.report_preview_page', {
            'records': records,
            'filters': kw,
            'report_html': html.decode('utf-8') if isinstance(html, bytes) else html,
        })
```

**Important:** In Odoo 18, `_render_qweb_html(report_ref, docids, data={})` requires `docids` as the second positional argument.

### 15.2 QWeb Template (`views/report_preview_templates.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_preview_page" name="Report Preview Page">
        <t t-call="web.html_container">
            <html>
                <head>
                    <title>Report Preview</title>
                    <link rel="stylesheet" href="/web/static/lib/bootstrap/css/bootstrap.min.css"/>
                    <style>
                        .filter-box { background: #fff; padding: 20px; margin-bottom: 20px; border: 1px solid #ddd; border-radius: 8px; }
                        .report-box { background: #fff; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
                        @media print { .filter-box, .btn { display: none !important; } }
                    </style>
                </head>
                <body>
                    <div class="container-fluid">
                        <div class="filter-box">
                            <form method="GET" action="/my_module/report_preview" class="row g-3">
                                <div class="col-md-3">
                                    <label>Customer</label>
                                    <select name="partner_id" class="form-select">
                                        <option value="">All</option>
                                        <t t-foreach="partners" t-as="partner">
                                            <option t-att-value="partner.id"
                                                    t-att-selected="str(partner.id) == filters.get('partner_id', '')">
                                                <t t-esc="partner.name"/>
                                            </option>
                                        </t>
                                    </select>
                                </div>
                                <div class="col-md-12">
                                    <button type="submit" class="btn btn-primary">Preview</button>
                                    <button type="button" class="btn btn-success" onclick="window.print()">Print</button>
                                </div>
                            </form>
                        </div>
                        <div class="report-box">
                            <t t-if="not records">
                                <div class="text-center text-muted">No records found.</div>
                            </t>
                            <t t-else="">
                                <div t-raw="report_html"/>
                            </t>
                        </div>
                    </div>
                </body>
            </html>
        </t>
    </template>
</odoo>
```

### 15.3 Open Preview from a Button

```python
# models/sale_order.py
def action_preview_report_page(self):
    self.ensure_one()
    return {
        'type': 'ir.actions.act_url',
        'url': f'/my_module/report_preview?partner_id={self.partner_id.id}',
        'target': 'new',
    }
```

```xml
<!-- views/sale_order_views.xml -->
<button name="action_preview_report_page"
        type="object"
        class="oe_stat_button"
        icon="fa-search">
    <span class="o_stat_text">Preview</span>
</button>
```

---

## 16. Common Pitfalls and Solutions

| Problem | Cause | Fix |
|---------|-------|-----|
| PDF layout broken / unexpected gaps | Flexbox unsupported in wkhtmltopdf | Use `table` or `float` layout |
| Thai / special characters not showing | Font not installed on server | Install font + set `font-family` in CSS |
| Numbers formatted incorrectly | Missing widget | Use `t-options='{"widget": "monetary"}'` |
| Table splits across pages mid-row | Default browser behavior | Add `page-break-inside: avoid` to table/tr |
| Image not displaying | Wrong URL path | Use `/web/image/model/id/field` pattern |
| Template not found after change | Module not updated | Run `--update=my_module` or upgrade in UI |
| Report missing from Print menu | Missing `binding_model_id` | Add `binding_model_id` to the report action |
| `_render_qweb_html()` error in Odoo 18 | Wrong argument signature | Use `_render_qweb_html(report_ref, docids, data={})` |

---

## Reference Files

Read these when needed — do not load unless the task specifically requires them:

- `references/qweb-cheatsheet.md` — compact QWeb syntax reference with all directives and loop variables
- `references/thai-invoice-template.xml` — complete Thai tax invoice template ready to adapt
- `references/filtered-report-preview.xml` — QWeb template for a filtered HTML report preview page
- `references/filtered-report-preview-controller.py` — HTTP controller for the filtered preview page

**Official documentation:**
- Reference: https://www.odoo.com/documentation/18.0/developer/reference/backend/reports.html
- Tutorial: https://www.odoo.com/documentation/18.0/developer/tutorials/pdf_reports.html
