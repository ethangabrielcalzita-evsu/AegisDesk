# AegisDesk: Three-Tier User System Architecture

## Overview

AegisDesk implements a sophisticated role-based access control (RBAC) system with three distinct user types, each with dedicated dashboards, interface features, and security controls. This architecture ensures that each system actor has exactly the tools and visibility they need for their role.

---

## User Type 1: End-User / Employee

### Purpose
Submit IT issues and security incident reports, monitor personal ticket status.

### Interface
- **Dashboard**: `/incidents/employee/dashboard/`
- **Primary View**: Employee Dashboard with personal metrics and recent tickets

### Features
- ✅ Submit new incident tickets via secure form
- ✅ View all personally submitted tickets with status tracking
- ✅ Real-time notification of incident progress (NIST stage updates)
- ✅ Filter tickets by category and severity
- ✅ Access ticket detail pages with chain-of-custody audit trail

### Security Layer
- 🔐 **Authentication**: Django `@login_required` decorator
- 🔐 **Rate Limiting**: 5 submissions per minute per IP address (prevents DoS)
- 🔐 **Data Isolation**: Users only see their own tickets via queryset filter
- 🔐 **CSRF Protection**: All forms use Django CSRF tokens
- 🔐 **Session Security**: HTTP-only cookies, secure flag enabled

### Navigation
```
Login → Home Router → Employee Dashboard
                    ├─ Submit Ticket
                    ├─ My Tickets
                    └─ View Details
```

### Key Views
| URL | View Function | Purpose |
|-----|---|---|
| `/incidents/` | `home()` | Router redirects to employee/manager dashboard |
| `/incidents/employee/dashboard/` | `employee_dashboard()` | Personal metrics and recent tickets |
| `/incidents/submit/` | `submit_ticket()` | Create new incident (rate-limited) |
| `/incidents/my-tickets/` | `my_tickets()` | Filtered list of user's tickets |
| `/incidents/ticket/<id>/` | `ticket_detail()` | Full incident details |

### Dashboard Features
- **Total Submitted**: Lifetime count of all tickets submitted
- **Open/Pending**: Count of tickets not yet resolved (NIST stage ≠ CLOSED)
- **Resolved**: Count of closed tickets (NIST stage = CLOSED)
- **Recent Incidents Table**: Last 5 submitted tickets with quick-view details
  - Ticket ID, title, category (IT Support / Security Breach)
  - Severity with color-coded badges (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)
  - Current NIST stage with emoji indicators
  - Submission date and quick-access link

---

## User Type 2: IT Manager / Security Operations Team

### Purpose
Incident triage, NIST response coordination, and SecOps management.

### Interface
- **Dashboard**: `/incidents/manager/dashboard/`
- **Incident Queue**: `/incidents/manager/tickets/`
- **Admin Console**: `/admin/`

### Features
- ✅ View all incidents across the organization (no data isolation)
- ✅ Triage incidents by severity and category
- ✅ Track incident progress through NIST Incident Response Lifecycle
- ✅ Update NIST stages via custom form with chain-of-custody logging
- ✅ Bulk-close resolved incidents via checkbox selection
- ✅ Real-time severity metrics and incident distribution
- ✅ Access Django admin console for user/permission management

### Security Layer
- 🔐 **Authentication**: Django `@login_required` decorator
- 🔐 **Authorization**: Checked via `user.is_staff` flag
- 🔐 **403 Forbidden**: Non-manager access returns error page
- 🔐 **Audit Logging**: Every stage update logged with user attribution
- 🔐 **CSRF Protection**: All forms use Django CSRF tokens

### Access Control Implementation
```python
def _is_it_manager(user):
    return user.is_authenticated and user.is_staff

@login_required
def manager_dashboard(request):
    if not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)
```

### Navigation
```
Login → Home Router → Manager Dashboard
                    ├─ Incident Queue (all tickets)
                    ├─ Admin Console (user mgmt)
                    └─ Triage & Update Forms
```

