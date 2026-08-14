# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceRevision(HttpSavepointCase):
    """Tour tests for the ``attendance_revision`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the ``attendance_revision`` fixtures each tour needs.

        ``attendance_revision_validator_group`` already grants
        ``base.user_admin`` membership by default (see
        ``security/res_groups/attendance_revision.xml``) and implies both
        the user and viewer groups, so ``admin`` can run every tour here
        (including approving, since the shipped "Standard"
        ``approval.template`` draws its approvers from the same
        Validator group) without any extra group setup.

        Every fixture record's ``user_id`` is set explicitly to
        ``admin`` — ``cls.env`` runs as SUPERUSER here, and the record
        rule ``attendance_revision_internal_user_rule`` would otherwise
        hide records owned by someone else from the ``admin`` tour
        session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        cls.calendar = cls.env.ref("resource.resource_calendar_std")
        cls.revision_type = cls.env["attendance_revision_type"].create(
            {
                "name": "TOUR AR Type",
                "code": "/",
                "reason_selection_method": "domain",
                "reason_domain": "[]",
            }
        )
        cls.revision_reason = cls.env["attendance_revision_reason"].create(
            {"name": "TOUR AR Reason", "code": "/"}
        )

        # Used by the create tour: an employee with an open timesheet that
        # already has computed Attendance Schedules, so the Reload from
        # Timesheet inline action has data to pull in.
        cls.employee_create = cls._create_employee("TOUR AR Employee Create")
        cls.timesheet_create = cls._create_timesheet(cls.employee_create)

        cls.employee_edit = cls._create_employee("TOUR AR Employee Edit")
        cls.timesheet_edit = cls._create_timesheet(cls.employee_edit)
        cls.rec_edit = cls._create_revision(
            cls.employee_edit, cls.timesheet_edit, "TOUR-AR-EDIT"
        )

        cls.employee_delete = cls._create_employee("TOUR AR Employee Delete")
        cls.timesheet_delete = cls._create_timesheet(cls.employee_delete)
        cls.rec_delete = cls._create_revision(
            cls.employee_delete, cls.timesheet_delete, "TOUR-AR-DELETE"
        )

        cls.employee_confirm = cls._create_employee("TOUR AR Employee Confirm")
        cls.timesheet_confirm = cls._create_timesheet(cls.employee_confirm)
        cls.rec_confirm = cls._create_revision(
            cls.employee_confirm, cls.timesheet_confirm, "TOUR-AR-CONFIRM"
        )

        cls.employee_approve = cls._create_employee("TOUR AR Employee Approve")
        cls.timesheet_approve = cls._create_timesheet(cls.employee_approve)
        cls.rec_approve = cls._create_revision(
            cls.employee_approve, cls.timesheet_approve, "TOUR-AR-APPROVE"
        )
        cls.rec_approve.with_user(cls.admin).action_confirm()
        cls.rec_approve.invalidate_cache()

        cls.employee_reject = cls._create_employee("TOUR AR Employee Reject")
        cls.timesheet_reject = cls._create_timesheet(cls.employee_reject)
        cls.rec_reject = cls._create_revision(
            cls.employee_reject, cls.timesheet_reject, "TOUR-AR-REJECT"
        )
        cls.rec_reject.with_user(cls.admin).action_confirm()
        cls.rec_reject.invalidate_cache()

        cls.employee_cancel = cls._create_employee("TOUR AR Employee Cancel")
        cls.timesheet_cancel = cls._create_timesheet(cls.employee_cancel)
        cls.rec_cancel = cls._create_revision(
            cls.employee_cancel, cls.timesheet_cancel, "TOUR-AR-CANCEL"
        )

        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR AR Cancel Reason",
                "code": "TOURAR",
                "global_use": True,
            }
        )

        cls.employee_restart = cls._create_employee("TOUR AR Employee Restart")
        cls.timesheet_restart = cls._create_timesheet(cls.employee_restart)
        cls.rec_restart = cls._create_revision(
            cls.employee_restart, cls.timesheet_restart, "TOUR-AR-RESTART"
        )
        cls.rec_restart.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_cancel(cls.cancel_reason)
        cls.rec_restart.invalidate_cache()

    @classmethod
    def _create_employee(cls, name):
        """Create one ``hr.employee`` fixture used to identify a row.

        :param name: employee name, also used by the tours to locate the
            row in the list view (the Employee column is always visible)
        :return: the created ``hr.employee`` record
        :rtype: :class:`HrEmployee`
        """
        return cls.env["hr.employee"].create({"name": name})

    @classmethod
    def _create_timesheet(cls, employee):
        """Create, open, and compute schedules for one ``hr.timesheet``.

        :param employee: the ``hr.employee`` the timesheet belongs to
        :return: the created ``hr.timesheet`` record, in state Open, with
            its Attendance Schedules already computed from the calendar
        :rtype: :class:`HrTimesheet`
        """
        timesheet = cls.env["hr.timesheet"].create(
            {
                "employee_id": employee.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "working_schedule_id": cls.calendar.id,
                "user_id": cls.admin.id,
            }
        )
        timesheet.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_open()
        timesheet.invalidate_cache()
        timesheet.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_compute_schedule()
        timesheet.invalidate_cache()
        return timesheet

    @classmethod
    def _create_revision(cls, employee, timesheet, tag):
        """Create one draft ``attendance_revision`` fixture.

        :param employee: the ``hr.employee`` the revision belongs to
        :param timesheet: the employee's open ``hr.timesheet``
        :param tag: unused directly here — the caller identifies the row
            in the list view via ``employee.name`` instead
        :return: the created ``attendance_revision`` record
        :rtype: :class:`AttendanceRevision`
        """
        return cls.env["attendance_revision"].create(
            {
                "employee_id": employee.id,
                "type_id": cls.revision_type.id,
                "reason_id": cls.revision_reason.id,
                "timesheet_id": timesheet.id,
                "date": "2026-01-15",
                "user_id": cls.admin.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``attendance_revision``.

        IK: docs/attendance_revision/01-create.md
        """
        self.start_tour(
            "/web", "ssi_attendance_revission_attendance_revision_create", login="admin"
        )

    def test_edit(self):
        """Run the edit tour for ``attendance_revision``.

        IK: docs/attendance_revision/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_attendance_revission_attendance_revision_edit", login="admin"
        )

    def test_delete(self):
        """Run the delete tour for ``attendance_revision``.

        IK: docs/attendance_revision/03-delete.md
        """
        self.start_tour(
            "/web", "ssi_attendance_revission_attendance_revision_delete", login="admin"
        )

    def test_confirm(self):
        """Run the confirm tour for ``attendance_revision``.

        IK: docs/attendance_revision/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``attendance_revision``.

        IK: docs/attendance_revision/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``attendance_revision``.

        IK: docs/attendance_revision/06-reject.md
        """
        self.start_tour(
            "/web", "ssi_attendance_revission_attendance_revision_reject", login="admin"
        )

    def test_cancel(self):
        """Run the cancel tour for ``attendance_revision``.

        IK: docs/attendance_revision/10-cancel.md
        """
        self.start_tour(
            "/web", "ssi_attendance_revission_attendance_revision_cancel", login="admin"
        )

    def test_restart(self):
        """Run the restart tour for ``attendance_revision``.

        IK: docs/attendance_revision/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_restart",
            login="admin",
        )
