# Odoo 18 Field Types Guide

Complete guide for defining model fields in Odoo 18.

## Simple Field Types

### Basic Fields

```python
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    
    # Character (string)
    name = fields.Char(
        string='Name',
        required=True,
        index=True,
        translate=True,  # Translatable
        size=256,
        default='Untitled',
    )
    
    # Integer
    quantity = fields.Integer(
        string='Quantity',
        default=0,
        required=True,
    )
    
    # Float
    price = fields.Float(
        string='Price',
        digits=(16, 2),  # (total, decimals)
        default=0.0,
    )
    
    # Boolean - MUST specify default in Odoo 18
    active = fields.Boolean(
        string='Active',
        default=True,  # Required in Odoo 18
    )
    is_published = fields.Boolean(default=False)
    
    # Text
    description = fields.Text(
        string='Description',
        translate=True,
    )
    
    # HTML
    content = fields.Html(
        string='Content',
        translate=True,
        sanitize=True,  # Sanitize HTML
    )
    
    # Date
    date = fields.Date(
        string='Date',
        default=fields.Date.today,
        required=True,
    )
    
    # Datetime
    datetime = fields.Datetime(
        string='DateTime',
        default=fields.Datetime.now,
        required=True,
    )
```

## Relational Fields

### Many2one

```python
# Basic Many2one
partner_id = fields.Many2one(
    'res.partner',
    string='Partner',
    required=True,
    ondelete='cascade',  # cascade, set null, restrict
    index=True,
    auto_join=True,  # Use SQL JOIN (faster but bypasses ACL)
    domain=[('customer', '=', True)],
    context={'default_customer': True},
)

# With company
company_id = fields.Many2one(
    'res.company',
    string='Company',
    required=True,
    default=lambda self: self.env.company,
)

# With user
user_id = fields.Many2one(
    'res.users',
    string='Responsible',
    default=lambda self: self.env.user,
    tracking=True,  # Track changes
)
```

### One2many

```python
# One2many (inverse of Many2one)
order_line = fields.One2many(
    'sale.order.line',  # Comodel
    'order_id',         # Inverse field
    string='Order Lines',
    copy=True,
    auto_join=False,
    context={'default_product_uom_qty': 1},
)

# With domain
line_ids = fields.One2many(
    'my.model.line',
    'model_id',
    string='Lines',
    domain=[('active', '=', True)],
)
```

### Many2many

```python
# Basic Many2many
tag_ids = fields.Many2many(
    'my.model.tag',
    string='Tags',
)

# With explicit table and columns
category_ids = fields.Many2many(
    'my.model.category',
    'my_model_category_rel',  # Relation table
    'model_id',               # Column for this model
    'category_id',            # Column for other model
    string='Categories',
)

# With domain and context
partner_ids = fields.Many2many(
    'res.partner',
    string='Partners',
    domain=[('customer', '=', True)],
    context={'search_default_customer': 1},
)

# With tracking
follower_ids = fields.Many2many(
    'res.partner',
    string='Followers',
    tracking=True,
)
```

## Special Field Types

### Selection

```python
# Basic Selection
state = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('done', 'Done'),
    ('cancel', 'Cancelled'),
], string='Status', default='draft', required=True, tracking=True)

# With selection_add (inheritance)
class MyModel(models.Model):
    _inherit = 'other.model'
    
    state = fields.Selection(
        selection_add=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
        ],
        ondelete={'pending': 'set default', 'approved': 'cascade'},
    )

# Dynamic selection
def _get_priority(self):
    return [
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Very High'),
    ]

priority = fields.Selection(
    selection='_get_priority',
    string='Priority',
    default='1',
)
```

### Monetary

```python
# Monetary field (requires currency_id)
amount = fields.Monetary(
    string='Amount',
    currency_field='currency_id',
    required=True,
)

currency_id = fields.Many2one(
    'res.currency',
    string='Currency',
    default=lambda self: self.env.company.currency_id,
    required=True,
)

# With computed total
total = fields.Monetary(
    string='Total',
    compute='_compute_total',
    currency_field='currency_id',
    store=True,
)
```

### Binary & Image

```python
# Binary (file)
attachment = fields.Binary(
    string='Attachment',
    required=True,
)

filename = fields.Char(string='Filename')

# Image
image = fields.Image(
    string='Image',
    max_width=1024,
    max_height=1024,
    verify_resolution=False,
)

# Multiple images
image_1920 = fields.Image(string='Image', max_width=1920)
image_1024 = fields.Image(string='Image 1024', max_width=1024, related='image_1920')
image_256 = fields.Image(string='Image 256', max_width=256, related='image_1920')
image_128 = fields.Image(string='Image 128', max_width=128, related='image_1920')
```

### Reference