### Key Views
| URL | View Function | Purpose |
|-----|---|---|
| `/incidents/` | `home()` | Router redirects to employee/manager dashboard |
| `/incidents/manager/dashboard/` | `manager_dashboard()` | SecOps metrics and NIST workflow |
| `/incidents/manager/tickets/` | `ticket_list()` | All incidents with bulk operations |
| `/incidents/manager/tickets/<id>/update/` | `update_incident()` | Update NIST stage with audit logging |

### Dashboard Features

#### Key Metrics
- **Total Incidents**: Aggregate count of all tickets in system
- **Open/Active**: Tickets not in CLOSED stage (requiring attention)
- **Resolved**: Tickets in CLOSED stage (completed response)
- **Critical/High**: Count of critical + high severity incidents (prioritization signal)

#### NIST Incident Response Lifecycle Breakdown
Displays count in each NIST stage:
1. **Preparation** (📋) - Initial intake and assessment
2. **Detection & Analysis** (🔍) - Security investigation and categorization
3. **Containment, Eradication & Recovery** (🛡️) - Active response phase
4. **Post-Incident Activity** (📊) - Lessons learned and documentation
5. **Resolved/Closed** (✓) - Incident fully resolved

#### Severity Distribution
- 🔴 **Critical**: System down, data breach, immediate threat
- 🟠 **High**: Major impact, requires quick response
- 🟡 **Medium**: Significant but not emergency
- 🟢 **Low**: Minor issues, routine handling

### Incident Queue Features
- **Table View**: All incidents with sortable columns
- **Bulk Operations**: Checkboxes to select multiple tickets and close in batch
- **Stage Update Form**: Change NIST stage for single ticket
- **Filter/Search**: By severity, category, assignee
- **Quick Actions**: Direct access to incident triage

---

## User Type 3: Remote Monitoring Tool (API)

### Purpose
Programmatic incident ingestion from automated monitoring systems, SIEMs, alerting tools.

### Interface
- **API Endpoints** (JWT authenticated)
- **Protocol**: REST/JSON via Django REST Framework

### Features
- ✅ Programmatic incident submission via `/api/v1/log-incident/`
- ✅ Token authentication with JWT (access + refresh tokens)
- ✅ Automated alert ingestion from monitoring tools
- ✅ No UI access (API-only layer)
- ✅ Structured JSON request/response format

### Security Layer
- 🔐 **Authentication**: Simple JWT (access token + refresh token)
- 🔐 **Authorization**: API key validation
- 🔐 **Rate Limiting**: Endpoint-specific rate limits via django-ratelimit
- 🔐 **No Session Access**: Stateless token-based auth
- 🔐 **HTTPS Only** (in production): SSL redirect enforced

### API Endpoints

#### 1. Token Obtain
```
POST /incidents/api/token/
Content-Type: application/json

{
  "username": "monitor_user",
  "password": "secret_key"
}

Response 200:
{
  "access": "eyJhbGciOiJIUzI1NiIs...",
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 2. Token Refresh
```
POST /incidents/api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJhbGciOiJIUzI1NiIs..."
}

