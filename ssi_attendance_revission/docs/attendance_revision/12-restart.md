# Restart Attendance Revision

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision`
>
> **Menu:** Human Resource > Timesheets > Attendance Revision
>
> **Actor:** user in group _Attendance Revision — User_
>
> **State:** `cancel` → `draft`
>
> **Requires:** `10-cancel`

## Pre-Condition

- **Record:** Status is **Cancelled**.
- **Config:** An active `policy.template` for this model grants `restart_ok` for state
  `cancel` to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Attendance Revision — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Revision** menu.
2. Open the record to restart.
3. Click the **Restart** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status returns to **Draft**.
