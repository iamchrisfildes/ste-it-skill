---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

write a PR description for this, STE please, save as pr.md. the change: InvoiceDateFormatter was calling DateTime.Now instead of using the customer's time zone, so invoices generated just after midnight UTC for customers in UTC-5 to UTC-8 showed the next day's date. about 2% of US invoices last month had the wrong date. fix injects TimeProvider and converts to the customer's TimeZoneId before formatting. added unit tests for UTC-8, UTC, and UTC+13 around midnight, plus a DST changeover case. no db changes, no API contract changes.
