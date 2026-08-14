# Create Attendance Revision Type

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision_type`
>
> **Menu:** Human Resource > Configuration > Attendance > Attendance Revision >
> Attendance Revision Type
>
> **Actor:** user in group _Attendance Revision Type_

## Pre-Condition

- **Access:** User is in group _Attendance Revision Type_.

## Flow

1. Open the **Human Resource > Configuration > Attendance > Attendance Revision >
   Attendance Revision Type** menu.
2. Click the **New** button. **(14.0: "Create")**
3. Fill in the fields:
   - **Name** _(required)_: Enter the name of the attendance revision type.
   - **Code** _(required)_: Enter a unique code identifying this type. Enter **/** to
     generate the code automatically later using the **Generate Code** button.
   - Open the **Reason Configuration** tab:
     - **Reason Selection Method** _(required)_: Choose how allowed **Reason** values
       are determined for this type — **Manual** (pick from a fixed list), **Domain**
       (filter with an Odoo domain expression), or **Python Code** (compute
       programmatically). Defaults to **Domain**.
     - **Reasons**: When **Reason Selection Method** is **Manual**, select the allowed
       `attendance_revision_reason` records.
     - **Reason Domain**: When **Reason Selection Method** is **Domain**, enter the
       domain expression. Defaults to `[]` (all reasons allowed).
     - **Reason Python Code**: When **Reason Selection Method** is **Python Code**,
       enter the code that assigns a list of reason IDs to `result`.
4. Click **Save**.

## Post-Condition

- A new attendance revision type record is created and active.
- The new type appears in the Attendance Revision Type list view.
- The new type becomes selectable as the **Type** on `attendance_revision` records (see
  `attendance_revision/01-create.md`), and its **Reason Selection Method** determines
  which **Reason** values those records may pick.
