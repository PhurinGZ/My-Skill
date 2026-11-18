"""
Reference: HTTP Controller for Filtered HTML Report Preview in Odoo 18

This controller renders a report preview page with a filter bar.
Copy into `my_module/controllers/report_preview_controller.py` and adjust:
  - route path
  - model name
  - report reference
  - template reference

Important: in Odoo 18, _render_qweb_html(report_ref, docids, data={})
requires `docids` as the second positional argument.
"""
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
        if kw.get('state'):
            domain.append(('state', '=', kw['state']))

        records = request.env['sale.order'].search(domain)
        partners = request.env['res.partner'].search([('customer_rank', '>', 0)], order='name asc')

        html = request.env['ir.actions.report']._render_qweb_html(
            'my_module.report_my_document',
            records.ids,
            data={},
        )[0]

        return request.render('my_module.report_preview_page', {
            'records': records,
            'partners': partners,
            'filters': kw,
            'report_html': html.decode('utf-8') if isinstance(html, bytes) else html,
        })
