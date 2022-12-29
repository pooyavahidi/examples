# IAM Policy Examples

## EnforceMFA
This policy enforces that all the actions on all the resources to have MFA token present, and age of the token is less than certain defined time (e.g. 1 hour).

> Note that the `aws:MultiFactorAuthAge` key is not present if MFA was not used. So, we can simplify this example and just test the age.
