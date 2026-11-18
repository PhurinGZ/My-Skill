# Odoo 18 Model Methods & ORM Guide

Complete guide for working with Odoo 18 ORM, CRUD operations, and model methods.

## Table of Contents

1. [CRUD Operations](#crud-operations)
2. [Search & Domain](#search--domain)
3. [RecordSets](#recordsets)
4. [Computed Fields](#computed-fields)
5. [Constraints](#constraints)
6. [Related Fields](#related-fields)
7. [Aggregation](#aggregation)
8. [Inheritance](#inheritance)
9. [Best Practices](#best-practices)

## CRUD Operations

### Create

```python
# Single record
record = self.env['my.model'].create({
    'name': 'Test Record',
    'state': 'draft',
    'partner_id': partner.id,
})

# Multiple records
records = self.env['my.model'].create([
    {'name': 'Record 1', 'state': 'draft'},
    {'name': 'Record 2', 'state': 'draft'},
])

# With One2many commands
order = self.env['sale.order'].create({
    'partner_id': partner.id,
    'order_line': [
        (0, 0, {
            'product_id': product.id,
            'product_uom_qty': 2,
            'price_unit': 100.0,
        }),
        (0, 0, {
            'product_id': product2.id,
            'product_uom_qty': 1,
            'price_unit': 200.0,
        }),
    ]
})
```

### Read

```python
# Browse by ID
record = self.env['my.model'].browse(record_id)
records = self.env['my.model'].browse([1, 2, 3])

# Check if exists
if record.exists():
    # Record exists in database
    pass

# Read specific fields
data = record.read(['name', 'state'])
# Returns: [{'id': 1, 'name': 'Test', 'state': 'draft'}]

# Read multiple records
data = records.read(['name', 'create_date'])
```

### Write

```python
# Single field
record.name = 'New Name'

# Multiple fields
record.write({
    'name': 'Updated Name',
    'state': 'confirmed',
    'date': fields.Date.today(),
})

# Bulk write
records.write({'state': 'done'})

# With One2many commands
record.write({
    'line_ids': [
        (0, 0, {'name': 'New Line'}),  # Create
        (1, 5, {'name': 'Updated'}),   # Update ID 5
        (2, 6, {}),                     # Delete ID 6
        (3, 7, {}),                     # Unlink ID 7
        (4, 8, {}),                     # Link ID 8
        (5, 0, {'name': 'Replace'}),   # Replace all
        (6, 0, [1, 2, 3]),             # Set list
    ]
})
```

### Unlink

```python
# Delete single record
record.unlink()

# Delete multiple records
records.unlink()

# With @api.ondelete (Odoo 18)
@api.ondelete(at_uninstall=False)
def _check_unlink(self):
    for record in self:
        if record.state != 'draft':
            raise UserError('Cannot delete non-draft records')
```

## Search & Domain

### Basic Search

```python
# Simple search
records = self.env['my.model'].search([('state', '=', 'draft')])

# With ordering
records = self.env['my.model'].search(
    [('state', '=', 'draft')],
    order='create_date desc'
)

# With limit
records = self.env['my.model'].search(
    [('state', '=', 'draft')],
    limit=10
)

# With offset
records = self.env['my.model'].search(
    [('state', '=', 'draft')],
    offset=20,
    limit=10
)
```

### Domain Operators

```python
# Comparison operators
[('field', '=', value)]
[('field', '!=', value)]
[('field', '>', value)]
[('field', '>=', value)]
[('field', '<', value)]
[('field', '<=', value)]

# Set operators
[('field', 'in', [val1, val2])]
[('field', 'not in', [val1, val2])]

# Text operators
[('name', 'ilike', 'search')]      # Case-insensitive
[('name', 'like', 'search')]       # Case-sensitive
[('name', 'not ilike', 'search')]
[('name', '=like', 'pattern')]     # SQL LIKE pattern
[('name', '=ilike', 'pattern')]

# Relational operators
[('partner_id', '=', partner.id)]
[('partner_id', 'child_of', company.id)]
[('partner_id', 'parent_of', company.id)]

# Boolean operators
[('active', '=', True)]
[('active', '!=', False)]

# Date operators
[('date', '=', '2026-04-11')]
[('date', '>=', '2026-01-01')]
[('date', '<=', fields.Date.today())]
```

### Complex Domains

```python
# AND (implicit)
domain = [
    ('state', '=', 'draft'),
    ('partner_id', '!=', False),
]

# OR (using |)
domain = [
    '|',
    ('state', '=', 'draft'),
    ('state', '=', 'confirmed'),
]

# Complex OR
domain = [
    '&',
    ('state', '=', 'draft'),
    '|',
    ('partner_id', '=', partner.id),
    ('user_id', '=', user.id),
]

# NOT
domain = [
    '!',
    ('state', '=', 'cancel'),
]

# Real example
domain = [
    ('state', 'in', ['draft', 'confirmed']),
    ('company_id', '=', self.env.company.id),
    '|',
    ('partner_id', 'child_of', partner.id),
    ('user_id', '=', self.env.uid),
]
records = self.env['my.model'].search(domain, order='create_date desc')
```

### Search Read

```python
# Search and read in one query
data = self.env['my.model'].search_read(
    domain=[('state', '=', 'draft')],
    fields=['name', 'state', 'partner_id'],
    order='create_date desc',
    limit=10
)
# Returns: [{'id': 1, 'name': 'Test', 'state': 'draft', 'partner_id': (1, 'Partner')}]
```

### Search Count

```python
# Count records
count = self.env['my.model'].search_count([('state', '=', 'draft')])
```

## RecordSets

### Basic Operations

```python
# Iteration
for record in records:
    print(record.name)

# Slicing
first = records[0]
last = records[-1]
subset = records[:5]

# Length
count = len(records)

# Boolean check
if records:
    # Records exist
    pass

# Contains
if record in records:
    pass
```

### Set Operations

```python
# Union
combined = records1 | records2

# Intersection
common = records1 & records2

# Difference
diff = records1 - records2

# Concatenation (keeps duplicates)
all_records = records1 + records2
```

### Mapping & Filtering

```python
# Get field values
names = records.mapped('name')
# Returns: ['Name1', 'Name2', 'Name3']

# Get related records
partners = records.mapped('partner_id')

# Get nested fields
emails = records.mapped('partner_id.email')

# Filter
draft_records = records.filtered(lambda r: r.state == 'draft')
active_records = records.filtered('active')

# Sort
sorted_records = records.sorted(key=lambda r: r.create_date, reverse=True)
sorted_records = records.sorted('create_date')
```

## Computed Fields

### Basic Computed Field

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    amount = fields.Float(string='Amount')
    tax = fields.Float(string='Tax')
    total = fields.Float(
        string='Total',
        compute='_compute_total',
        store=True,  # Store in database
        readonly=True,
    )
    
    @api.depends('amount', 'tax')
    def _compute_total(self):
        for record in self:
            record.total = record.amount + record.tax
```

### Computed with Multiple Records

```python
@api.depends('line_ids.amount', 'line_ids.quantity')
def _compute_total(self):
    for record in self:
        record.total = sum(
            record.line_ids.mapped(lambda l: l.amount * l.quantity)
        )
```

### Inverse Function (Writable Computed)

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    full_name = fields.Char(
        string='Full Name',
        compute='_compute_full_name',
        inverse='_inverse_full_name',
        search='_search_full_name',
    )
    first_name = fields.Char(string='First Name')
    last_name = fields.Char(string='Last Name')
    
    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"
    
    def _inverse_full_name(self):
        for record in self:
            if record.full_name:
                parts = record.full_name.split()
                record.first_name = parts[0] if parts else ''
                record.last_name = parts[-1] if len(parts) > 1 else ''
    
    def _search_full_name(self, operator, value):
        # Custom search logic
        return [
            '|',
            ('first_name', operator, value),
            ('last_name', operator, value),
        ]
```

## Constraints

### Python Constraints

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    email = fields.Char(string='Email')
    age = fields.Integer(string='Age')
    
    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email and '@' not in record.email:
                raise ValidationError('Invalid email format')
    
    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 0:
                raise ValidationError('Age cannot be negative')
            if record.age > 150:
                raise ValidationError('Age seems invalid')
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError('Start date must be before end date')
```

### SQL Constraints

```python
class MyModel(models.Model):
    _name = 'my.model'
    
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique'),
        ('positive_amount', 'CHECK(amount > 0)', 'Amount must be positive'),
        ('valid_qty', 'CHECK(quantity >= 0)', 'Quantity cannot be negative'),
    ]
```

## Related Fields

```python
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    
    order_id = fields.Many2one('sale.order', string='Order')
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='order_id.partner_id',
        store=True,
        readonly=True,
    )
    date_order = fields.Datetime(
        string='Order Date',
        related='order_id.date_order',
        store=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='order_id.company_id',
        store=True,
    )
```

## Aggregation

### read_group

```python
# Basic grouping
result = self.env['sale.order'].read_group(
    domain=[('state', '=', 'sale')],
    fields=['partner_id', 'amount_total:sum'],
    groupby=['partner_id']
)
# Returns: [{'partner_id': (1, 'Customer'), 'partner_id_count': 5, 'amount_total': 5000.0}]

# Multiple fields
result = self.env['sale.order.line'].read_group(
    domain=[],
    fields=['product_id', 'quantity:sum', 'price_subtotal:sum'],
    groupby=['product_id']
)

# Multiple groupby
result = self.env['sale.order'].read_group(
    domain=[('state', 'in', ['sale', 'done'])],
    fields=['partner_id', 'user_id', 'amount_total:sum'],
    groupby=['partner_id', 'user_id'],
    lazy=False  # Get all levels at once
)

# With orderby
result = self.env['sale.order'].read_group(
    domain=[],
    fields=['state', 'amount_total:sum'],
    groupby=['state'],
    orderby='amount_total desc'
)

# Aggregation functions
# - sum: Total
# - avg: Average
# - min: Minimum
# - max: Maximum
# - count: Count (default for integer fields)

result = self.env['sale.order.line'].read_group(
    domain=[],
    fields=[
        'product_id',
        'quantity:sum',
        'quantity:avg',
        'price_unit:min',
        'price_unit:max',
        'id:count',
    ],
    groupby=['product_id']
)
```

## Inheritance

### Class Inheritance (_inherit)

```python
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    custom_field = fields.Char(string='Custom Field')
    
    def custom_method(self):
        # Custom logic
        pass
```

### Prototype Inheritance (_inherits)

```python
class ProductProduct(models.Model):
    _name = 'product.product'
    _inherits = {'product.template': 'product_tmpl_id'}
    
    product_tmpl_id = fields.Many2one(
        'product.template',
        required=True,
        ondelete='cascade',
    )
```

### Extension

```python
# Extend existing view
<record id="view_sale_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

## Best Practices

### ✅ DO

```python
# Use search_read for simple queries
data = self.env['model'].search_read(domain, fields)

# Use mapped for related fields
partners = records.mapped('partner_id')

# Bulk operations
records.write({'state': 'done'})

# Check existence
if record.exists():
    pass

# Use sudo() carefully
admin_records = self.env['model'].sudo().search([])
```

### ❌ DON'T

```python
# N+1 query problem
for record in records:
    partner = record.partner_id  # Query per record!

# Unnecessary loops
for record in records:
    record.write({'state': 'done'})  # Use records.write() instead

# Direct SQL when not needed
self.env.cr.execute("SELECT * FROM ...")  # Use ORM instead

# Unsafe sudo()
self.sudo().write(...)  # Be specific about what needs sudo
```

## Performance Tips

1. **Use `search_read()`** for simple data retrieval
2. **Use `mapped()`** to prefetch related fields
3. **Avoid loops** for write operations
4. **Use `filtered()`** instead of manual filtering
5. **Set `store=True`** on frequently accessed computed fields
6. **Use SQL** only for complex aggregations
7. **Index frequently searched fields**

## Common Patterns

### Get or Create

```python
record = self.env['my.model'].search([('name', '=', 'Test')], limit=1)
if not record:
    record = self.env['my.model'].create({'name': 'Test'})
```

### Toggle Boolean

```python
def toggle_active(self):
    for record in self:
        record.active = not record.active
```

### Copy Record

```python
new_record = record.copy({
    'name': 'Copy of ' + record.name,
    'state': 'draft',
})
```

---

**Reference**: Based on Odoo 18 ORM implementation
**Source**: [Odoo 18 models.py](https://github.com/odoo/odoo/blob/18.0/odoo/models.py)
