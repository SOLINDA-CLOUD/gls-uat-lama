from odoo import _, api, fields, models
from dateutil import relativedelta

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    location_id = fields.Many2one('stock.location', string='Location')    

class ActionPlanMaintenance(models.Model):
    _name = 'action.plan.maintenance'
    _description = 'Action Plan Maintenance'
    
    name = fields.Char('Plan')
    due_date = fields.Datetime('Due Date')
    status = fields.Selection([
        ('open', 'Open'),
        ('op', 'On Progress'),
        ('done', 'Done'),
    ], string='status',default="open")
    maintenance_id = fields.Many2one('maintenance.request', string='Maintenance')

class ProgresHistoryMaintenance(models.Model):
    _name = 'progres.history.maintenance'
    _description = 'Progres History Maintenance'
    
    start_date = fields.Datetime('Start Date')
    end_date = fields.Datetime('End Date')
    stage_from = fields.Char('Stage From')
    stage_to = fields.Char('Stage To')
    duration = fields.Char(compute='_compute_duration', string='Duration')
    maintenance_id = fields.Many2one('maintenance.request', string='Maintenance')
    
    @api.depends('start_date','end_date')
    def _compute_duration(self):
        for i in self:
            if i.start_date and i.end_date:
                diff = relativedelta.relativedelta(i.end_date, i.start_date)
                years = diff.years
                months = diff.months
                days = diff.days
                hours = diff.hours
                minutes = diff.minutes
                if years > 0:
                    i.duration = str(years) + " Tahun " + str(months) + " bulan " + str(days) + " Hari" + str(hours) + " jam " + str(minutes) + " menit"
                elif months > 0:
                    i.duration = str(months) + " Bulan " + str(days) + " hari " + str(hours) + " jam " + str(minutes) + " menit"
                elif days > 0:
                    i.duration = str(days) + " Hari " + str(hours) + " jam " + str(minutes) + " menit"
                elif hours > 0:
                    i.duration = str(hours) + " Jam " + str(minutes) + " menit"
                else:
                    i.duration =str(minutes) + " Menit " + str(diff.seconds) + " detik"
            else:
                i.duration = False

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    _description = 'Maintenance Request'
    
    progres_history_line = fields.One2many('progres.history.maintenance', 'maintenance_id', string='Progress History')
    action_plan_line = fields.One2many('action.plan.maintenance', 'maintenance_id', string='Action Plan')
    shutdown_id = fields.Many2one('shutdown.system', string='Shutdown')
    job_order_id = fields.Many2one('job.order.request', string='Job Order') 
    location_id = fields.Many2one('stock.location', string='Location')
    mr_ids = fields.One2many('stock.picking', 'maintenance_id', string='MR')
    mr_count = fields.Integer(compute='_compute_mr_count', string='MR')

    change_stage_time = fields.Datetime('Change Stage Time')
    duration_change_stage = fields.Char(compute='_compute_duration_change_stage', string='Duration')
    
    # @api.depends('change_stage_time')
    def _compute_duration_change_stage(self):
        now = fields.datetime.now()
        for i in self:
            if i.change_stage_time:
                diff = relativedelta.relativedelta(i.change_stage_time, now)
                years = diff.years
                months = diff.months
                days = diff.days
                hours = diff.hours
                minutes = diff.minutes
                if years > 0:
                    i.duration_change_stage = str(years) + " Tahun " + str(months) + " bulan " + str(days) + " Hari" + str(hours) + " jam " + str(minutes) + " menit"
                elif months > 0:
                    i.duration_change_stage = str(months) + " Bulan " + str(days) + " hari " + str(hours) + " jam " + str(minutes) + " menit"
                elif days > 0:
                    i.duration_change_stage = str(days) + " Hari " + str(hours) + " jam " + str(minutes) + " menit"
                elif hours > 0:
                    i.duration_change_stage = str(hours) + " Jam " + str(minutes) + " menit"
                else:
                    i.duration_change_stage =str(minutes) + " Menit " + str(diff.seconds) + " detik"
            else:
                i.duration_change_stage = 'The changes stage time is not defined!'

    @api.onchange('stage_id')
    def _onchange_stages_id(self):
        for i in self:
            i.change_stage_time = fields.datetime.now()

    @api.depends('mr_ids')
    def _compute_mr_count(self):
        for i in self:
            i.mr_count = len(i.mr_ids)

    def create_open_mr(self):
         return {
                'name': 'Material Request',
                'type': 'ir.actions.act_window',
                'view_mode': 'tree,kanban,form,calendar,map',
                'res_model': 'stock.picking',
                'context': {'default_company_id': self.env.company.id,'default_maintenance_id':self.id},
                'domain': [('maintenance_id','=',self.id)],
            }
