# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase — NOT HttpCase. 14.0's HttpCase has no cls.env in
# setUpClass (see odoo-development-ui-test skill, structure-and-runner.md).
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiAttendanceRevision(HttpSavepointCase):
    """Tours the Operating Unit field added to the attendance revision form."""

    @classmethod
    def setUpClass(cls):
        """Grant admin the group needed to see the Operating Unit field.

        Also creates the ``operating.unit`` fixture the tour picks from
        the field's dropdown. ``admin`` already belongs to
        ``attendance_revision_validator_group`` by default (see
        ``ssi_attendance_revission/security/res_groups/attendance_revision.xml``),
        which implies the User and Viewer groups, so no extra group is
        needed to open the menu and create form.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")
        # Pre-Condition: the Operating Unit field is gated by the multi
        # operating unit group; without it the field is not rendered and
        # the delta assertion would never find it.
        cls.env.ref("operating_unit.group_multi_operating_unit").sudo().write(
            {"users": [(4, cls.admin.id)]}
        )
        cls.tour_ou = cls.env["operating.unit"].create(
            {
                "name": "TOUR AR OU",
                "code": "TOURAROU",
                "partner_id": cls.env.ref("base.main_partner").id,
            }
        )

    def test_field_ou(self):
        """Run the operating unit field tour for ``attendance_revision``.

        IK: docs/attendance_revision/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_attendance_revision_operating_unit_attendance_revision_field_ou",
            login="admin",
        )