```python
# Generic reference to any model
reference = fields.Reference(
    selection=[
        ('res.partner', 'Contact'),
        ('account.move', 'Invoice'),
        ('sale.order', 'Sale Order'),
    ],
    string='Reference',
)
```

### Serialized

```python
# JSON data
settings = fields.Serialized(
    string='Settings',
    default=lambda: {'key1': 'value1', 'key2': 0},
)

# Usage
record.settings = {'theme': 'dark', 'lang': 'en'}
theme = record.settings.get('theme')
```

## Field Parameters

### Common Parameters

```python
field_name = fields.Type(
    # Display
    string='Field Label',
    help='Help text shown to users',
    
    # Requirements
    required=True,
    readonly=True,
    copy=False,  # Don't copy when duplicating record
    
    # Database
    index=True,  # Add database index
    store=True,  # Store computed field
    default=value,  # Default value
    
    # Security
    groups='base.group_user',  # Restrict by group
    invisible=True,  # Hide from views
    
    # Special
    translate=True,  # Make translatable
    tracking=True,  # Track changes in chatter
    related='parent_id.field',  # Related field
    compute='_compute_field',  # Computed field
    inverse='_inverse_field',  # Writable computed
    search='_search_field',  # Custom search
    aggregator='sum',  # Aggregation function (Odoo 18)
)
```

### Default Values

```python
# Static default
active = fields.Boolean(default=True)
state = fields.Selection([...], default='draft')

# Function default
company_id = fields.Many2one(
    'res.company',
    default=lambda self: self.env.company,
)

user_id = fields.Many2one(
    'res.users',
    default=lambda self: self.env.user,
)

date = fields.Date(
    default=fields.Date.context_today,
)

datetime = fields.Datetime(
    default=fields.Datetime.now,
)

# From context
lang = fields.Char(
    default=lambda self: self.env.context.get('lang'),
)

# Computed default
def _default_name(self):
    return f"New/{self.env['ir.sequence'].next_by_code('my.model')}"

name = fields.Char(default=_default_name)
```

## Field Inheritance

### Extend Field

```python
class MyModel(models.Model):
    _inherit = 'sale.order'
    
    # Extend existing field
    partner_id = fields.Many2one(
        string='Customer',
        domain=[('customer', '=', True)],
        required=True,
    )
```

### Change Field Attributes

```python
# Make required
name = fields.Char(required=True)

# Change string
date = fields.Date(string='Order Date')

# Add tracking
state = fields.Selection([...], tracking=True)

# Change default
active = fields.Boolean(default=False)

# Remove required
name = fields.Char(required=False)
```

## Odoo 18 Changes

### Aggregator (replaces group_operator)

```python
# Odoo 17
total = fields.Float(group_operator='sum')

# Odoo 18
total = fields.Float(aggregator='sum')

# Available aggregators
# - sum: Total
# - avg: Average
# - min: Minimum
# - max: Maximum
# - count: Count
# - bool_and: All True
# - bool_or: Any True
```

### Boolean Fields

```python
# Odoo 18 - MUST specify default
active = fields.Boolean(default=True)
is_published = fields.Boolean(default=False)

# Don't rely on default False anymore
```

## Best Practices

### ✅ DO

```python
# Specify defaults for Boolean
active = fields.Boolean(default=True)

# Use tracking for important fields
state = fields.Selection([...], tracking=True)
amount = fields.Monetary(tracking=True)

# Add index for frequently searched fields
name = fields.Char(index=True)
email = fields.Char(index=True)

# Use aggregator in Odoo 18
total = fields.Float(aggregator='sum')

# Set appropriate ondelete
partner_id = fields.Many2one('res.partner', ondelete='cascade')
```

### ❌ DON'T

```python
# Don't omit Boolean default
active = fields.Boolean()  # Error in Odoo 18

# Don't use old syntax
total = fields.Float(group_operator='sum')  # Use aggregator

# Don't overuse index
description = fields.Text(index=True)  # Not useful for Text

# Don't make everything required
notes = fields.Text(required=True)  # Probably shouldn't be required
```

## Common Field Combinations

### Audit Fields

```python
create_uid = fields.Many2one('res.users', string='Created By', readonly=True)
create_date = fields.Datetime(string='Created On', readonly=True)
write_uid = fields.Many2one('res.users', string='Last Updated By', readonly=True)
write_date = fields.Datetime(string='Last Updated On', readonly=True)
```

### Company Dependent

```python
company_id = fields.Many2one(
    'res.company',
    string='Company',
    required=True,
    default=lambda self: self.env.company,
)
```

### Active Record

```python
active = fields.Boolean(
    string='Active',
    default=True,
    index=True,
)
```

---

**Reference**: Based on Odoo 18 fields.py
**Source**: [Odoo 18 fields.py](https://github.com/odoo/odoo/blob/18.0/odoo/fields.py)
