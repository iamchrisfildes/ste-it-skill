---
tags: [skill-creator]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

can you turn these notes into the "Why an outbox?" section of our README, in STE? it's background for new devs, not instructions. save it as why-outbox.md

notes:
- we used to publish OrderPlaced straight to Service Bus from the controller after SaveChanges. if the publish failed (it did, a lot, during the Service Bus outage in March) the order was saved but nobody downstream ever heard about it. also the other way round - sometimes the publish went out and then SaveChanges threw, so billing charged for orders that didn't exist
- now the controller writes the order and an OutboxMessages row in the same transaction, so they either both happen or neither does
- OutboxPublisher is a background service that polls OutboxMessages every 5s and pushes anything unsent to Service Bus, then marks it sent
- tradeoffs: up to ~5s extra latency before downstream sees the event, one more table to keep an eye on, and the publisher can send the same message twice if it crashes between the send and the mark-as-sent, so every consumer has to be idempotent (we dedupe on MessageId)
- we looked at distributed transactions (MSDTC) but they're not supported on Service Bus and would've tied us to Windows anyway
