# Confirm Attendance Revision

> **Module:** ssi_attendance_revission
>
> **Model:** `attendance_revision`
>
> **Menu:** Human Resource > Timesheets > Attendance Revision
>
> **Actor:** user in group _Attendance Revision — User_
>
> **State:** `draft` → `confirm`
>
> **Requires:** `01-create`

## Pre-Condition

- **Record:** Status is **Draft**.
- **Config:** An active `policy.template` for this model grants `confirm_ok` for state
  `draft` to the actor's group (see the _Standard_ `policy.template`).
- **Config:** An active `approval.template` for this model matches this record and has
  at least one approver level (see the _Standard_ `approval.template`, which defines a
  single sequential level approved by group _Attendance Revision — Validator_).
- **Access:** User is in group _Attendance Revision — User_.

## Flow

1. Open the **Human Resource > Timesheets > Attendance Revision** menu.
2. Open the record to confirm.
3. Click the **Confirm** button.
4. Click **OK** on the confirmation dialog.

## Post-Condition

- Status changes to **Waiting for Approval**.
- Approval records are created for each approver level defined by the _Standard_
  `approval.template`.
- Once every approval level has approved (see `05-approve`), the document transitions to
  **Done** automatically — there is no separate Finish/Done button, and no dedicated IK
  for this transition. The document number is also assigned automatically at this point
  (unless already manually assigned).
