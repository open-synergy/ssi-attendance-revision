# Edit Attendance Revision

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision`
>
> **Menu:** Human Resource > Timesheets > Attendance Revision
>
> **Actor:** user in group _Attendance Revision — User_
>
> **Requires:** `01-create`
>
> **Inline Actions:** `action_reload_schedule` — **Reload from Timesheet** button

## Pre-Condition

- **Record:** Status is **Draft**.
- **Access:** User is in group _Attendance Revision — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Revision** menu.
2. Find and open the record to edit.
3. Change **Employee**, **Date**, **Type**, **Reason**, or **# Timesheet** as needed —
   the same constraints described in `01-create` apply.
4. Optionally, open the **Details** tab and click the **Reload from Timesheet** button.
   _(Inline Action — only enabled while the document is in Draft.)_ This clears the
   current detail lines and rebuilds them from the selected **# Timesheet**'s attendance
   schedules, discarding any **Actual Date Start**/**Actual Date End** already entered.
5. Change the **Actual Date Start**/**Actual Date End** on the **Details** lines as
   needed.
6. Click **Save**.

## Post-Condition

- The record is updated with the new values.
