# Deactivate Attendance Revision Reason

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Revision >
> Attendance Revision Reason
>
> **Actor:** user in group _Attendance Revision Reason_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Revision Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Revision >
   Attendance Revision Reason** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated reasons cannot be selected as the **Reason** on a new attendance revision
  (see `attendance_revision/01-create.md`).
