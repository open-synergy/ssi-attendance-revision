# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Attendance Revision",
    "version": "14.0.1.1.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_timesheet_attendance",
        "ssi_employee_document_mixin",
        "ssi_master_data_mixin",
        "ssi_transaction_confirm_mixin",
        "ssi_transaction_done_mixin",
        "ssi_transaction_cancel_mixin",
        "ssi_m2o_configurator_mixin",
    ],
    "data": [
        "security/ir_module_category/attendance_revision.xml",
        "security/res_groups/attendance_revision_type.xml",
        "security/res_groups/attendance_revision_reason.xml",
        "security/res_groups/attendance_revision.xml",
        "security/ir_model_access/attendance_revision_type.xml",
        "security/ir_model_access/attendance_revision_reason.xml",
        "security/ir_model_access/attendance_revision.xml",
        "security/ir_rule/attendance_revision.xml",
        "ir_sequence/attendance_revision.xml",
        "sequence_template/attendance_revision.xml",
        "approval_template/attendance_revision.xml",
        "policy_template/attendance_revision.xml",
        "menu.xml",
        "views/attendance_revision_type_views.xml",
        "views/attendance_revision_reason_views.xml",
        "views/attendance_revision_views.xml",
    ],
}
