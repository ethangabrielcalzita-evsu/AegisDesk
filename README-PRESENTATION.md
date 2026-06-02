# AegisDesk PowerPoint Presentation Outline

## Cover Page
- **Final Project Requirement**
- **IT363 - Information Assurance and Security 1**
- **SY2025-2026-SEM2**
- **Project:** AegisDesk: IT Helpdesk & Security Incident Tracker
- **Presenters:**
  - Shan Silvestrece
  - Chris Rodrigo
  - Robert Balintec
  - Ethan Calzita
  - Christian Catada

---

## Slide 2: Presentation Outline
1. Project Overview
2. Objectives
3. Problem Statement
4. Solution Approach
5. System Architecture
6. Key Features
7. Data Model and NIST Mapping
8. Security Controls
9. API Integration
10. Demo Flow
11. Implementation Details
12. Challenges and Lessons Learned
13. Conclusion
14. References

---

## Slide 3: Objectives
- Build an enterprise-ready tool for IT support ticketing and incident response.
- Enforce the NIST Incident Response lifecycle across the database and workflows.
- Protect submission endpoints from abuse using rate limiting.
- Enable JWT-secured API access for automated monitoring and incident creation.
- Provide audit logging for strict chain of custody on ticket updates.

---

## Slide 4: Problem Statement
- IT teams need a centralized, secure system for tracking helpdesk and security incidents.
- Existing solutions may not align directly with NIST incident response stages.
- Attackers can spam ticket submission endpoints, risking denial-of-service and false incident noise.
- Remote monitoring systems need a secure API to create incidents automatically.

---

## Slide 5: Solution Overview
- AegisDesk is a Django web application that combines IT helpdesk and security incident management.
- Ticket entries are mapped to NIST stages in the database schema.
- Security features include rate limiting and audit logging.
- A JWT-protected REST API supports external incident creation and monitoring.

---

## Slide 6: System Architecture
- Frontend: Django templates, forms, and Bootstrap/Crispy Forms UI.
- Backend: Django app with models for assets and incident tickets.
- Security layers:
  - User authentication
  - Django RateLimit on ticket submission
  - JWT authentication for API endpoints
- Persistence: SQLite database for development (scalable to PostgreSQL in production).

---

## Slide 7: Key Features
- **Helpdesk ticket submission** with incident details.
- **NIST-aligned incident stages** for lifecycle tracking.
- **Severity levels**: Low, Medium, High, Critical.
- **Asset management** for servers, workstations, network devices, and cloud resources.
- **Authentication and admin management** via Django admin.
- **Rate limiting** to prevent ticket submission abuse.
- **JWT API** for integration with external monitoring tools.

---

## Slide 8: Data Model and NIST Mapping
- `Asset` model stores networked resource details.
- `IncidentTicket` model contains:
  - Title
  - Description
  - Affected asset
  - Severity level
  - NIST stage selection
  - Reporter association
  - Timestamps for audit traceability
- NIST stages mapped into choice fields:
  - Preparation
  - Detection & Analysis
  - Containment, Eradication & Recovery
  - Post-Incident Activity
  - Resolved / Closed

---

## Slide 9: Security Controls
- `django-ratelimit` protects the ticket submission endpoint from DoS and spam.
- Rate configured at **5 tickets per minute per IP address**.
- If exceeded, submission is blocked with a 403 response.
- Python logging records each ticket creation and update event.
- Admin authentication enforced for sensitive management actions.

---

## Slide 10: API Integration
- JWT authentication for remote access to the incident endpoint.
- Allows external monitoring tools to create incident tickets automatically.
- Example workflow:
  - Monitoring system detects a security alert
  - It requests a token using username/password
  - It posts incident details to `/api/incidents/`
- Supports secure programmatic incident creation.

---

## Slide 11: Demo Flow
1. Log in as an authenticated user.
2. Submit a new support or security incident ticket.
3. Verify the ticket is saved with the correct NIST stage.
4. Inspect the incident in the admin panel.
5. Simulate API incident creation using JWT token.
6. Demonstrate rate limiting by submitting too many tickets quickly.

---

## Slide 12: Implementation Details
- Framework: Django 5.0.6 with Django REST Framework.
- Dependencies:
  - `djangorestframework`
  - `djangorestframework-simplejwt`
  - `django-ratelimit`
  - `crispy-forms`, `crispy-bootstrap5`
- Database: SQLite for development, extensible to PostgreSQL.
- Deployable as a web app with standard Django production practices.

---

## Slide 13: Challenges and Lessons Learned
- Mapping the incident workflow to NIST stages required careful schema design.
- Balancing usability with security controls in the submission flow.
- Implementing audit logging and rate limiting together improved incident integrity.
- Ensuring the JWT API remained secure while still accessible for automation.

---

## Slide 14: Conclusion
- AegisDesk delivers a secure, NIST-aligned incident tracking system.
- The project integrates IT helpdesk workflows with security response lifecycle control.
- Built with Django, it supports user management, audit logging, and API automation.
- Future work can include advanced reporting, asset dashboards, and ticket history analytics.

---

## Slide 15: References
- NIST Computer Security Incident Handling Guide
- Django documentation
- Django REST Framework documentation
- django-ratelimit package documentation
- JWT authentication best practices
