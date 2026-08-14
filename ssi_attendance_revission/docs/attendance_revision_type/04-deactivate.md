# Deactivate Attendance Revision Type

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision_type`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Revision >
> Attendance Revision Type
>
> **Actor:** user in group _Attendance Revision Type_
>
> **Active:** `true` → `false`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** The record is currently active.
- **Access:** User is in group _Attendance Revision Type_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Revision >
   Attendance Revision Type** menu.
2. Select one or more records to deactivate (check the checkbox).
3. Click **Action** > **Archive**.
4. Click **OK** to confirm.

## Post-Condition

- The records are archived and no longer appear in the default list view.
- Deactivated types cannot be selected as the **Type** on a new attendance revision (see
  `attendance_revision/01-create.md`).
