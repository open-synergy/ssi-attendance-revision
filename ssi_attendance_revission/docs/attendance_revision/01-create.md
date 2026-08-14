# Create Attendance Revision

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision`
>
> **Menu:** Human Resource > Timesheets > Attendance Revision
>
> **Actor:** user in group _Attendance Revision — User_
>
> **State:** `—` → `draft`
>
> **Inline Actions:** `action_reload_schedule` — **Reload from Timesheet** button

## Pre-Condition

- **Config:** An active `policy.template` for this model grants `confirm_ok` (state
  `draft`), `manual_number_ok` (state `draft`), `restart_approval_ok` (state `reject`),
  `cancel_ok` (states `draft`, `confirm`), and `restart_ok` (state `cancel`) to the
  relevant groups — see the _Standard_ `policy.template` shipped with this module. Both
  `restart_ok` and `restart_approval_ok` use `mixin.policy` (`use_group`/additional
  Python code) to decide who may act.
- **Config:** An active `approval.template` for this model exists — see the _Standard_
  `approval.template`, which defines a single sequential level approved by group
  _Attendance Revision — Validator_ (`mixin.multiple_approval`).
- **Config:** An active `sequence.template` for this model exists — see the _Standard_
  `sequence.template` shipped with this module (`mixin.sequence`).
- **Data:** The **Employee** to select has an `hr.employee` record, and has an
  `hr.timesheet` record in state **Open** (see
  `ssi_timesheet/docs/hr_timesheet/07-start.md`) — an attendance revision cannot be
  saved without an open timesheet for that employee.
- **Access:** User is in group _Attendance Revision — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Revision** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Employee** _(required)_: Automatically filled from the current user's linked
     employee record, if any. Change if needed.
   - **Department**, **Manager**, **Job Position**: Automatically filled from
     **Employee**. Read-only.
   - **Date** _(required)_: Defaults to today. Change if needed.
   - **Type** _(required)_: Select the attendance revision type. Determines which
     **Reason** values are offered.
   - **Reason**: Select a reason, filtered to those allowed by the selected **Type**
     (see `attendance_revision_type/01-create.md`).
   - **# Timesheet** _(required)_: Select the employee's open timesheet, filtered to
     open (`hr.timesheet` state **Open**) timesheets of the selected **Employee**.
4. Open the **Details** tab and click the **Reload from Timesheet** button. _(Inline
   Action — only enabled while the document is in Draft.)_ This clears any existing
   detail lines and rebuilds them, one line per attendance schedule on the selected **#
   Timesheet**, pre-filled with the schedule's original check-in/check-out times.
5. On the reloaded lines, fill in **Actual Date Start** and **Actual Date End** with the
   corrected check-in/check-out datetimes. Repeat for as many lines as needed.
6. Click **Save**.

## Post-Condition

- A new attendance revision record is created in **Draft** status.
- The **Details** tab lists one line per attendance schedule reloaded from the
  timesheet, each showing the original schedule dates alongside the entered actual
  dates.
- The document number stays **/** until the record transitions to **Done**, which
  happens automatically once approval completes (see `04-confirm`) — there is no
  separate Finish/Done button — unless the actor has _Can Input Manual Document Number_
  access.
