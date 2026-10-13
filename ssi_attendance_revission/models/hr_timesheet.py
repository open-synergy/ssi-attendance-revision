# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models


class HrTimesheet(models.Model):
    # Extension of hr.timesheet: reports the attendance revisions that
    # refer to the schedule slots of the timesheet, so that rebuilding
    # the schedules is refused before any slot is deleted.
    _inherit = "hr.timesheet"

    def _get_schedule_rebuild_blockers(self):
        """Add the attendance revisions that refer to the schedule slots.

        Every revision owning a detail line that points to a slot of this
        timesheet blocks the rebuild, whatever its state, because the
        database foreign key is ``restrict`` regardless of the state.

        :return: the blockers, each as ``(label, recordset)``
        :rtype: list
        """
        self.ensure_one()
        result = super(HrTimesheet, self)._get_schedule_rebuild_blockers()
        details = self.env["attendance_revision.detail"].search(
            [("attendance_schedule_id", "in", self.schedule_ids.ids)]
        )
        revisions = details.mapped("attendance_revision_id")
        if revisions:
            result.append((_("Attendance Revision"), revisions))
        return result
