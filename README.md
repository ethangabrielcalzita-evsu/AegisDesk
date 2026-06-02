# AegisDesk

A Django-based incident management system for tracking and managing security incidents using the NIST 4-stage incident response framework. AegisDesk helps security teams efficiently report, track, and resolve security incidents across your organization's assets.

## Features

- **Incident Ticket Management**: Create and track security incidents with detailed descriptions
- **NIST Framework Integration**: Track incidents through NIST incident response stages:
  - 1. Preparation
  - 2. Detection & Analysis
  - 3. Containment, Eradication & Recovery
  - 4. Post-Incident Activity
  - 5. Resolved / Closed
- **Severity Classification**: Categorize incidents by severity (Low, Medium, High, Critical)
- **Asset Management**: Track incidents against specific organizational assets (Servers, Workstations, Network devices, Cloud repositories)
- **Rate Limiting**: Protection against abuse with rate-limited ticket submissions (5 tickets per minute per IP)
- **User Authentication**: Secure login for authenticated incident reporting
- **REST API**: RESTful API endpoints for programmatic access with JWT authentication
- **Audit Logging**: Comprehensive logging of incident creation and modifications

## Project Structure

```
AegisDesk/
├── AegisDesk/              # Main Django project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py            # URL routing configuration
│   ├── wsgi.py            # WSGI application
│   └── asgi.py            # ASGI application
├── incident_core/          # Main application
│   ├── models.py          # Database models (Asset, IncidentTicket)
│   ├── views.py           # View functions
│   ├── api_views.py       # REST API views
│   ├── serializers.py     # DRF serializers
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL patterns
│   ├── admin.py           # Django admin configuration
│   ├── templates/         # HTML templates
│   │   └── incident_core/
│   │       ├── base.html           # Base template
│   │       ├── submit_ticket.html  # Incident submission form
│   │       └── success.html        # Success message
│   └── management/        # Custom management commands
│       └── commands/
│           └── populate_incidents.py  # Sample data loader
├── requirements.txt        # Python dependencies
├── manage.py             # Django CLI tool
├── db.sqlite3            # SQLite database (development)
└── README.md             # This file

```

## Architecture Overview

AegisDesk is built as a Django web application with separate UI and API layers:

- **Web UI**: Django views and templates provide employee and manager dashboards, incident submission, and ticket detail workflows.
- **Employee dashboard**: End users submit incidents and track only their own tickets.
- **Manager dashboard**: IT/SecOps staff triage incidents, update NIST response stages, and manage the incident queue.
- **API layer**: Django REST Framework exposes JWT-protected endpoints for remote monitoring tools and programmatic incident ingestion.
- **Data model**: `IncidentTicket` captures incident details, severity, NIST stage, category, reporter, and affected asset relationships.
- **Authentication**: Django session authentication for web users and Simple JWT for API clients.
- **Security**: CSRF protection, secure cookies, rate limiting, audit logging, and role-based access control using `is_staff`.

## Setup Process

Follow these steps to install and run AegisDesk locally:

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies from `requirements.txt`.
4. Apply database migrations with `python manage.py migrate`.
5. Create a Django superuser with `python manage.py createsuperuser`.
6. Optionally populate sample data with `python manage.py populate_incidents`.
7. Start the development server with `python manage.py runserver`.

## Requirements

- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

### Windows Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shan-silvestrece/AegisDesk.git
   cd AegisDesk
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Command Prompt
   venv\Scripts\activate

   # PowerShell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter your username, email, and password.

7. **Load sample data (optional):**
   ```bash
   python manage.py populate_incidents
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

### macOS Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shan-silvestrece/AegisDesk.git
   cd AegisDesk
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter your username, email, and password.

7. **Load sample data (optional):**
   ```bash
   python manage.py populate_incidents
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

### Linux Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shan-silvestrece/AegisDesk.git
   cd AegisDesk
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to enter your username, email, and password.

7. **Load sample data (optional):**
   ```bash
   python manage.py populate_incidents
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

## How to Use the Application

### Accessing the Application

1. **Admin Dashboard:**
   - Navigate to `http://localhost:8000/admin`
   - Log in with your superuser credentials
   - Here you can manage assets, incidents, and users

