from odoo import _, api, fields, models

class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Mail Activity'
    
    def action_close_dialog(self):
        res = super(MailActivity, self).action_close_dialog()
        active_ids = self.env.context.get('active_ids', [])
        print("=======ACTIVE_IDS==========",active_ids)
        if self.activity_type_id.name in ['RAB / Cost Sheet']:
            create_rab = self.env["cost.sheet"].create({"crm_id": self.id,'partner_id':self.partner_id.id})
        print("RAB===============================")
        return res