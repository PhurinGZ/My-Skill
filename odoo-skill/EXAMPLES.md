# Odoo 18 Code Examples

## Example 1: Simple Module Structure

```
my_module/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── book.py
├── views/
│   └── book_views.xml
├── security/
│   └── ir.model.access.csv
└── demo/
    └── book_demo.xml
```

## Example 2: Complete Model

```python
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name, publish_date desc'

    # Basic fields
    name = fields.Char(string='Title', required=True, index=True, translate=True)
    isbn = fields.Char(string='ISBN', index=True)
    description = fields.Text(string='Description', translate=True)
    publish_date = fields.Date(string='Publish Date')
    pages = fields.Integer(string='Pages')
    active = fields.Boolean(string='Active', default=True)
    
    # Relational fields
    author_id = fields.Many2one('library.author', string='Author', required=True)
    category_ids = fields.Many2many('library.book.category', string='Categories')
    publisher_id = fields.Many2one('res.partner', string='Publisher',
                                   domain=[('is_company', '=', True)])
    
    # Monetary
    price = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    
    # Selection
    state = fields.Selection([
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)
    
    # Computed
    age_days = fields.Integer(string='Age (Days)', compute='_compute_age')
    
    @api.depends('publish_date')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.publish_date:
                delta = today - book.publish_date
                book.age_days = delta.days
            else:
                book.age_days = 0
    
    @api.constrains('isbn')
    def _check_isbn(self):
        for book in self:
            if book.isbn and len(book.isbn) not in [10, 13]:
                raise ValidationError('ISBN must be 10 or 13 characters')
    
    @api.ondelete(at_uninstall=False)
    def _check_unlink(self):
        for book in self:
            if book.state != 'draft':
                raise UserError('Cannot delete published or archived books')
    
    # Button actions
    def action_publish(self):
        for book in self:
            book.state = 'published'
        return True
    
    def action_draft(self):
        for book in self:
            book.state = 'draft'
        return True
    
    def action_archive(self):
        for book in self:
            book.state = 'archived'
        return True
```

## Example 3: Complete Views

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <!-- Search View -->
    <record id="view_library_book_search" model="ir.ui.view">
        <field name="name">library.book.search</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <search string="Search Books">
                <field name="name"/>
                <field name="isbn"/>
                <field name="author_id"/>
                <filter string="Draft" name="draft" 
                        domain="[('state', '=', 'draft')]"/>
                <filter string="Published" name="published" 
                        domain="[('state', '=', 'published')]"/>
                <separator/>
                <filter string="Archived" name="inactive" 
                        domain="[('active', '=', False)]"/>
                <group expand="0" string="Group By">
                    <filter string="Author" name="author" 
                            context="{'group_by': 'author_id'}"/>
                    <filter string="Category" name="category" 
                            context="{'group_by': 'category_ids'}"/>
                    <filter string="Status" name="state" 
                            context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- List View -->
    <record id="view_library_book_list" model="ir.ui.view">
        <field name="name">library.book.list</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <list string="Books" create="1" delete="1" edit="1" 
                  decoration-info="state == 'draft'"
                  decoration-success="state == 'published'"
                  decoration-muted="state == 'archived'">
                <field name="name"/>
                <field name="author_id"/>
                <field name="isbn"/>
                <field name="category_ids" widget="many2many_tags"/>
                <field name="publish_date"/>
                <field name="price" widget="monetary"/>
                <field name="state" widget="badge"
                       decoration-info="state == 'draft'"
                       decoration-success="state == 'published'"
                       decoration-warning="state == 'archived'"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_library_book_form" model="ir.ui.view">
        <field name="name">library.book.form</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <form string="Book">
                <header>
                    <button name="action_publish" string="Publish" 
                            type="object" class="oe_highlight"
                            invisible="state != 'draft'"/>
                    <button name="action_draft" String="Set to Draft" 
                            type="object"
                            invisible="state != 'published'"/>
                    <button name="action_archive" String="Archive" 
                            type="object"
                            invisible="state != 'published'"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="draft,published,archived"/>
                </header>
                <sheet>
                    <div class="oe_button_box" name="button_box">
                        <button name="toggle_active" type="object" 
                                class="oe_stat_button" icon="fa-archive">
                            <field name="active" widget="boolean_button" 
                                   options='{"terminology": "archive"}'/>
                        </button>
                    </div>
                    <div class="oe_title">
                        <label for="name"/>
                        <h1>
                            <field name="name" placeholder="Book title..."/>
                        </h1>
                    </div>
                    <group>
                        <group>
                            <field name="author_id"/>
                            <field name="isbn"/>
                            <field name="publisher_id"/>
                            <field name="category_ids" widget="many2many_tags"/>
                        </group>
                        <group>
                            <field name="publish_date"/>
                            <field name="pages"/>
                            <field name="price"/>
                            <field name="currency_id"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Description" name="description">
                            <field name="description" 
                                   placeholder="Book description..."/>
                        </page>
                    </notebook>
                </sheet>
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Action -->
    <record id="action_library_book" model="ir.actions.act_window">
        <field name="name">Books</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_library_book_search"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first book
            </p>
            <p>
                Add books to your library collection.
            </p>
        </field>
    </record>

    <!-- Menus -->
    <menuitem id="menu_library_root" name="Library" sequence="10"/>
    <menuitem id="menu_library_books" name="Books" 
              parent="menu_library_root" 
              action="action_library_book" 
              sequence="10"/>
