# Odoo 18 API Decorators Guide

Complete guide for using @api decorators in Odoo 18.

## Decorator Types

### @api.model

```python
# Method that works on model, not records
@api.model
def create(self, vals):
    # Pre-process vals
    if vals.get('name') == '/':
        vals['name'] = self.env['ir.sequence'].next_by_code('my.model')
    return super().create(vals)

@api.model
def default_get(self, fields_list):
    res = super().default_get(fields_list)
    res['date'] = fields.Date.today()
    return res

@api.model
def _get_default_partner(self):
    return self.env.user.partner_id
```

### @api.depends

```python
# Computed fields
class MyModel(models.Model):
    _name = 'my.model'
    
    amount = fields.Float()
    tax = fields.Float()
    total = fields.Float(compute='_compute_total', store=True)
    
    @api.depends('amount', 'tax')
    def _compute_total(self):
        for record in self:
            record.total = record.amount + record.tax

# With nested depends
@api.depends('line_ids.amount', 'line_ids.quantity')
def _compute_total(self):
    for record in self:
        record.total = sum(
            record.line_ids.mapped(lambda l: l.amount * l.quantity)
        )

# With related fields
@api.depends('partner_id.name', 'partner_id.email')
def _compute_partner_info(self):
    for record in self:
        record.partner_name = record.partner_id.name
        record.partner_email = record.partner_id.email
```

### @api.constrains

```python
# Field validation
class MyModel(models.Model):
    _name = 'my.model'
    
    email = fields.Char()
    age = fields.Integer()
    start_date = fields.Date()
    end_date = fields.Date()
    
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
                raise ValidationError('Invalid age')
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError('Start date must be before end date')
    
    @api.constrains('name')
    def _check_name_length(self):
        for record in self:
            if record.name and len(record.name) < 3:
                raise ValidationError('Name must be at least 3 characters')
```

### @api.onchange

```python
# Dynamic UI updates
class MyModel(models.Model):
    _name = 'my.model'
    
    partner_id = fields.Many2one('res.partner')
    phone = fields.Char()
    email = fields.Char()
    line_ids = fields.One2many('my.model.line', 'model_id')
    total = fields.Float()
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.phone = self.partner_id.phone
            self.email = self.partner_id.email
        else:
            self.phone = False
            self.email = False
    
    @api.onchange('line_ids')
    def _onchange_lines(self):
        self.total = sum(self.line_ids.mapped('amount'))
    
    @api.onchange('field1', 'field2')
    def _onchange_fields(self):
        # Can return warning message
        if self.field1 > 100:
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Value seems high!',
                }
            }
    
    @api.onchange('date')
    def _onchange_date(self):
        # Can update other fields
        if self.date:
            self.deadline = self.date + timedelta(days=30)
```

### @api.ondelete

```python
# Odoo 18 - Delete validation
class MyModel(models.Model):
    _name = 'my.model'
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
    ])
    
    @api.ondelete(at_uninstall=False)
    def _check_unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError('Cannot delete non-draft records')
            if record.active:
                raise UserError('Cannot delete active records')

# With at_uninstall=True (allow delete during module uninstall)
@api.ondelete(at_uninstall=True)
def _check_unlink(self):
    for record in self:
        if record.related_ids:
            raise UserError('Cannot delete records with related data')
```

### @api.returns

```python
# Deprecated in newer Odoo versions
# Just return the recordset directly
def get_partner(self):
    return self.partner_id  # No decorator needed
```

## Method Patterns

### Create Override

```python
@api.model
def create(self, vals):
    # Pre-create logic
    if not vals.get('name'):
        vals['name'] = self._generate_name(vals)
    
    # Call super
    record = super().create(vals)
    
    # Post-create logic
    record._send_notification()
    
    return record
```

### Write Override

```python
def write(self, vals):
    # Pre-write logic
    if 'state' in vals:
        self._check_state_transition(vals['state'])
    
    # Call super
    result = super().write(vals)
    
    # Post-write logic
    if 'state' in vals:
        self._log_state_change()
    
    return result
```

### Unlink Override (Old style - use @api.ondelete in Odoo 18)

```python
# Odoo 17 or earlier
def unlink(self):
    for record in self:
        if record.state != 'draft':
            raise UserError('Cannot delete non-draft records')
    return super().unlink()

# Odoo 18 - Use @api.ondelete instead
@api.ondelete(at_uninstall=False)
def _check_unlink(self):
    for record in self:
        if record.state != 'draft':
            raise UserError('Cannot delete non-draft records')
```

### Read Override

```python
def read(self, fields=None, load='_classic_read'):
    # Pre-read logic
    result = super().read(fields, load)
    # Post-read logic
    return result
```

## Best Practices

### ✅ DO

```python
# Use @api.depends for computed fields
@api.depends('field1', 'field2')
def _compute_field(self):
    for record in self:
        record.field = record.field1 + record.field2

# Use @api.constrains for validation
@api.constrains('email')
def _check_email(self):
    for record in self:
        if not self._is_valid_email(record.email):
            raise ValidationError('Invalid email')

# Use @api.ondelete in Odoo 18
@api.ondelete(at_uninstall=False)
def _check_unlink(self):
    for record in self:
        if record.active:
            raise UserError('Cannot delete active records')

# Use @api.onchange for UI updates
@api.onchange('partner_id')
def _onchange_partner(self):
    self.email = self.partner_id.email
```

### ❌ DON'T

```python
# Don't use @api.multi (deprecated)
@api.multi
def my_method(self):  # Wrong in Odoo 18
    pass

# Don't forget @api.depends
# Wrong
def _compute_total(self):  # Missing @api.depends
    for record in self:
        record.total = record.amount * record.qty

# Don't use unlink override in Odoo 18
def unlink(self):  # Use @api.ondelete instead
    if self.state != 'draft':
        raise UserError('...')
    return super().unlink()

# Don't return values from onchange
@api.onchange('field')
def _onchange_field(self):
    return self.field  # Wrong, update self directly
```

## Common Patterns

### Compute with Default

```python
@api.depends('partner_id')
def _compute_name(self):
    for record in self:
        if record.partner_id:
            record.name = f"Order for {record.partner_id.name}"
        else:
            record.name = 'New Order'
```

### Multi-field Constrain

```python
@api.constrains('date_start', 'date_end', 'duration')
def _check_dates(self):
    for record in self:
        if record.date_start and record.date_end:
            if record.date_start > record.date_end:
                raise ValidationError('Start date must be before end date')
            if record.duration:
                actual_days = (record.date_end - record.date_start).days
                if abs(actual_days - record.duration) > 1:
                    raise ValidationError('Duration does not match dates')
```

### Onchange with Warning

```python
@api.onchange('product_id')
def _onchange_product(self):
    if self.product_id:
        self.price = self.product_id.list_price
        if self.product_id.type != 'service':
            return {
                'warning': {
                    'title': 'Product Type',
                    'message': 'This is a storable product. Make sure you have stock.',
                }
            }
```

### Ondelete with Multiple Checks

```python
@api.ondelete(at_uninstall=False)
def _check_unlink(self):
    for record in self:
        # Check state
        if record.state in ['done', 'cancel']:
            raise UserError('Cannot delete completed or cancelled records')
        
        # Check related records
        if record.invoice_ids:
            raise UserError('Cannot delete records with invoices')
        
        # Check activity
        if record.activity_ids:
            raise UserError('Please remove activities before deletion')
```

---

**Reference**: Based on Odoo 18 api.py
**Source**: [Odoo 18 api.py](https://github.com/odoo/odoo/blob/18.0/odoo/api.py)
