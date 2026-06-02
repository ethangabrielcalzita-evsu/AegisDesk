# AegisDesk — System Flow & Application Walkthrough

## Project Overview

AegisDesk is an internal enterprise tool for logging IT support tickets and security breach incidents.
The system strictly follows the **NIST Incident Response Life Cycle** as its core workflow model,
mapping every ticket's progress through Preparation → Detection → Containment → Recovery → Closed.

It serves two types of users:
- **Employees** — report IT or security incidents via a web form
- **IT Managers / SecOps** — triage, update, and close incidents through a management dashboard

A **JWT-protected REST API** also allows remote monitoring tools to automatically generate tickets
without going through the web UI.

---

## User Flow

### 1. Employee — Submitting an Incident

```
[ Employee visits / ]
        │
        ▼
[ Redirected to /incidents/submit/ ]
        │
        ▼
[ Fills in the ticket form ]
  - Title
  - Description
  - Category: IT Support / Security Breach
  - Affected Asset (Server, Workstation, Network, Cloud)
  - Severity: Low / Medium / High / Critical
  - NIST Stage (defaults to: 1. Preparation)
        │
        ▼
[ Rate limit check — max 5 submissions/min per IP ]
  ┌─────────────────────────────────────┐
  │ Limit exceeded?                     │
  │  YES → Show error, block submission │
  │  NO  → Continue                     │
  └─────────────────────────────────────┘
        │
        ▼
[ Ticket saved to database ]
[ Audit log entry written: "New incident registered" ]
        │
        ▼
[ Redirected to /incidents/submit/success/ ]
```

---

### 2. Employee — Viewing Own Tickets

```
[ Employee navigates to /incidents/my-tickets/ ]
        │
        ▼
[ System filters tickets where reported_by = current user ]
        │
        ▼
[ List displayed with title, severity, NIST stage, date ]
        │
        ▼
[ Employee clicks a ticket → /incidents/ticket/<id>/ ]
  ┌──────────────────────────────────────────┐
  │ Owner check:                             │
  │  reported_by = current user? → Show      │
  │  Not owner and not manager? → 403 page   │
  └──────────────────────────────────────────┘
```

---

### 3. IT Manager — Triaging Incidents

```
[ Manager logs in → redirected to /incidents/manager/dashboard/ ]
        │
        ▼
[ Dashboard displays:
  - Total open / closed tickets
  - Critical & High severity count
  - NIST stage breakdown (count per stage)
  - Severity breakdown (Critical / High / Medium / Low) ]
        │
        ▼
[ Manager navigates to /incidents/manager/tickets/ ]
        │
        ▼
[ All open tickets listed (excludes CLOSED stage) ]
        │
  ┌─────────────────────────────────────────────────┐
  │ Option A: Update a single ticket                │
  │  → Click ticket → /incidents/manager/tickets/   │
  │    <id>/update/                                 │
  │  → Change NIST stage via dropdown               │
  │  → Save → Audit log entry written:              │
  │    "Stage altered from X to Y"                  │
  │  → Redirected to ticket detail page             │
  └─────────────────────────────────────────────────┘
        │
  ┌─────────────────────────────────────────────────┐
  │ Option B: Bulk close resolved tickets           │
  │  → Select multiple tickets via checkboxes       │
  │  → Click "Bulk Close"                           │
  │  → All selected tickets set to CLOSED           │
  │  → Audit log entry written per ticket           │
  └─────────────────────────────────────────────────┘
```

---

### 4. Remote Monitoring Tool — API Ticket Ingestion

