# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import datetime

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class AttendanceRevision(models.Model):
    """
    Transactional document that records a request to revise an employee's
    attendance schedule. Allows correcting the actual check-in and check-out
    times that differ from the original timesheet schedule.
    Follows the confirm → approve → done workflow.
    """

    _name = "attendance_revision"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
        "mixin.many2one_configurator",
        "mixin.employee_document",
    ]
    _description = "Attendance Revision"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "done"

    date = fields.Date(
        string="Date",
        required=True,
        readonly=True,
        default=lambda self: datetime.date.today(),
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Date of the attendance revision request.",
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="attendance_revision_type",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Type of attendance revision that determines available reasons.",
    )

    @api.depends("type_id")
    def _compute_allowed_reason_ids(self):
        """Restrict selectable reasons to those allowed by ``type_id``.

        Delegates to the M2O Configurator helper on the selected
        ``attendance_revision_type``, using whichever selection method
        (manual list, domain, or Python code) that type defines.
        """
        for record in self:
            result = False
            if record.type_id:
                result = record._m2o_configurator_get_filter(
                    object_name="attendance_revision_reason",
                    method_selection=record.type_id.reason_selection_method,
                    manual_recordset=record.type_id.reason_ids,
                    domain=record.type_id.reason_domain,
                    python_code=record.type_id.reason_python_code,
                )
            record.allowed_reason_ids = result

    allowed_reason_ids = fields.Many2many(
        string="Allowed Reasons",
        comodel_name="attendance_revision_reason",
        compute="_compute_allowed_reason_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Computed list of reasons available for the selected type. "
            "Used as domain source in the view."
        ),
    )
    reason_id = fields.Many2one(
        string="Reason",
        comodel_name="attendance_revision_reason",
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="Reason for this attendance revision, filtered by the selected type.",
    )

    @api.depends("employee_id")
    def _compute_allowed_timesheet_ids(self):
        """Restrict selectable timesheets to open ones of ``employee_id``.

        Only ``hr.timesheet`` records in state ``open`` belonging to the
        selected employee are offered, since a revision must attach to a
        timesheet that is still being worked on.
        """
        Timesheet = self.env["hr.timesheet"]
        for record in self:
            result = []
            if record.employee_id:
                criteria = [
                    ("employee_id", "=", record.employee_id.id),
                    ("state", "=", "open"),
                ]
                result = Timesheet.search(criteria).ids
            record.allowed_timesheet_ids = result

    allowed_timesheet_ids = fields.Many2many(
        string="Allowed Timesheets",
        comodel_name="hr.timesheet",
        compute="_compute_allowed_timesheet_ids",
        store=False,
        compute_sudo=True,
        help=(
            "Computed list of open timesheets for the selected employee. "
            "Used as domain source in the view."
        ),
    )
    timesheet_id = fields.Many2one(
        string="# Timesheet",
        comodel_name="hr.timesheet",
        required=True,
        readonly=True,
        ondelete="restrict",
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The timesheet period being revised. Determines the attendance "
            "schedules available for correction."
        ),
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="attendance_revision.detail",
        inverse_name="attendance_revision_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        copy=True,
        help=(
            "List of attendance schedule lines being revised with their "
            "corrected check-in/check-out times."
        ),
    )

    @api.model
    def _get_policy_field(self):
        res = super(AttendanceRevision, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.onchange("employee_id", "type_id")
    def onchange_timesheet_id(self):
        self.timesheet_id = False

    @api.onchange("type_id")
    def onchange_reason_id(self):
        self.reason_id = False

    def action_reload_schedule(self):
        """Rebuild ``detail_ids`` from ``timesheet_id``'s schedule lines.

        Only applies to records still in state ``draft``. Existing detail
        lines are discarded and replaced with one new line per
        ``hr.timesheet_attendance_schedule`` entry found on the linked
        timesheet, each pre-filled from that schedule's current values
        (see ``_prepare_detail_data``). Inline action, invoked from the
        create and edit Instruction Kerja of this model.
        """
        for rec in self.sudo().filtered(lambda s: s.state == "draft"):
            rec.detail_ids = False
            line_vals = []
            for schedule in rec.timesheet_id.schedule_ids:
                line_vals.append(
                    (
                        0,
                        0,
                        rec._prepare_detail_data(schedule),
                    )
                )
            rec.detail_ids = line_vals

    def _prepare_detail_data(self, schedule):
        """Build the ``attendance_revision.detail`` values for ``schedule``.

        Extension point: override to change which fields are copied from
        the source ``hr.timesheet_attendance_schedule`` when
        ``action_reload_schedule`` (re)builds ``detail_ids``.

        :param schedule: the source ``hr.timesheet_attendance_schedule``
            record being copied into a new detail line
        :return: dict of ``attendance_revision.detail`` values
        """
        return {
            "attendance_revision_id": self.id,
            "attendance_schedule_id": schedule.id,
            "actual_date_start": schedule.real_date_start,
            "actual_date_end": schedule.real_date_end,
        }

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
