---
name: apache-kafka-broker
description: "Designing, producing, or consuming Kafka events, handling serialization formats, managing consumer groups, and tuning brokers."
---

# Goal
Build high-throughput, event-driven integrations with Apache Kafka, guaranteeing reliable delivery guarantees and concurrent offset processing.

# Instructions
1. **Idempotence & Delivery Guarantees**: Enforce consumer-side idempotency to guard against duplicate deliveries. Use unique IDs (like `game_id` or event IDs) to de-duplicate processing.
2. **Graceful Shutdown**: Always handle SIGTERM/SIGINT signals to cleanly close consumer connections, ensuring offsets are fully committed and rebalances are handled cleanly.
3. **Structured Schemas**: Use standard serialization patterns (like JSON or Avro) to decouple producers and consumers. Always map payloads strictly to types/structs.
4. **Consumer Group Allocation**: Enforce distinct group IDs (e.g. `statsapp_group`) to orchestrate load-balancing across consumer pods.
5. **Batching & Buffering**: Optimize producer settings (like `linger.ms` and compression type) to balance latency and throughput during high-concurrency event publishing.

# Constraints
- Never commit offsets before message processing is complete to prevent data loss.
- Do not hardcode topic names across different environment configurations; load them via configuration variables.
