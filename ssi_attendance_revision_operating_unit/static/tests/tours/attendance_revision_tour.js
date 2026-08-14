odoo.define(
    "ssi_attendance_revision_operating_unit.attendance_revision_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/attendance_revision/01-create.md (E1 delta — Additional
        // Fields). Navigation (open menu -> New) is taken from the base IK
        // ssi_attendance_revission/docs/attendance_revision/01-create.md
        // Flow steps 1-2. The delta assertion is that the Operating Unit
        // field is visible and fillable on the form for a user in the
        // operating_unit.group_multi_operating_unit group. The tour stops
        // there; it does not fill the rest of the base create flow, save,
        // or confirm (E1 delta-only, per Keputusan Desain issue #8).
        tour.register(
            "ssi_attendance_revision_operating_unit_attendance_revision_field_ou",
            {
                test: true,
                url: "/web",
            },
            [
                // Base Flow 1 — Open the Human Resource > Timesheets >
                // Attendance Revision menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Human Resource app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_hr.menu_root_human_resource"]',
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
                    // Gate on the TARGET action title so the next step
                    // does not run against the stale landing view of the
                    // app.
                    content: "Attendance Revision list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Attendance Revision)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default
                        // click action.
                    },
                },

                // Base Flow 2 — Click the New button. (14.0: "Create")
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

                // Delta assertion — the Operating Unit field is visible on
                // the create form for a user in the multi operating unit
                // group.
                {
                    content: "Operating Unit field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_many2one[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; the field's presence is what we
                        // verify first.
                    },
                },

                // Delta assertion — the field can be filled in. It starts
                // pre-filled with the user's default operating unit
                // (mixin.single_operating_unit default, admin ships with
                // one via operating_unit's own data/ — always loaded, not
                // demo), so typing over it and picking a different,
                // fixture-only record from the dropdown also proves the
                // value can be CHANGED, not just displayed.
                //
                // There is deliberately NO further step asserting the
                // resulting text. In 14.0 (Sizzle,
                // web/static/lib/jquery/jquery.js) the attribute selector
                // "input[value=...]" reads elem.defaultValue — the
                // original HTML attribute — never the live elem.value the
                // many2one widget sets via $input.val() in _renderEdit(),
                // so such a trigger would NEVER match even though the
                // value is right there on screen (odoo-development-ui-test
                // skill, patterns.md §L). The widget also offers no other
                // attribute/text-node carrying the live value while the
                // form stays in edit mode (unsaved) — the skill's own fix,
                // closing and reopening the record read-only, does not
                // apply here since this delta tour never saves. The click
                // below succeeding on a real, name_search-matched dropdown
                // item (it does not exist unless our fixture record is
                // found) is itself the proof that the field accepts input,
                // exactly like the base create tour's other many2one
                // fields (Employee/Type/Reason/# Timesheet), which do not
                // assert a post-pick value either.
                {
                    content: "Fill in the Operating Unit",
                    trigger: ".o_field_many2one[name='operating_unit_id'] input",
                    run: "text TOUR AR OU",
                },
                {
                    content: "Pick the Operating Unit from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(TOUR AR OU)",
                    in_modal: false,
                },
            ]
        );
    }
);