2. **User Dashboard:**
   - Navigate to `http://localhost:8000/` (or your configured URL)
   - Log in with your credentials
   - Access incident submission forms and view your reported incidents

### Submitting an Incident Ticket

1. Log in to the application
2. Navigate to the incident submission page
3. Fill in the incident details:
   - **Title**: Brief description of the incident
   - **Description**: Detailed information about the incident
   - **Affected Asset**: Select which asset is affected by the incident
   - **Severity Level**: Choose from Low, Medium, High, or Critical
   - **NIST Stage**: Select the current incident response stage
4. Click "Submit Ticket"
5. You will see a success confirmation

### Managing Assets

1. Go to the Django admin panel at `http://localhost:8000/admin`
2. Click on "Assets" under "Incident Core"
3. Click "Add Asset" to create a new asset
4. Fill in:
   - **Name**: Asset identifier (e.g., "Server-01", "Router-Main")
   - **Asset Type**: Choose from:
     - Enterprise Server
     - Employee Workstation
     - Network Router/Switch
     - Cloud Repository
   - **IP Address**: The IPv4 or IPv6 address of the asset
5. Click "Save"

### Viewing and Updating Incidents

1. Go to `http://localhost:8000/admin`
2. Click on "Incident Tickets" under "Incident Core"
3. View all reported incidents with:
   - Severity level
   - NIST response stage
   - Reporting user
   - Affected asset
   - Creation and last modification timestamps
4. Click on an incident to update its NIST stage or other details as it progresses through the incident response process

### Using the REST API

The application provides REST API endpoints for programmatic access:

**Authentication:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

**Create an Incident Ticket (Authenticated):**
```bash
curl -X POST http://localhost:8000/api/incidents/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Security Breach Detected",
    "description": "Suspicious activity on server",
    "affected_asset": 1,
    "severity": "HIGH",
    "nist_stage": "DETECTION_ANALYSIS"
  }'
```

**Retrieve Incidents:**
```bash
curl http://localhost:8000/api/incidents/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Dependencies

- **Django 5.0.6**: Web framework
- **Django REST Framework 3.15.1**: REST API toolkit
- **djangorestframework-simplejwt 5.3.1**: JWT authentication
- **django-ratelimit 4.1.0**: Rate limiting for API endpoints
- **crispy-forms & crispy-bootstrap5**: Enhanced form rendering

## Rate Limiting

The application includes rate limiting to prevent abuse:
- **Limit**: 5 tickets per minute per IP address
- **Applied to**: `submit_ticket` endpoint
- **Behavior**: Returns a 403 Forbidden response when limit is exceeded

## Security Notes

- **Development Only**: The current `SECRET_KEY` is insecure. For production deployment:
  - Generate a new `SECRET_KEY`
  - Set `DEBUG = False`
  - Configure `ALLOWED_HOSTS` with your domain
  - Use environment variables for sensitive settings
  - Use a production database (PostgreSQL recommended)

## Environment Variables

For production deployment, these are the recommended environment variables to configure. The current repository uses static settings for development, but you should switch to env-driven settings before going live.

- `DJANGO_SECRET_KEY` – secret key for cryptographic signing
- `DJANGO_DEBUG` – `False` in production
- `DJANGO_ALLOWED_HOSTS` – comma-separated hostnames
- `DATABASE_URL` – production database URL (for example, PostgreSQL)
- `REDIS_URL` – cache and rate limit backend URL if using Redis
- `EMAIL_HOST` – SMTP server hostname
- `EMAIL_PORT` – SMTP server port
- `EMAIL_HOST_USER` – SMTP user
- `EMAIL_HOST_PASSWORD` – SMTP password
- `SECURE_SSL_REDIRECT` – `True` to enforce HTTPS in production
- `SENTRY_DSN` – optional error monitoring DSN if using Sentry

### Recommended production configuration
1. Do not keep `DEBUG = True` in production.
2. Replace the hardcoded `SECRET_KEY` in `AegisDesk/settings.py` with a call to `os.environ.get('DJANGO_SECRET_KEY')`.
3. Set `ALLOWED_HOSTS` to the actual domain names or IP addresses.
4. Use a production database such as PostgreSQL instead of SQLite.
5. Use Redis for caching and rate limiting if you need high throughput.

## Troubleshooting

### Issue: "Port 8000 is already in use"
**Solution**: Run the server on a different port:
```bash
python manage.py runserver 8001
```

### Issue: "No module named django"
**Solution**: Ensure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: "Database tables don't exist"
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Issue: Can't log in to admin panel
**Solution**: Make sure you created a superuser:
```bash
python manage.py createsuperuser
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue in the GitHub repository.

