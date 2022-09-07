from odoo import _, api, fields, models

class ReporttingBoo(models.TransientModel):
    _name = 'reporting.boo'
    _description = 'Reportting Boo'
    

    type = fields.Selection([('water_prod', 'Water Production'),('chemical_catridge', 'Chemical Catridge')], string='Type')
    warehouse_id = fields.Many2many('stock.location', string='Lokasi',domain=[("usage", "=", "internal")])
    product_ids = fields.Many2many('product.product', string='Product')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def download_report(self):
        # template_report = 'sol_boo.action_report_water_prod'
        # return self.env.ref(template_report).report_action(self)
        return
