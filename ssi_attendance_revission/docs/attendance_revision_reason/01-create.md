# Create Attendance Revision Reason

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision_reason`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Revision >
> Attendance Revision Reason
>
> **Actor:** user in group _Attendance Revision Reason_

## Pre-Condition

- **Access:** User is in group _Attendance Revision Reason_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Revision >
   Attendance Revision Reason** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the required fields:
   - **Name** _(required)_: Enter the name of the attendance revision reason.
   - **Code** _(required)_: Enter a unique code identifying this reason. Enter **/** to
     generate the code automatically later using the **Generate Code** button.
4. Click **Save**.

## Post-Condition

- A new attendance revision reason record is created and active.
- The new reason appears in the Attendance Revision Reason list view.
- The new reason becomes selectable as the **Reason** on `attendance_revision` records
  (see `attendance_revision/01-create.md`), subject to the filtering configured on the
  selected **Type** (see `attendance_revision_type/01-create.md`).
