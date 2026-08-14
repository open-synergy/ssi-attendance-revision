# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AttendanceRevision(models.Model):  # pylint: disable=too-few-public-methods
    """
    Adds operating unit traceability to attendance revisions.

    Brings in ``mixin.single_operating_unit`` so each attendance
    revision carries an ``operating_unit_id``, and pairs it with a
    record rule (``security/ir_rule/attendance_revision.xml``) that
    scopes visibility to the operating units the current user belongs
    to.
    """

    _name = "attendance_revision"
    _inherit = [
        "attendance_revision",
        "mixin.single_operating_unit",
    ]
