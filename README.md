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
