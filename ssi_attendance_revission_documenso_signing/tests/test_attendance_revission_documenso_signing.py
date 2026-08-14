# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestAttendanceRevissionDocumensoSigning(YamlTransactionCase):
    """YAML-scenario test for the Documenso signing integration fields."""

    def test_attendance_revission_documenso_signing(self):
        """Run the scenario asserting the Documenso signing fields exist."""
        self.run_yaml_scenario("test_data_attendance_revission_documenso_signing.yaml")
