# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceRevisionType(YamlTransactionCase):
    """Cover the ``attendance_revision_type`` master data scenario."""

    def test_attendance_revision_type(self):
        """Run the create/read/update master data scenario."""
        self.run_yaml_scenario("test_data_attendance_revision_type.yaml")
