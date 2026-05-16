# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceRevision(models.Model):  # pylint: disable=too-few-public-methods
    _name = "attendance_revision"
    _inherit = [
        "attendance_revision",
        "mixin.single_operating_unit",
    ]
