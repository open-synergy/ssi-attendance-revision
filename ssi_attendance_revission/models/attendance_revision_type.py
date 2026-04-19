# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttendanceRevisionType(models.Model):
    """
    Master data for types of attendance revision.
    Each type controls which reasons are available for selection
    via the M2O Configurator pattern (manual list, domain, or Python code).
    """

    _name = "attendance_revision_type"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Revision Type"

    # M2O Configurator for reason_id
    reason_selection_method = fields.Selection(
        string="Reason Selection Method",
        default="domain",
        selection=[
            ("manual", "Manual"),
            ("domain", "Domain"),
            ("code", "Python Code"),
        ],
        required=True,
        help=(
            "Method used to filter available reasons for this type. "
            "Manual: select from a fixed list. "
            "Domain: filter using an Odoo domain expression. "
            "Python Code: compute programmatically."
        ),
    )
    reason_ids = fields.Many2many(
        string="Reasons",
        comodel_name="attendance_revision_reason",
        relation="rel_attendance_revision_type_2_reason",
        column1="type_id",
        column2="reason_id",
        help="List of allowed reasons when selection method is set to Manual.",
    )
    reason_domain = fields.Text(
        string="Reason Domain",
        default="[]",
        help=(
            "Odoo domain expression used to filter allowed reasons "
            "when selection method is Domain."
        ),
    )
    reason_python_code = fields.Text(
        string="Reason Python Code",
        default="result = []",
        help=(
            "Python code that returns a list of reason IDs "
            "when selection method is Python Code."
        ),
    )
