odoo.define("ssi_attendance_revission.attendance_revision_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Flow 1 of every IK in this file: "Open the Human Resource > Timesheets
    // > Attendance Revision menu." "Timesheets" is a level-2 menu with
    // children, so it renders as a dropdown-toggle section; "Attendance
    // Revision" is a leaf underneath it (patterns.md "Jumlah level menu di
    // IK != jumlah step tour"). The breadcrumb gate checks the ACTION
    // title ("Attendance Revision" — see views/attendance_revision_views.xml),
    // not the menu label.
    var openAttendanceRevisionList = function () {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Human Resource app",
                trigger: '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
            },
            {
                content: "Open the Timesheets menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_timesheet.timesheet_menu"]',
            },
            {
                content: "Open the Attendance Revision menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_attendance_revission.attendance_revision_menu"]',
            },
            {
                content: "Attendance Revision list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Attendance Revision)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    };

    // IK: docs/attendance_revision/01-create.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Click the New button.
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Fill in the required fields.
            {
                content: "Select the Employee",
                trigger: ".o_field_many2one[name='employee_id'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR AR Employee Create",
            },
            {
                content: "Pick the Employee from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(TOUR AR Employee Create)",
                in_modal: false,
            },
            {
                content: "Select the Type",
                trigger: ".o_field_many2one[name='type_id'] input",
                run: "text TOUR AR Type",
            },
            {
                content: "Pick the Type from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AR Type)",
                in_modal: false,
            },
            {
                content: "Select the Reason",
                trigger: ".o_field_many2one[name='reason_id'] input",
                run: "text TOUR AR Reason",
            },
            {
                content: "Pick the Reason from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AR Reason)",
                in_modal: false,
            },
            {
                // The fixture timesheet has an explicit manual document
                // number (not the default "/"), so it can be searched by
                // name like any other many2one — relying on domain
                // uniqueness plus a blind click on the first autocomplete
                // result is unsafe: a race between the employee_id
                // onchange (which recomputes allowed_timesheet_ids) and
                // opening the dropdown can leave the result list stale,
                // and an unfiltered click can land on the "Create ..."
                // quick-create option instead of the real record.
                content: "Select the # Timesheet",
                trigger: ".o_field_many2one[name='timesheet_id'] input",
                run: "text TOUR-AR-TS-CREATE",
            },
            {
                content: "Pick the Timesheet from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR-AR-TS-CREATE)",
                in_modal: false,
            },

            // Flow 4 — Reload from Timesheet (Inline Action).
            {
                content: "Click the Reload from Timesheet button",
                trigger: ".o_notebook button[name='action_reload_schedule']",
            },
            // Gerbang — record is new (unsaved), so the object button
            // forces an auto-save first. Breadcrumb title only stops
            // reading "New" once that save has landed (patterns.md §P).
            {
                content: "Record has been saved by Reload from Timesheet",
                trigger: ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Attendance Schedule lines are loaded",
                trigger: ".o_field_x2many[name='detail_ids'] .o_data_row",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 5 — Fill in Actual Date Start/End on the reloaded line.
            // 14.0 list cells carry NO `name` attribute until the row is
            // activated into edit mode (only <th> headers have
            // data-name) — click any cell of the row first, matching
            // patterns.md §C ("...SO/2026/001) .o_data_cell:first").
            {
                content: "Open the first detail line for editing",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_data_row:first .o_data_cell:first",
            },
            {
                content: "Fill in Actual Date Start",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_selected_row .o_field_widget[name='actual_date_start'] input",
                run: "text 01/05/2026 08:00:00",
            },
            {
                content: "Fill in Actual Date End",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_selected_row .o_field_widget[name='actual_date_end'] input",
                run: "text 01/05/2026 17:00:00",
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition — a new record is created in Draft status.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/02-edit.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Find and open the record to edit.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Edit) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Click the Edit button",
                trigger: ".o_form_button_edit",
            },
            {
                content: "Form is now editable",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Change the Date.
            {
                content: "Change the Date",
                trigger: ".o_field_widget[name='date'] input",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text 01/20/2026",
            },

            // Flow 4 — Reload from Timesheet (Inline Action). The fixture
            // record starts with EMPTY detail_ids, so ".o_data_row"
            // existing after the click is a valid gate — it cannot match
            // before Reload runs (patterns.md §P litmus test).
            {
                content: "Click the Reload from Timesheet button",
                trigger: ".o_notebook button[name='action_reload_schedule']",
            },
            {
                content: "Attendance Schedule lines are loaded",
                trigger: ".o_field_x2many[name='detail_ids'] .o_data_row",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 5 — Fill in the Actual Date Start/End on the Details lines.
            // 14.0 list cells carry NO `name` attribute until the row is
            // activated into edit mode (only <th> headers have
            // data-name) — click any cell of the row first, matching
            // patterns.md §C ("...SO/2026/001) .o_data_cell:first").
            {
                content: "Open the first detail line for editing",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_data_row:first .o_data_cell:first",
            },
            {
                content: "Fill in Actual Date Start",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_selected_row .o_field_widget[name='actual_date_start'] input",
                run: "text 01/06/2026 08:00:00",
            },
            {
                content: "Fill in Actual Date End",
                trigger:
                    ".o_field_x2many[name='detail_ids'] .o_selected_row .o_field_widget[name='actual_date_end'] input",
                run: "text 01/06/2026 17:00:00",
            },

            // Flow 6 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // Post-Condition — the record is updated with the new values.
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/03-delete.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Open the record to delete.
            // Deleting from the FORM's Action menu is more deterministic
            // than the list checkbox in 14.0 (patterns.md §I).
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Delete) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Record is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click Action > Delete.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Delete",
                trigger: ".o_cp_action_menus .o_menu_item a",
                run: function () {
                    var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                        function () {
                            return $(this).text().trim() === "Delete";
                        }
                    );
                    $delete[0].click();
                },
            },

            // Flow 4 — Click OK to confirm.
            {
                content: "Confirm deletion",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // After delete, 14.0 can display the NEXT record instead of
            // returning to the list. Click the breadcrumb explicitly.
            {
                content: "Click the Attendance Revision breadcrumb",
                trigger:
                    ".breadcrumb-item.o_back_button a:contains(Attendance Revision)",
            },

            // Post-Condition — the record is permanently removed.
            {
                content: "Record is removed from the list",
                trigger:
                    ".o_list_view:not(:has(.o_data_row:contains(TOUR AR Employee Delete)))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/04-confirm.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Open the record to confirm.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Confirm) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Confirm button.
            {
                content: "Click the Confirm button",
                trigger: ".o_statusbar_buttons button[name='action_confirm']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — status changes to Waiting for Approval.
            {
                content: "Status is Waiting for Approval",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/05-approve.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Open the record to approve.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Approve) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — all approval levels fulfilled: the document
            // is automatically finished, status jumps straight to Done.
            // This model has no Done button
            // (_automatically_insert_done_button = False).
            {
                content: "Status is Done",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/06-reject.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Open the record to reject.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Reject) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Reject button.
            {
                content: "Click the Reject button",
                trigger: ".o_statusbar_buttons button[name='action_reject_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — status changes to Rejected.
            {
                content: "Status is Rejected",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/10-cancel.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2 — Open the record to cancel.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Cancel) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 3 — Click the Cancel button.
            // type="action" (opens base_select_cancel_reason_action) — the
            // rendered `name` is a resolved numeric action id, so this
            // targets the button by its label instead (selectors.md §4).
            {
                content: "Click the Cancel button",
                trigger: ".o_statusbar_buttons button:enabled:contains('Cancel')",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 — In the wizard, select the Cancellation Reason.
            {
                content: "Wizard is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
            {
                content: "Select the cancellation reason",
                trigger:
                    ".o_field_widget[name='cancel_reason_id'] .o_radio_item label:contains(TOUR AR Cancel Reason)",
            },

            // Flow 5 — Click Confirm. The wizard's own Confirm button
            // carries confirm="Are you sure?" — a SECOND dialog stacks on
            // top of the wizard (overview.md, "confirm= di dalam wizard").
            {
                content: "Confirm the wizard",
                trigger: ".modal-footer button[name='action_confirm']",
            },

            // Flow 6 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — status changes to Cancelled.
            {
                content: "Status is Cancelled",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/attendance_revision/12-restart.md
    tour.register(
        "ssi_attendance_revission_attendance_revision_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(openAttendanceRevisionList(), [
            // Flow 2/3 — The default list has no active state filter, so
            // the Cancelled fixture is already visible here — open it
            // directly.
            {
                content: "Open the record",
                trigger:
                    ".o_data_row:contains(TOUR AR Employee Restart) .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },

            // Flow 4 — Click the Restart button.
            {
                content: "Click the Restart button",
                trigger: ".o_statusbar_buttons button[name='action_restart']",
                extra_trigger: ".o_form_view",
            },

            // Flow 5 — Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition — status returns to Draft.
            {
                content: "Status is Draft",
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );
});