```
[ Monitoring tool starts up ]
        │
        ▼
[ POST /incidents/api/token/
  Body: { "username": "...", "password": "..." } ]
        │
        ▼
[ Server returns access_token + refresh_token ]
        │
        ▼
[ Tool detects an incident event ]
        │
        ▼
[ POST /incidents/api/v1/log-incident/
  Header: Authorization: Bearer <access_token>
  Body: {
    "title": "...",
    "description": "...",
    "severity": "HIGH",
    "affected_asset": <asset_id>,
    "nist_stage": "DETECTION_ANALYSIS"
  } ]
        │
        ▼
[ Server validates token → validates payload ]
  ┌──────────────────────────────────────┐
  │ No token?       → 401 Unauthorized  │
  │ Missing field?  → 400 Bad Request   │
  │ Valid?          → Continue          │
  └──────────────────────────────────────┘
        │
        ▼
[ Ticket saved — reported_by = null
  Audit log: attributed to "Remote_Monitoring_API_Agent" ]
        │
        ▼
[ Response: 201 { "status": "Incident logged successfully" } ]
        │
        ▼
[ When access_token expires:
  POST /incidents/api/token/refresh/
  Body: { "refresh": "<refresh_token>" }
  → New access_token returned, no re-login needed ]
```

---

## NIST Incident Response Life Cycle — Ticket Progression

Every ticket moves through the following stages. Managers update the stage as the response progresses.

```
  ┌─────────────────────┐
  │  1. PREPARATION     │  ← Default stage when ticket is created
  └────────┬────────────┘
           │ Incident confirmed and under investigation
           ▼
  ┌─────────────────────┐
  │  2. DETECTION &     │
  │     ANALYSIS        │  ← Severity assessed, scope determined
  └────────┬────────────┘
           │ Response actions initiated
           ▼
  ┌─────────────────────┐
  │  3. CONTAINMENT,    │
  │     ERADICATION &   │  ← Threat isolated, systems cleaned
  │     RECOVERY        │
  └────────┬────────────┘
           │ Systems restored, lessons documented
           ▼
  ┌─────────────────────┐
  │  4. POST-INCIDENT   │  ← Review completed, report filed
  │     ACTIVITY        │
  └────────┬────────────┘
           │ Fully resolved
           ▼
  ┌─────────────────────┐
  │  5. CLOSED          │  ← Ticket resolved and archived
  └─────────────────────┘
```

Every stage change is recorded in `aegis_audit.log` with a timestamp and the username of the manager
who made the change — forming a strict chain of custody.

---

## Security Controls in the Flow

| Control | Where it applies | What it does |
|---|---|---|
| `@login_required` | All web views | Redirects unauthenticated users to login page |
| `is_staff` check | All manager views | Returns 403 if a non-manager accesses manager pages |
| Rate limiting (5/min/IP) | `submit_ticket` view | Blocks submission spam without crashing the app |
| JWT authentication | All API endpoints | Rejects requests without a valid Bearer token |
| Audit logging | Every ticket save | Records creation and stage changes with user attribution |
| CSRF protection | All POST forms | Django middleware blocks cross-site form submissions |
| Secure cookies | Session & CSRF cookies | HTTP-only; secure flag enabled in production |
| `X-Frame-Options: DENY` | All responses | Prevents clickjacking |

---

## Authentication Flow Summary

```
Web Users                          API Clients
─────────────────                  ──────────────────────
Visit /accounts/login/             POST /incidents/api/token/
Enter username + password          Receive access + refresh tokens
Django session created             Use Bearer token on each request
Session cookie stored              Refresh token renews access token
All views check session            Expired token → 401 → re-request
```

---

## Chain of Custody — Audit Log

Every incident creation and stage change produces a log entry in `aegis_audit.log`:

```
INFO 2026-06-02 10:15:33 models [User:jsmith] New incident registered. Title: 'VPN Outage' for Asset: Firewall-01
INFO 2026-06-02 11:42:07 models [User:it_manager] Ticket #14 modified. Stage altered from 'PREPARATION' to 'DETECTION_ANALYSIS'.
INFO 2026-06-02 14:05:51 models [User:Remote_Monitoring_API_Agent] New incident registered. Title: 'CPU Spike on Server-03' for Asset: Server-03
```

This log is the authoritative record of who did what and when — it cannot be modified through the UI.
