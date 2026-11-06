---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

break this feature down into a task list for the team. feature: let users export their order history as CSV from the account page. needs a new GET /v1/account/orders/export endpoint that streams the CSV (orders can be in the tens of thousands for big business accounts so don't load it all into memory), a button on the account page, rate limit it to 5 exports per hour per user, and an audit log entry each time someone exports. use exactly this template for each task and nothing else:

### Task N: <title>
**Description:** <what and why>
**Acceptance criteria:**
- [ ] <criterion>
**Verification:** <how to check it>
**Depends on:** <task numbers or "None">

use STE. save as tasks.md
