# QWeb Cheatsheet — Odoo 18 Report

## Core Directives

| Directive | Usage |
|-----------|-------|
| `t-field="o.name"` | Render field value through widget (recommended) |
| `t-esc="o.name"` | Plain text output, HTML-escaped |
| `t-raw="o.html"` | Raw HTML output — XSS risk, use carefully |
| `t-if / t-elif / t-else` | Conditional rendering |
| `t-foreach="list" t-as="item"` | Loop over a collection |
| `t-set="var" t-value="expr"` | Set a local variable |
| `t-call="module.template_id"` | Call a sub-template |
| `t-att-href="expr"` | Dynamic HTML attribute |
| `t-lang="o.partner_id.lang"` | Set rendering language for translation |
| `t-out="expr"` | Alias for t-esc (Odoo 16+) |

## Loop Variables

When using `t-foreach="items" t-as="item"`:

| Variable | Value |
|----------|-------|
| `item_index` | Zero-based index of current item |
| `item_size` | Total number of items |
| `item_first` | True if this is the first item |
| `item_last` | True if this is the last item |
| `item_parity` | `"even"` or `"odd"` |
| `item_value` | The current item (same as `item`) |

## t-field Widgets

```xml
<!-- Date / Datetime -->
<span t-field="o.date" t-options='{"widget": "date"}'/>
<span t-field="o.datetime" t-options='{"widget": "datetime"}'/>

<!-- Monetary amount with currency -->
<span t-field="o.amount" t-options='{"widget": "monetary", "display_currency": o.currency_id}'/>

<!-- Partner address block -->
<span t-field="o.partner_id" t-options='{"widget": "contact", "fields": ["name", "address", "city"]}'/>

<!-- Rich text / HTML field -->
<div t-field="o.description" t-options='{"widget": "html"}'/>

<!-- Image field -->
<img t-field="o.image" t-options='{"widget": "image", "width": 64, "height": 64}'/>
```

## Layout Templates

```xml
<!-- Standard layout: includes company header, footer, logo, page numbers -->
<t t-call="web.external_layout">...</t>

<!-- Minimal layout: no company branding -->
<t t-call="web.internal_layout">...</t>

<!-- Required outer wrapper for all reports -->
<t t-call="web.html_container">...</t>
```

## Bootstrap Classes Commonly Used in Reports

```
Tables:     .table  .table-sm  .table-bordered  .table-striped
Grid:       .row  .col-6  .col-4  .col-3  .col-2
Text:       .text-right  .text-left  .text-center  .text-muted
Weight:     .font-weight-bold
Borders:    .border  .border-top  .border-bottom
Spacing:    .py-1  .px-2  .mt-3  .mb-2  .p-0
Visibility: .d-none
```

## Page Break CSS

```html
<!-- Force new page before this element -->
<div style="page-break-before: always;"/>

<!-- Force new page after this element -->
<div style="page-break-after: always;"/>

<!-- Prevent element from splitting across pages -->
<div style="page-break-inside: avoid;"/>
```

## XPath Positions (for inheritance)

| Position | Effect |
|----------|--------|
| `before` | Insert before the matched node |
| `after` | Insert after the matched node |
| `inside` | Append inside the matched node (at end) |
| `replace` | Replace the matched node entirely |
| `attributes` | Modify only the attributes of the node |

### Common XPath Expressions

```xml
<!-- Match by name attribute -->
<xpath expr="//div[@name='footer']" position="before"/>

<!-- Match by t-call attribute -->
<xpath expr="//t[@t-call='web.external_layout']" position="inside"/>

<!-- Match by t-field attribute -->
<xpath expr="//span[@t-field='o.name']" position="replace"/>

<!-- Match table with a specific class -->
<xpath expr="//table[hasclass('o_main_table')]" position="after"/>

<!-- Last row of a table -->
<xpath expr="//table//tr[last()]" position="after"/>
```
