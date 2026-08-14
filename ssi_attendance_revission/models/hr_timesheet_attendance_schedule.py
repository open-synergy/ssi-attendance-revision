# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrTimesheetAttendanceSchedule(models.Model):
    """
    Extends hr.timesheet_attendance_schedule to support attendance revision.
    Stores the latest approved revision detail and overrides the real
    work hour computation to reflect the revised check-in/check-out times.
    """

    _inherit = "hr.timesheet_attendance_schedule"

    @api.depends(
        "revision_detail_ids",
        "revision_detail_ids.attendance_revision_id",
        "revision_detail_ids.attendance_revision_id.state",
    )
    def _compute_latest_revision_detail_id(self):
        """Resolve the newest done-revision detail for this schedule.

        Searches ``attendance_revision.detail`` for lines that reference
        this schedule and belong to an ``attendance_revision`` already in
        state ``done``, keeping the most recently created one.
        """
        Detail = self.env["attendance_revision.detail"]
        for record in self:
            result = False
            criteria = [
                ("attendance_schedule_id", "=", record.id),
                ("attendance_revision_id.state", "=", "done"),
            ]
            detail = Detail.search(criteria, limit=1, order="id desc")
            if detail:
                result = detail.id
            record.latest_revision_detail_id = result

    revision_detail_ids = fields.One2many(
        string="Revision Details",
        comodel_name="attendance_revision.detail",
        inverse_name="attendance_schedule_id",
        readonly=True,
        help="All revision detail lines that reference this attendance schedule.",
    )
    latest_revision_detail_id = fields.Many2one(
        string="Latest Revision Detail",
        comodel_name="attendance_revision.detail",
        compute="_compute_latest_revision_detail_id",
        store=True,
        compute_sudo=True,
        help="The most recent approved revision detail for this schedule entry.",
    )
    latest_revision_id = fields.Many2one(
        string="Latest Revision",
        comodel_name="attendance_revision",
        related="latest_revision_detail_id.attendance_revision_id",
        store=False,
        help="The attendance revision document of the latest approved revision detail.",
    )
    revision_date_start = fields.Datetime(
        string="Revision Date Start",
        related="latest_revision_detail_id.actual_date_start",
        store=True,
        help="Revised check-in datetime from the latest approved revision.",
    )
    revision_date_end = fields.Datetime(
        string="Revision Date End",
        related="latest_revision_detail_id.actual_date_end",
        store=True,
        help="Revised check-out datetime from the latest approved revision.",
    )

    @api.depends(
        "attendance_ids",
        "attendance_ids.check_in",
        "attendance_ids.check_out",
        "attendance_ids.total_hour",
        "attendance_ids.total_valid_hour",
        "latest_revision_detail_id",
        "latest_revision_detail_id.actual_date_start",
        "latest_revision_detail_id.actual_date_end",
    )
    def _compute_attendance(self):
        """Override real check-in/out and hours with the latest revision.

        Calls ``super()`` to keep the base computation first, then, for
        schedules that have a done revision (``latest_revision_detail_id``
        set), replaces ``real_date_start``/``real_date_end`` with the
        revised datetimes and recomputes ``real_work_hour`` and
        ``real_valid_hour`` from that revised range.
        """
        super(HrTimesheetAttendanceSchedule, self)._compute_attendance()
        for schedule in self.filtered(lambda s: s.latest_revision_detail_id):
            if schedule.revision_date_start:
                schedule.real_date_start = schedule.revision_date_start
            if schedule.revision_date_end:
                schedule.real_date_end = schedule.revision_date_end
            if schedule.real_date_start and schedule.real_date_end:
                start = fields.Datetime.from_string(schedule.real_date_start)
                end = fields.Datetime.from_string(schedule.real_date_end)
                duration = (end - start).total_seconds() / 3600.0
                schedule.real_work_hour = duration
                schedule.real_valid_hour = duration
