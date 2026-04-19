# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AttendanceRevisionDetail(models.Model):
    """
    Detail line of an attendance revision document.
    Stores the original and actual (revised) check-in and check-out
    datetime for each attendance schedule being corrected.
    """

    _name = "attendance_revision.detail"
    _description = "Attendance Revision - Detail"
    _order = "attendance_revision_id, attendance_schedule_id"

    attendance_revision_id = fields.Many2one(
        string="# Attendance Revision",
        comodel_name="attendance_revision",
        required=True,
        ondelete="cascade",
        help="The parent attendance revision document that this detail line belongs to.",
    )
    attendance_schedule_id = fields.Many2one(
        string="Attendance Schedule",
        comodel_name="hr.timesheet_attendance_schedule",
        required=True,
        ondelete="restrict",
        help="The attendance schedule entry being revised.",
    )
    schedule_date_start = fields.Datetime(
        string="Schedule Date Start",
        related="attendance_schedule_id.date_start",
        store=False,
        help="Schedule Date Start from the attendance schedule before revision.",
    )
    schedule_date_end = fields.Datetime(
        string="Schedule Date End",
        related="attendance_schedule_id.date_end",
        store=False,
        help="Schedule Date End from the attendance schedule before revision.",
    )
    original_date_start = fields.Datetime(
        string="Original Date Start",
        related="attendance_schedule_id.real_date_start",
        store=False,
        help="Original check-in datetime from the attendance schedule before revision.",
    )
    original_date_end = fields.Datetime(
        string="Original Date End",
        related="attendance_schedule_id.real_date_end",
        store=False,
        help="Original check-out datetime from the attendance schedule before revision.",
    )
    actual_date_start = fields.Datetime(
        string="Actual Date Start",
        help="Revised actual check-in datetime to replace the original schedule.",
    )
    actual_date_end = fields.Datetime(
        string="Actual Date End",
        help="Revised actual check-out datetime to replace the original schedule.",
    )
