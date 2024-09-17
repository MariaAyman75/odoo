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