## Team Roles & Responsibilities

AegisDesk is developed and presented by a specialized team of five engineers, each responsible for specific technical domains and demonstration components during the project defense.

### Member 1: Lead Cloud & DevOps Engineer

**Development Responsibilities:**
- Manages the PaaS deployment (e.g., Render or Railway)
- Configures environment variables securely
- Provisions the PostgreSQL database
- Integrates Cloudinary for media storage

**Presentation Responsibilities:**
- Opens the defense
- Demonstrates the live application
- Explains the cloud architecture
- Proves the secure handling of environment variables

### Member 2: API & IAM (Identity Access) Engineer

**Development Responsibilities:**
- Builds the DRF REST API
- Implements JWT authentication
- Automates role seeding
- Designs the Serializer field-level masking logic

**Presentation Responsibilities:**
- Conducts a live Postman demonstration showing JWT token generation
- Demonstrates role-based API responses
- Showcases the masked vs. unmasked data twist

### Member 3: Database Architect & RBAC Lead

**Development Responsibilities:**
- Designs primary models
- Enforces Anti-IDOR logic
- Builds "Mine/All" view querysets
- Implements manager-only bulk update functionalities

**Presentation Responsibilities:**
- Demonstrates horizontal privilege escalation prevention (attempting unauthorized ID access)
- Showcases bulk operations executing securely

### Member 4: Frontend UI & Component Engineer

**Development Responsibilities:**
- Designs base templates
- Implements interactive dashboard filtering (dates, statuses)
- Builds inline formsets
- Creates custom template tags

**Presentation Responsibilities:**
- Walks through the UI/UX
- Demonstrates pagination persisting with active filters
- Highlights formset data entry and custom tag logic

### Member 5: DevSecOps & Compliance Analyst

**Development Responsibilities:**
- Implements active defense (django-axes, ratelimiting, honeypots)
- NIST-aligned Python audit logging
- Runs Bandit/pip-audit scans

**Presentation Responsibilities:**
- Executes live simulated attacks (e.g., triggering a lockout or ratelimit)
- Displays the audit logs
- Presents the clean results of the check --deploy command

---

## Demonstration Guide

This section provides step-by-step instructions for each team member to demonstrate their contributions during the project defense.

### Member 1: Cloud & DevOps Demonstration

**Duration**: 5-7 minutes

**Pre-Demo Checklist:**
- [ ] Live application deployed and accessible
- [ ] Environment variables configured in PaaS dashboard
- [ ] PostgreSQL database provisioned and connected
- [ ] Cloudinary account configured (if applicable)

**Demonstration Steps:**

1. **Opening Statement** (30 seconds)
   - Introduce the project: "AegisDesk is an enterprise incident management system following NIST guidelines"
   - Brief overview of tech stack: Django, PostgreSQL, REST API, JWT authentication

2. **Live Application Tour** (2 minutes)
   - Open the live deployed URL
   - Show the login page and mention authentication requirements
   - Log in as an employee user
   - Navigate through the employee dashboard
   - Log out and log in as a manager
   - Show the manager dashboard with metrics

3. **Cloud Architecture Explanation** (2 minutes)
   - Open the PaaS dashboard (Render/Railway)
   - Explain the deployment architecture:
     - Web service configuration
     - PostgreSQL database instance
     - Environment variable management
   - Show the deployment logs (last successful deployment)
   - Explain auto-deploy from GitHub integration

