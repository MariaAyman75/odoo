from odoo import models, fields

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Model'
    _rec_name = 'first_name'

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-')])
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer()
    department_id = fields.Many2one('hms.department', string='Department')