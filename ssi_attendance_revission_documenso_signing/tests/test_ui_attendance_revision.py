# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceRevisionDocumensoSigning(HttpSavepointCase):
    """Tour test for the ``attendance_revision`` Documenso signing delta."""

    @classmethod
    def setUpClass(cls):
        """Prepare one Waiting-for-Approval fixture.

        Pre-Condition IK (delta): a record already Waiting for Approval,
        whose active Approval Template has **no** Documenso Signing
        Template configured -- the Signature Requests tab is still shown
        (``_documenso_signing_create_page = True``), but base Flow steps
        3-4 (Approve / OK) are unaffected, per this module's own Modified
        Flow bullet 2. ``attendance_revision_validator_group`` already
        grants ``base.user_admin`` membership by default (see
        ``ssi_attendance_revission/security/res_groups/
        attendance_revision.xml``) and implies both the user and viewer
        groups, so ``admin`` can approve without any extra group setup --
        same fixture shape as
        ``ssi_attendance_revission.tests.test_ui_attendance_revision``.

        Every fixture record's ``user_id`` is set explicitly to
        ``admin`` -- ``cls.env`` runs as SUPERUSER here, and the record
        rule ``attendance_revision_internal_user_rule`` would otherwise
        hide records owned by someone else from the ``admin`` tour
        session.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        calendar = cls.env.ref("resource.resource_calendar_std")
        revision_type = cls.env["attendance_revision_type"].create(
            {
                "name": "TOUR AR DS Type",
                "code": "/",
                "reason_selection_method": "domain",
                "reason_domain": "[]",
            }
        )
        employee = cls.env["hr.employee"].create(
            {"name": "TOUR AR DS Employee Approve"}
        )
        timesheet = cls.env["hr.timesheet"].create(
            {
                "name": "TOUR-AR-DS-TS-APPROVE",
                "employee_id": employee.id,
                "date_start": "2026-01-01",
                "date_end": "2026-01-31",
                "working_schedule_id": calendar.id,
                "user_id": cls.admin.id,
            }
        )
        timesheet.with_user(cls.admin).with_context(
            bypass_policy_check=True
        ).action_open()
        timesheet.invalidate_cache()

        cls.rec_approve = cls.env["attendance_revision"].create(
            {
                "employee_id": employee.id,
                "type_id": revision_type.id,
                "timesheet_id": timesheet.id,
                "date": "2026-01-15",
                "user_id": cls.admin.id,
            }
        )
        cls.rec_approve.with_user(cls.admin).action_confirm()
        cls.rec_approve.invalidate_cache()

    def test_approve(self):
        """Run the approve tour for the Documenso signing delta.

        IK: docs/attendance_revision/05-approve.md (E2a delta -- Modified
        Flow)
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_documenso_signing_attendance_revision_approve",
            login="admin",
        )