4. **Secure Environment Variables** (1-2 minutes)
   - Navigate to environment variables section in PaaS dashboard
   - Show (but don't reveal values) of:
     - `DJANGO_SECRET_KEY`
     - `DATABASE_URL`
     - `ALLOWED_HOSTS`
     - Any API keys (Cloudinary, etc.)
   - Explain: "These are never committed to version control"
   - Show `.gitignore` file excluding `.env` files

5. **Database Connection Proof** (1 minute)
   - Open database dashboard
   - Show connection details (hide credentials)
   - Run a simple query showing data exists:
     ```sql
     SELECT COUNT(*) FROM incident_core_incidentticket;
     ```
   - Show the database is actively being used by the application

**Key Talking Points:**
- "Our application is production-ready and follows 12-factor app principles"
- "All sensitive configuration is externalized via environment variables"
- "Database is isolated and accessed via encrypted connections"
- "Auto-deployment ensures rapid iteration and continuous delivery"

---

### Member 2: API & IAM Demonstration

**Duration**: 5-7 minutes

**Pre-Demo Checklist:**
- [ ] Postman installed with AegisDesk collection imported
- [ ] Test user credentials ready (employee and manager)
- [ ] API endpoints documented and tested

**Demonstration Steps:**

1. **JWT Token Generation** (2 minutes)
   - Open Postman
   - Show the token endpoint: `POST /incidents/api/token/`
   - Request body:
     ```json
     {
       "username": "employee_user",
       "password": "test_password"
     }
     ```
   - Execute the request
   - Show the response with `access` and `refresh` tokens
   - Copy the access token
   - Explain: "Access tokens expire in 5 minutes, refresh tokens in 24 hours"

2. **Authenticated API Call** (2 minutes)
   - Show the log incident endpoint: `POST /incidents/api/v1/log-incident/`
   - Add Authorization header: `Bearer [access_token]`
   - Request body:
     ```json
     {
       "title": "API Test Incident",
       "description": "Testing automated incident logging",
       "severity": "HIGH",
       "affected_asset": 1,
       "nist_stage": "DETECTION_ANALYSIS"
     }
     ```
   - Execute the request
   - Show 201 Created response
   - Navigate to the web UI and show the ticket was created

3. **Unauthorized Access Attempt** (1 minute)
   - Remove the Authorization header
   - Execute the same request
   - Show 401 Unauthorized response
   - Explain: "All API endpoints require valid JWT authentication"

4. **Role-Based API Response** (2 minutes)
   - Get a new token for a manager user
   - Call a "list incidents" endpoint (if available)
   - Show manager can see all incidents
   - Get token for employee user
   - Call same endpoint
   - Show employee sees only their tickets
   - Explain: "Serializers enforce field-level permissions based on user role"

5. **Token Refresh** (1 minute)
   - Show `POST /incidents/api/token/refresh/`
   - Use the refresh token from step 1
   - Get a new access token without re-entering credentials

**Key Talking Points:**
- "JWT tokens are stateless and cryptographically signed"
- "Short-lived access tokens minimize exposure from token theft"
- "API enforces the same RBAC rules as the web interface"
- "Remote monitoring tools can automatically ingest incidents without human intervention"

---

### Member 3: Database & RBAC Demonstration

**Duration**: 5-7 minutes

**Pre-Demo Checklist:**
- [ ] Multiple test users created (employee1, employee2, manager)
- [ ] Test incident tickets created by different users
- [ ] Browser developer tools ready for URL manipulation
- [ ] Database query tool ready (Django admin or shell)

**Demonstration Steps:**

1. **Model Structure Overview** (1 minute)
   - Open `incident_core/models.py` in the code editor
   - Highlight the `IncidentTicket` model
   - Point out key fields: `reported_by`, `nist_stage`, `severity`, `affected_asset`
   - Show the `Asset` model with asset types

2. **"Mine" vs "All" Querysets** (2 minutes)
   - Log in as `employee1`
   - Navigate to "My Tickets"
   - Show only tickets created by `employee1`
   - Open browser developer tools → Network tab
   - Note the URL: `/incidents/my-tickets/`
   - Log out and log in as manager
   - Navigate to "Manager Tickets"
   - Show ALL tickets from all users
   - Explain the queryset filtering logic:
     ```python
     # Employee: tickets.filter(reported_by=request.user)
     # Manager: tickets.all()
     ```

3. **Anti-IDOR Demonstration** (3 minutes)
   - Still logged in as `employee1`
   - Open a ticket detail page (their own ticket): `/incidents/ticket/5/`
   - Note the ticket ID in the URL
   - Manually change the URL to a ticket ID belonging to `employee2`: `/incidents/ticket/8/`
   - Press Enter
   - **Expected Result**: 403 Forbidden page or "Unauthorized" message
   - Explain: "The view checks `ticket.reported_by != request.user` and blocks access"
   - Show the code snippet from `views.py`:
     ```python
     if ticket.reported_by != request.user and not _is_it_manager(request.user):
         return render(request, 'unauthorized.html', status=403)
     ```

4. **Manager-Only Bulk Update** (2 minutes)
   - Log in as manager
   - Navigate to "Manager Tickets" page
   - Select multiple open tickets using checkboxes
   - Click "Bulk Close" button
   - Show success message: "X ticket(s) were closed successfully"
   - Refresh the page
   - Show the tickets are now removed from the open list (moved to CLOSED stage)
   - Explain: "Only managers have access to this endpoint, enforced by `@login_required` and `_is_it_manager()` check"

**Key Talking Points:**
- "Horizontal privilege escalation is blocked at the view layer"
- "Every query is filtered by ownership or role"
- "IDOR attacks are mitigated by comparing `request.user` to resource ownership"
- "Bulk operations are restricted to staff accounts only"

---

### Member 4: Frontend UI Demonstration

**Duration**: 5-7 minutes

**Pre-Demo Checklist:**
- [ ] Multiple test tickets with varying dates and statuses created
- [ ] Browser window at comfortable zoom level
- [ ] Code editor open to template files

**Demonstration Steps:**

1. **Base Template Overview** (1 minute)
   - Open `templates/base.html` in code editor
   - Highlight key elements:
     - Navigation bar with role-based menu items
     - Bootstrap 5 integration
     - Messages framework for alerts
     - Block structure for inheritance
   - Show how child templates extend base

2. **Dashboard UI Walkthrough** (2 minutes)
   - Navigate to employee dashboard
   - Point out UI elements:
     - Personal metrics cards (total submitted, open, resolved)
     - Recent tickets table
     - Color-coded severity badges
     - NIST stage indicators
   - Navigate to manager dashboard
   - Show enhanced metrics:
     - NIST stage breakdown chart
     - Severity distribution
     - Critical/high priority count

3. **Interactive Filtering** (2 minutes)
   - Navigate to "Manager Tickets" page with many tickets
   - Show filter controls (date range, severity, status)
   - Apply a filter (e.g., severity = HIGH)
   - Show results update
   - Add another filter (e.g., date range)
   - Show combined filtering
   - Explain: "Filters are applied via query parameters and preserved across pagination"

4. **Pagination with Active Filters** (1 minute)
   - With filters still active, navigate to page 2
   - Show URL contains both pagination and filter parameters:
     ```
     ?severity=HIGH&page=2
     ```
   - Show filters remain active on page 2
   - Navigate back to page 1
   - Explain: "Django's pagination preserves query strings"

5. **Inline Formsets / Form Interactions** (2 minutes)
   - Navigate to "Submit Ticket" form
   - Show form fields with proper styling (crispy-forms)
   - Point out:
     - Required field indicators
     - Dropdown menus (severity, NIST stage, asset)
     - Text area for description
     - Form validation (try submitting empty)
   - Show validation errors displayed inline
   - Fill form correctly and submit
   - Show success page with styled confirmation

6. **Custom Template Tags** (1 minute, if implemented)
   - Open a template file showing custom tag usage
   - Example: `{% get_severity_badge ticket.severity %}`
   - Show the output in the browser (color-coded badge)
   - Briefly show the tag definition in `templatetags/` folder

**Key Talking Points:**
- "Bootstrap 5 provides responsive, mobile-friendly layouts"
- "Crispy-forms reduces template boilerplate and ensures consistent styling"
- "Filter state persists across pagination for better UX"
- "Custom template tags encapsulate reusable UI logic"

---

### Member 5: DevSecOps & Compliance Demonstration

**Duration**: 5-7 minutes

**Pre-Demo Checklist:**
- [ ] Test account credentials ready
- [ ] Audit log file accessible
- [ ] Bandit installed: `pip install bandit`
- [ ] `python manage.py check --deploy` ready to run
- [ ] Rate limiting configured and tested

**Demonstration Steps:**

1. **Rate Limiting Attack Simulation** (2 minutes)
   - Open the submit ticket form
   - Open browser developer tools → Network tab
   - Submit a ticket normally (success)
   - Rapidly submit 5 more tickets (use browser refresh or script)
   - **Expected Result**: After 5 submissions in 1 minute, show error message:
     ```
     "Too many requests. Please wait before submitting another ticket."
     ```
   - Show 403 Forbidden response in Network tab
   - Explain: "Rate limiting prevents automated abuse and DOS attacks"
   - Show the code decorator:
     ```python
     @ratelimit(key='ip', rate='5/m', block=False)
     ```

2. **Audit Log Chain of Custody** (2 minutes)
   - Open `aegis_audit.log` file
   - Show recent entries with format:
     ```
     INFO 2026-06-02 10:15:33 models [User:jsmith] New incident registered. Title: 'VPN Outage' for Asset: Firewall-01
     INFO 2026-06-02 11:42:07 models [User:it_manager] Ticket #14 modified. Stage altered from 'PREPARATION' to 'DETECTION_ANALYSIS'.
     ```
   - Create a new ticket via web UI
   - Refresh the audit log
   - Show the new entry with correct timestamp and user attribution
   - Update a ticket's NIST stage as manager
   - Show the stage change logged with before/after values
   - Explain: "Every incident creation and modification is logged immutably"

3. **NIST Compliance Demonstration** (1 minute)
   - Show the NIST stage progression in a ticket:
     - PREPARATION → DETECTION_ANALYSIS → CONTAINMENT_ERADICATION → POST_INCIDENT → CLOSED
   - Explain: "This follows the NIST 800-61 Incident Response framework"
   - Show audit log entries tracking stage transitions

4. **Security Scanning with Bandit** (2 minutes)
   - Open terminal
   - Run Bandit scan:
     ```bash
     bandit -r incident_core/ AegisDesk/
     ```
   - Show the output (should be clean or minimal issues)
   - Explain: "Bandit scans for common security issues in Python code"
   - If issues found, explain they are false positives or low severity

5. **Django Deployment Check** (2 minutes)
   - Run Django's deployment checklist:
     ```bash
     python manage.py check --deploy
     ```
   - Show the output
   - **Expected**: Clean output or only warnings (not errors)
   - If warnings appear, explain each one:
     - SECURE_SSL_REDIRECT (okay in dev, required in prod)
     - SECURE_HSTS_SECONDS (production setting)
   - Show `settings.py` security configurations:
     ```python
     SECURE_BROWSER_XSS_FILTER = True
     X_FRAME_OPTIONS = 'DENY'
     CSRF_COOKIE_HTTPONLY = True
     SESSION_COOKIE_SECURE = True  # in production
     ```

6. **Additional Security Features** (1 minute, if time permits)
   - Show CSRF token in form HTML (view source)
   - Explain Django's built-in protections:
     - SQL injection prevention (ORM parameterized queries)
     - XSS protection (auto-escaping templates)
     - Clickjacking protection (X-Frame-Options)

**Key Talking Points:**
- "Defense-in-depth: multiple layers of security controls"
- "Audit logging provides forensic evidence and compliance records"
- "Rate limiting prevents abuse without affecting legitimate users"
- "Automated scanning catches security issues before deployment"
- "Following NIST framework ensures industry-standard incident response"

---

## Defense Coordination Tips

1. **Timing**: Each member should aim for 5-7 minutes. Total presentation: 25-35 minutes + Q&A
2. **Handoffs**: End each section with a transition statement:
   - "Now I'll hand it over to [Member 2] to demonstrate our API layer"
3. **Backup Plans**: Have screenshots ready if live demos fail
4. **Practice**: Run through the entire demo sequence at least twice
5. **Questions**: Designate who answers questions in specific domains
6. **Shared Screen**: Decide in advance who controls screen sharing for each section

---

## Author

**AegisDesk Development Team**

GitHub: https://github.com/shan-silvestrece/AegisDesk
