# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceRevision(models.Model):
    _name = "attendance_revision"
    _inherit = [
        "attendance_revision",
        "mixin.documenso_signing_approval",
    ]

    _documenso_signing_create_page = True
