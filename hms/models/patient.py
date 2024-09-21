from odoo import models, fields, api
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Model'
    _rec_name = 'first_name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    history = fields.Text()
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
    age = fields.Integer(compute='_compute_age', store=True)
    department_id = fields.Many2one('hms.department',domain=[('is_opened', '=', True)])
    doctor_ids = fields.Many2many('hms.doctor')
    department_capacity = fields.Integer(related='department_id.capacity', store=True)
    email = fields.Char()
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='Patient State', default='undetermined')
    patient_line_ids = fields.One2many('hms.patient.line', 'patient_id', string="Comments")

    @api.onchange('pcr')
    def _onchange_pcr(self):
        if self.pcr and not self.cr_ratio:
            raise ValidationError("CR Ratio is required when PCR is checked.")

    def action_undetermined(self):
        self.state = 'undetermined'
        self._create_log_entry('State changed to Undetermined')

    def action_good(self):
        self.state = 'good'
        self._create_log_entry('State changed to Good')

    def action_fair(self):
        self.state = 'fair'
        self._create_log_entry('State changed to Fair')

    def action_serious(self):
        self.state = 'serious'
        self._create_log_entry('State changed to Serious')

    def _create_log_entry(self, description):
        self.env['hms.patient.line'].create({
            'patient_id': self.id,
            'create_uid': self.env.user.id,
            'description': description,
            'date': fields.Datetime.now()
        })

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'This email already exists!'),
    ]

    @api.constrains('email')
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("Please enter a valid email address.")

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age = relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age = 0


class PatientLine(models.Model):
    _name = 'hms.patient.line'
    _description = 'Patient Line'

    patient_id = fields.Many2one('hms.patient', string="Patient", required=True)
    date = fields.Date(string="Date")
    description = fields.Char(string="Description")