</odoo>
```

## Example 4: Controller

```python
from odoo import http, _
from odoo.http import request
import json

class LibraryController(http.Controller):
    
    @http.route('/library/books', type='json', auth='user')
    def get_books(self, **kwargs):
        """Get all books as JSON"""
        books = request.env['library.book'].search([])
        return {
            'books': books.read(['name', 'isbn', 'author_id', 'state'])
        }
    
    @http.route('/library/books/<int:book_id>', type='json', auth='user')
    def get_book(self, book_id, **kwargs):
        """Get specific book"""
        book = request.env['library.book'].browse(book_id)
        if not book.exists():
            return {'error': 'Book not found'}
        return {'book': book.read(['name', 'isbn', 'description', 'price'])[0]}
    
    @http.route('/library/public/books', type='http', auth='public', website=True)
    def public_books(self, **kwargs):
        """Public books page"""
        books = request.env['library.book'].search([
            ('state', '=', 'published'),
            ('active', '=', True)
        ])
        return request.render('my_module.public_books_template', {
            'books': books
        })
    
    @http.route('/library/books/<int:book_id>/download', type='http', auth='user')
    def download_book(self, book_id, **kwargs):
        """Download book details as PDF"""
        book = request.env['library.book'].browse(book_id)
        if not book.exists():
            return request.not_found()
        
        # Generate PDF
        pdf = request.env['ir.actions.report']._render_qweb_pdf(
            'my_module.report_book', [book.id]
        )[0]
        
        return request.make_response(
            pdf,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', f'attachment; filename="{book.name}.pdf"')
            ]
        )
```

## Example 5: OWL Component

```javascript
/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class BookDashboard extends Component {
    static template = "library.BookDashboard";
    static components = {};
    static props = {};

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            books: [],
            loading: true,
            error: null,
            stats: {
                total: 0,
                published: 0,
                draft: 0,
            }
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        try {
            this.state.loading = true;
            
            // Get books
            this.state.books = await this.orm.searchRead(
                'library.book',
                [['state', '=', 'published']],
                ['name', 'author_id', 'price', 'state']
            );

            // Get stats
            const allBooks = await this.orm.searchRead(
                'library.book',
                [],
                ['state']
            );

            this.state.stats = {
                total: allBooks.length,
                published: allBooks.filter(b => b.state === 'published').length,
                draft: allBooks.filter(b => b.state === 'draft').length,
            };

        } catch (error) {
            this.state.error = error.message;
        } finally {
            this.state.loading = false;
        }
    }

    async onBookClick(bookId) {
        // Open book form view
        return this.env.services.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'library.book',
            res_id: bookId,
            views: [[false, 'form']],
            target: 'current',
        });
    }
}
```

## Example 6: Tests

```python
from odoo.tests import common, tagged
from odoo.exceptions import ValidationError, UserError

@tagged('post_install', '-at_install')
class TestLibraryBook(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.Book = self.env['library.book']
        self.Author = self.env['library.author']
        
        # Create test author
        self.author = self.Author.create({
            'name': 'Test Author',
        })
        
        # Create test book
        self.book = self.Book.create({
            'name': 'Test Book',
            'author_id': self.author.id,
            'state': 'draft',
        })
    
    def test_create_book(self):
        """Test book creation"""
        self.assertEqual(self.book.name, 'Test Book')
        self.assertEqual(self.book.author_id, self.author)
        self.assertEqual(self.book.state, 'draft')
    
    def test_publish_book(self):
        """Test publishing workflow"""
        self.book.action_publish()
        self.assertEqual(self.book.state, 'published')
    
    def test_isbn_validation(self):
        """Test ISBN validation"""
        with self.assertRaises(ValidationError):
            self.Book.create({
                'name': 'Invalid ISBN Book',
                'author_id': self.author.id,
                'isbn': '123',  # Too short
            })
    
    def test_delete_published_book(self):
        """Test cannot delete published book"""
        self.book.action_publish()
        with self.assertRaises(UserError):
            self.book.unlink()
    
    def test_search_books(self):
        """Test search functionality"""
        books = self.Book.search([('state', '=', 'draft')])
        self.assertIn(self.book, books)
    
    def test_compute_age(self):
        """Test computed age field"""
        from datetime import date, timedelta
        
        yesterday = date.today() - timedelta(days=1)
        self.book.publish_date = yesterday
        self.book._compute_age()
        
        self.assertGreaterEqual(self.book.age_days, 1)
```

---

**Note**: These are example snippets. Always refer to SKILL.md for complete documentation and best practices.
