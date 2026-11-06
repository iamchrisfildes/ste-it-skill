---
type: llm
focus: trace
weight: 1
---

why-outbox.md keeps all the reasons and trade-offs from the notes: lost events when the publish failed, events for orders that were not saved, one transaction for the order and the OutboxMessages row, polling every 5 seconds, up to about 5 seconds of extra latency, one more table to monitor, possible duplicate sends with dedupe on MessageId, and MSDTC rejected because Service Bus does not support it and it ties the service to Windows
