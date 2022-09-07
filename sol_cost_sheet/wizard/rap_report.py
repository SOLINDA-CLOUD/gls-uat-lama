from odoo import _, api, fields, models

class RapReportWizard(models.TransientModel):
    _name = 'rap.report.wizard'
    _description = 'Rap Report Wizard'
    
    project_ids = fields.Many2many('project.project', string='Project')

    def download_xlsx_report(self):
        template_report = 'sol_cost_sheet.action_rap_report'
        return self.env.ref(template_report).report_action(self)
