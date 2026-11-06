---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

can you rewrite this section of our CLAUDE.md in STE? the agent keeps getting it wrong. save it as claude-section.md

## Database migrations

You should generally avoid touching the Migrations folder directly. If you need a schema change, it's best to run `dotnet ef migrations add <Name> --project src/Orders.Data` and let EF generate it. You may also want to run `dotnet ef migrations script` to review the SQL, though that's optional.

Migrations may be squashed before a release, so don't rely on old migration names. The migration scripts in that directory can change under you.

Ideally run `dotnet ef database update` against the local container (ORDERS_DB_CONNECTION should already be set by docker-compose) to check it applies cleanly.

It should take under a minute, but it might take a while the first time.

Never ever run migrations against staging or prod yourself - that's handled by the release pipeline.
