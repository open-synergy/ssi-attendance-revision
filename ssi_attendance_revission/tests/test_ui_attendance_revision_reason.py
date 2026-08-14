# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceRevisionReason(HttpSavepointCase):
    """Tour tests for the ``attendance_revision_reason`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the ``attendance_revision_reason`` fixtures each tour needs.

        ``attendance_revision_reason_group`` already grants
        ``base.user_root`` and ``base.user_admin`` membership by default
        (see ``security/res_groups/attendance_revision_reason.xml``), so
        ``admin`` can run every tour here without any extra group setup.
        """
        super().setUpClass()
        cls.rec_edit = cls.env["attendance_revision_reason"].create(
            {"name": "TOUR ARR Edit", "code": "/"}
        )
        cls.rec_delete = cls.env["attendance_revision_reason"].create(
            {"name": "TOUR ARR Delete", "code": "/"}
        )
        cls.rec_deactivate = cls.env["attendance_revision_reason"].create(
            {"name": "TOUR ARR Deactivate", "code": "/"}
        )
        cls.rec_activate = cls.env["attendance_revision_reason"].create(
            {"name": "TOUR ARR Activate", "code": "/", "active": False}
        )

    def test_create(self):
        """Run the create tour for ``attendance_revision_reason``.

        IK: docs/attendance_revision_reason/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_reason_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``attendance_revision_reason``.

        IK: docs/attendance_revision_reason/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_reason_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``attendance_revision_reason``.

        IK: docs/attendance_revision_reason/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_reason_delete",
            login="admin",
        )

    def test_deactivate(self):
        """Run the deactivate tour for ``attendance_revision_reason``.

        IK: docs/attendance_revision_reason/04-deactivate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_reason_deactivate",
            login="admin",
        )

    def test_activate(self):
        """Run the activate tour for ``attendance_revision_reason``.

        IK: docs/attendance_revision_reason/05-activate.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revission_attendance_revision_reason_activate",
            login="admin",
        )
