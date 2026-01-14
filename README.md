## event-driven-order-platform
An event-driven order platform showcasing strong write consistency, asynchronous processing, and derived read models with explicit failure handling.

## System Guarantees

1. Strong Consistency for Writes
   All order creation and state transitions are atomic and strongly consistent.
   - Each order is written using a single database transaction
   - Either the entire write succeeds, or nothing is persisted
   - No partial order states are visible to clients

2. Event Emission Is Transactionally Safe
   - Events are persisted in the same transaction as domain state
   - No event is published without a corresponding committed state
   - Dual-write inconsistencies are explicitly avoided

3. Read Models Are Eventually Consistent
   All query-facing views are derived asynchronously from events.
   - Read models may temporarily lag behind the write model
   - The system favors availability and low read latency for queries
   - Eventual consistency is explicit and documented

4. Consumers Are Idempotent and Replayable
   Event consumers are designed to be idempotent and replay-safe.
   - Duplicate events do not corrupt derived state
   - Read models can be fully rebuilt by replaying the event log
   - Offset management favors at-least-once delivery

5. Writes Are Not Blocked by Downstream Failures
   Failures in event publishing, consumers, or read models never block order creation.
   - Orders can be created even if the event system is unavailable
   - Backlogs are drained when downstream systems recover
   - The system degrades gracefully under partial failure

## Explicit Non-Goals and Trade-Offs
1. No Global Strong Consistency
   Non-goal
   - The system does not provide strong consistency across all read paths.
     
   Trade-off
   - Read models may return stale data briefly.

   Why this is intentional
   - Enforcing global consistency would reduce availability and increase latency. The system explicitly optimizes for correctness on writes and scalability on reads.
   
  