Response 200:
{
  "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 3. Log Incident (Automated Submission)
```
POST /incidents/api/v1/log-incident/
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "title": "High CPU usage detected on prod-web-01",
  "description": "CPU usage exceeded 95% for 5 minutes",
  "category": "IT_SUPPORT",
  "severity": "HIGH",
  "affected_asset": "prod-web-01"
}

Response 201:
{
  "id": 42,
  "title": "High CPU usage detected...",
  "severity": "HIGH",
  "nist_stage": "PREPARATION",
  "created_at": "2025-01-24T14:32:15Z"
}
```

### Technology Stack
- **Framework**: Django REST Framework 3.15.1
- **Authentication**: Simple JWT 5.3.1 (djangorestframework-simplejwt)
- **Serializers**: Custom serializers for incident data validation
- **Status Codes**: Standard HTTP (200/201/400/401/403/500)

---

## Home Router Logic

The `home()` view implements the core role-based routing:

```python
@login_required
def home(request):
    """
    Role-based dashboard router:
    - IT/SecOps Managers → manager dashboard
    - End-Users/Employees → employee dashboard
    """
    if _is_it_manager(request.user):
        return redirect('manager_dashboard')
    else:
        return redirect('employee_dashboard')
```

### Flow
1. User logs in → Django redirects to `/incidents/` (home)
2. `home()` view checks `user.is_staff` flag
3. If `is_staff=True` → Redirect to `/incidents/manager/dashboard/`
4. If `is_staff=False` → Redirect to `/incidents/employee/dashboard/`
5. Each dashboard displays role-appropriate interface

---

## Navigation Bar (base.html)

The navbar dynamically renders based on user role:

### For Employees (is_staff=False)
```
AegisDesk | Dashboard | Submit Ticket | My Tickets | [Theme Toggle] | [Employee username] | [Logout]
```

### For Managers (is_staff=True)
```
AegisDesk | Dashboard | Incident Queue | Admin | [Theme Toggle] | [SecOps username] | [Logout]
```

### For Unauthenticated Users
```
AegisDesk | [Theme Toggle] | [Login]
```

### Features
- **Dynamic Links**: Show only relevant links for user role
- **User Type Badge**: Displays "Employee" or "SecOps" next to username
- **Theme Toggle**: Light/dark mode switcher (localStorage persistent)
- **Logout**: POST form with CSRF protection

---

## Database Schema (Relevant Fields)

### User Model (Django Auth)
```
User
├── username (unique)
├── email
├── is_staff (Boolean) ← PRIMARY ROLE DETERMINANT
├── is_authenticated
└── ...
```

### IncidentTicket Model
```
IncidentTicket
├── id (PK)
├── title
├── description
├── category (IT_SUPPORT or SECURITY_BREACH)
├── severity (CRITICAL, HIGH, MEDIUM, LOW)
├── nist_stage (PREPARATION, DETECTION_ANALYSIS, etc.)
├── reported_by (ForeignKey to User) ← EMPLOYEE
├── created_at (DateTime)
├── updated_at (DateTime)
└── affected_asset (ForeignKey to Asset)
```

---

## Audit Logging

Every action is logged with chain-of-custody attributes:

### Format
```
{timestamp} {level} {module} [User:{username}] {message}
```

### Example Entries
```
2025-01-24 14:32:15,123 INFO models [User:john.smith] Ticket #42 modified. Stage altered from 'PREPARATION' to 'DETECTION_ANALYSIS'.
2025-01-24 14:35:42,456 INFO views [User:alice.boss] Bulk closed 3 tickets: [#40, #41, #42]
```

### Log Location
- **File**: `aegis_audit.log` (root project directory)
- **Format**: Python logging with verbose formatter
- **Retention**: Persistent file-based storage for compliance

---

## Security Best Practices Implemented

### 1. Authentication
- ✅ Django session-based for web UI
- ✅ JWT tokens for API access
- ✅ `@login_required` decorator on all protected views
- ✅ Password hashing via Django password validators

### 2. Authorization
- ✅ Role-based access control via `is_staff` flag
- ✅ 403 Forbidden for unauthorized manager access
- ✅ Data isolation (employees see only own tickets)
- ✅ No privilege escalation vectors

### 3. CSRF Protection
- ✅ CSRF tokens on all POST/PUT/DELETE forms
- ✅ HTTP-only cookies for session tokens
- ✅ Same-site cookie policy enforced

### 4. Rate Limiting
- ✅ 5 submissions/minute per IP on `/submit/` endpoint
- ✅ Redis-backed rate limiting cache
- ✅ Prevents DoS attacks from automated submissions

### 5. Data Security
- ✅ SSL redirect (SECURE_SSL_REDIRECT=True in production)
- ✅ XSS filter enabled (SECURE_BROWSER_XSS_FILTER=True)
- ✅ Secure headers (HSTS, CSP, Referrer Policy)
- ✅ Secure cookies (SECURE_COOKIE_HTTPONLY, SESSION_COOKIE_SECURE)

### 6. Audit Trail
- ✅ User attribution on every action
- ✅ Stage transition logging
- ✅ Bulk operation logging
- ✅ Persistent file-based audit log

---

## Testing Scenarios

### Scenario 1: Employee Login Flow
1. User visits `/accounts/login/`
2. Enters employee credentials
3. Django redirects to `/incidents/` (home)
4. `home()` checks `is_staff=False`
5. Redirects to `/incidents/employee/dashboard/`
6. Sees personal metrics and recent tickets only
7. Can submit new ticket (rate-limited)

### Scenario 2: Manager Login Flow
1. User visits `/accounts/login/`
2. Enters manager credentials (admin account)
3. Django redirects to `/incidents/` (home)
4. `home()` checks `is_staff=True`
5. Redirects to `/incidents/manager/dashboard/`
6. Sees full incident overview and NIST breakdown
7. Can access incident queue and admin console

### Scenario 3: Unauthorized Access Attempt
1. Non-manager user visits `/incidents/manager/dashboard/`
2. `_is_it_manager()` check fails
3. Returns 403 Forbidden with unauthorized.html page
4. User prompted to submit ticket instead

### Scenario 4: API Submission
1. Monitoring tool authenticates with `/api/token/`
2. Receives JWT access token (valid 5 minutes)
3. Submits incident to `/api/v1/log-incident/`
4. Incident created with PREPARATION stage
5. Employee can see submitted incident in dashboard
6. Manager can triage in incident queue

---

## Deployment Checklist

- [x] Three-tier user system implemented and tested
- [x] Employee dashboard with personal metrics
- [x] Manager dashboard with NIST workflow and SecOps metrics
- [x] API endpoints for automated incident submission
- [x] Role-based navbar navigation
- [x] Chain-of-custody audit logging
- [x] Rate limiting on public endpoints
- [x] CSRF and session security
- [x] Django checks passing (0 errors)
- [x] Committed to Git with descriptive message
- [x] Pushed to GitHub main branch

---

## File Changes Summary

### New Files
- `incident_core/templates/employee_dashboard.html` (118 lines) - Employee dashboard UI

### Modified Files
- `incident_core/views.py` - Added `home()` and `employee_dashboard()`, enhanced `manager_dashboard()`
- `incident_core/urls.py` - Added routes for home and employee dashboard
- `AegisDesk/settings.py` - Changed `LOGIN_REDIRECT_URL` to `/incidents/`
- `incident_core/templates/base.html` - Updated navbar with role-based navigation
- `incident_core/templates/manager/manager_dashboard.html` - Enhanced with NIST breakdown and metrics

---

## Future Enhancements

### Phase 2: Advanced Features
- [ ] Incident assignment to team members
- [ ] SLA tracking and breach alerts
- [ ] Custom severity/category fields
- [ ] Workflow automation rules
- [ ] Incident trend analytics
- [ ] Export reports (PDF/CSV)

### Phase 3: Enterprise Features
- [ ] Multi-tenancy support
- [ ] Custom RBAC roles
- [ ] Single Sign-On (SSO) integration
- [ ] Splunk/ELK integration
- [ ] Mobile app (React Native)
- [ ] Incident timeline visualization

---

## Support & Documentation

**GitHub Repository**: https://github.com/shan-silvestrece/AegisDesk

**Contributing**: Follow the existing code style and include audit logging for all new features.

**Questions?** Review the existing views.py, models.py, and templates for implementation patterns.
