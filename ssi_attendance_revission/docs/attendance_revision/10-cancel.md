# Cancel Attendance Revision

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision`
>
> **Menu:** Human Resource > Timesheets > Attendance Revision
>
> **Actor:** user in group _Attendance Revision — User_
>
> **State:** `draft` | `confirm` → `cancel`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft** or **Waiting for Approval**.
- **Config:** An active `policy.template` for this model grants `cancel_ok` for that
  state to the actor's group (see the _Standard_ `policy.template`).
- **Access:** User is in group _Attendance Revision — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Revision** menu.
2. Open the record to cancel.
3. Click the **Cancel** button.
4. In the wizard that appears, select the **Reason**.
5. Click **Confirm**.
6. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Cancelled**.
- The selected **Reason** is recorded on the attendance revision.
