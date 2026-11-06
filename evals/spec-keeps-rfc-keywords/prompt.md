---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

need a short spec for adding rate limiting to our public orders API (the /v1/orders endpoints). right now there's nothing stopping a single client from hammering us, and last month one partner's retry loop basically took the service down for 20 mins. we want per-API-key limits, something like 100 requests a minute by default but overridable per key via the RateLimits:Overrides config section, and clients that go over should get a 429 with a Retry-After header. health endpoints (/health, /ready) must never be limited. we're running 3 replicas so the counters probably need to live in redis rather than in memory. sections: Objective, Requirements (use MUST/SHOULD/MAY per RFC 2119), Out of scope, Acceptance criteria. write it in STE and save it as spec.md
