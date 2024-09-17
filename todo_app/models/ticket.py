from odoo import models, fields

class Ticket(models.Model):
    _name = 'todo.ticket'
    _description = 'Todo Ticket'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    state = fields.Selection([('new', 'New'), ('doing', 'Doing'), ('done', 'Done')],  default='new')
    file = fields.Binary()
    assign_to = fields.Many2one('res.users')
    description = fields.Text()

    def action_new(self):
        print("inside action_new")
        self.state = 'new'

    def action_doing(self):
        print("inside action_doing")
        self.state = 'doing'

    def action_done(self):
        print("inside action_done")
        self.state = 'done'
