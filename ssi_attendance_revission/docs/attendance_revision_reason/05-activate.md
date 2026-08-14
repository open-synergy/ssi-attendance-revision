# Activate Attendance Revision Reason

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Revision >
> Attendance Revision Reason
>
> **Actor:** user in group _Attendance Revision Reason_
>
> **Active:** `false` → `true`
>
> **Requires:** `04-deactivate`

## Pre-Condition

- **Record:** The record is currently archived.
- **Access:** User is in group _Attendance Revision Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Revision >
   Attendance Revision Reason** menu.
2. Enable the **Archived** filter in the search bar.
3. Select one or more records to reactivate (check the checkbox).
4. Click **Action** > **Unarchive**.
5. Click **OK** to confirm.

## Post-Condition

- The records are restored and appear again in the default list view.
- The reasons can be selected again as the **Reason** on a new attendance revision.
