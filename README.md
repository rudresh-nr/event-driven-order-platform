# Full-Stack AI-Enabled Platform
Django · React · REST · PostgreSQL · Docker

## Overview

This project is a production-grade full-stack web application built using Django (Backend) and React (Frontend).
It demonstrates clean architecture, scalable backend design, secure APIs, and modern frontend practices, with optional GenAI integration for intelligent features.

### Key Objectives
- Design a scalable backend architecture using Django
- Implement secure, versioned REST APIs
- Build a clean and maintainable React frontend
- Demonstrate real-world system design decisions
- Showcase production concerns: auth, performance, testing, deployment
### Tech Stack
#### Backend

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Celery (async tasks)
- Redis (caching / queues)

#### Frontend
- React
- TypeScript
- Axios
- React Query
- Tailwind CSS

#### Infrastructure
- Docker & Docker Compose
- Nginx
- GitHub Actions (CI/CD)

<img width="442" height="238" alt="Screenshot from 2026-01-14 15-06-41" src="https://github.com/user-attachments/assets/714eca67-e9a6-4cec-b067-023d37583c59" />

#### Backend Architecture Principles
- Separation of Concerns
- Thin Views, Fat Services
- Domain-driven structure (not “fat models”)
- Explicit business logic layer
- Framework treated as infrastructure, not core logic

## Features

### Core Features
- User authentication & authorization (JWT)
- Role-based access control
- CRUD APIs with pagination & filtering
- Secure API versioning (/api/v1/)
- Centralized error handling

### Advanced Features
- Async background jobs using Celery
- Caching for high-read endpoints
- Rate limiting & security headers
- Optimized database queries
- Modular, testable frontend components

### GenAI Integration
- AI-powered search or recommendations
- Prompt orchestration via service layer
- Model-agnostic AI provider abstraction



============#########===========================##################==================#################===




## Eventual Consistency
"Orders appear immediately after creation, but user-facing order history may lag briefly while events are processed asynchronously. This trade-off allows the system to remain available under failure and scale read workloads independently."

## Handling cache failures
The read path tolerates cache failures by falling back to database-backed projections. Redis is treated as a best-effort performance optimization rather than a required dependency.

## Failure & Recovery
This system is explicitly designed to tolerate partial failures and recover
without data loss or manual intervention.

### Publisher Failure (Async Infrastructure Down)
If the event publisher or message broker is unavailable:
- Orders continue to be created synchronously
- Outbox events are persisted with `published = false`
- A backlog accumulates safely in the database

Once the publisher is restored, pending events are published in order.
No committed order state is lost.

### Consumer Failure or Restart
If consumers crash or are restarted:
- Events may be delivered more than once
- Consumers are idempotent and replay-safe
- Duplicate processing does not create duplicate state


Consumers can be safely restarted without coordination.

### Read Model Corruption or Data Loss
Read models are treated as disposable projections:
- Tables can be truncated or dropped
- State is rebuilt by replaying published events
- Reprocessing events is deterministic and safe



The authoritative state is never derived from read models.

### Cache Failure
Redis is used as a best-effort cache:
- Cache outages degrade performance only
- Read requests fall back to database-backed projections
- No correctness or availability guarantees depend on Redis
