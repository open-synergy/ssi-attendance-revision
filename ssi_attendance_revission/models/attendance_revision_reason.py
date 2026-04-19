# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceRevisionReason(models.Model):
    """
    Master data for reasons used to justify an attendance revision request.
    Used to categorize why an employee's check-in or check-out time
    needs to be corrected.
    """

    _name = "attendance_revision_reason"
    _inherit = ["mixin.master_data"]
    _description = "Attendance Revision Reason"
