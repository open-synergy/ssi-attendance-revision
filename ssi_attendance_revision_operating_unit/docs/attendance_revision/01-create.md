# Create Attendance Revision

> **Module:** ssi_attendance_revision_operating_unit
>
> **Extends:** ssi_attendance_revission — model `attendance_revision`, aksi `01-create`

## Additional Fields

When this module is installed, the create form gains one field, inserted right after
**Company**:

- **Operating Unit**: The operating unit this attendance revision belongs to. Defaults
  to the current user's default operating unit. Only visible/editable to users in the
  _Multi Operating Unit_ group. Not required — change if needed.

## Modified — Record Visibility

- The attendance revision list is now filtered by operating unit (record rule
  `attendance_revision_rule_ou`). A user only sees attendance revisions of operating
  units they are assigned to. This is not a Flow step.
