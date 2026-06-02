# AegisDesk Project Defense - Presentation Script

## 📋 Overview

**Total Duration:** 30-35 minutes  
**Team Members:** 5  
**Format:** Live demonstration + Q&A  
**Order:** Member 1 → 2 → 3 → 4 → 5 → Q&A

---

## 🎬 Opening (30 seconds) - Member 1

**[Member 1 stands, shares screen showing live application]**

**Script:**

> "Good [morning/afternoon], everyone. Thank you for joining us today. I'm [Name], and on behalf of my team, I'm excited to present **AegisDesk** — an enterprise incident management system designed for IT security operations.
> 
> AegisDesk follows the **NIST 800-61 Incident Response Life Cycle**, providing a complete workflow for logging, triaging, and resolving security incidents across an organization's infrastructure.
> 
> Our system serves two user roles: **employees** who report incidents, and **IT managers** who triage and resolve them. It's backed by a secure REST API for automated incident ingestion, and it's deployed on a cloud platform with PostgreSQL for production-grade reliability.
> 
> Over the next 30 minutes, each team member will demonstrate their contribution to this system. Let's begin with the live application and cloud infrastructure."

**[Transition to demo]**

---

## 🌐 Part 1: Cloud & DevOps (6 minutes) - Member 1

### Section 1A: Live Application Tour (2 minutes)

**[Screen: Browser with live application URL]**

**Script:**

> "First, let me show you our deployed application running live on [Render/Railway].
>
> Here's our production URL: **[show URL in browser]**"

**[Action: Navigate to login page]**

> "I'll log in as an employee first to show the employee experience."

**[Action: Enter employee credentials and login]**

> "As an employee, I see my personal dashboard with my submitted tickets, open vs. resolved counts, and quick access to submit new incidents."

**[Action: Click around dashboard, show metrics]**

> "Now let me log out and switch to a manager account."

**[Action: Logout, login as manager]**

> "The manager dashboard is completely different. Here we see **NIST stage breakdowns** — this shows how many tickets are in Preparation, Detection, Containment, and Post-Incident stages. We also see severity distributions and critical/high priority alerts."

**[Action: Hover over metrics, show stage counts]**

> "This role-based separation ensures employees and managers have tailored interfaces for their responsibilities."

---

### Section 1B: Cloud Architecture (2 minutes)

**[Screen: Switch to PaaS dashboard - Render/Railway]**

**Script:**

> "Now let me show you how this is deployed. We're using **[Render/Railway]** as our Platform-as-a-Service."

**[Action: Show dashboard overview]**

> "Our architecture consists of three main components:
> 
> 1. **Web Service** — running our Django application
> 2. **PostgreSQL Database** — managed database instance for production data
> 3. **Static Assets** — served via CDN for optimal performance
> 
> The platform handles auto-scaling, SSL certificates, and health checks automatically."

**[Action: Click on web service]**

> "Here's our web service. You can see the latest deployment was successful [point to deployment log], and it's connected to our GitHub repository for continuous deployment."

**[Action: Show deployment logs - last 5-10 lines]**

> "Every push to our main branch triggers an automatic deployment. This ensures our production environment stays up-to-date without manual intervention."

---

### Section 1C: Secure Environment Variables (2 minutes)

**[Screen: Navigate to Environment Variables section]**

**Script:**

> "Security is critical for our application. Let me show how we handle sensitive configuration.
> 
> All secrets and credentials are stored as **environment variables** — never in our codebase."

**[Action: Show environment variables list (WITHOUT revealing values)]**

> "Here you can see we have several key variables configured:
> 
> - **DJANGO_SECRET_KEY** — for cryptographic signing
> - **DATABASE_URL** — PostgreSQL connection string with credentials
> - **ALLOWED_HOSTS** — restricts which domains can access our app
> - **DEBUG** — set to False for production security
> 
> Notice that the values are hidden. These are encrypted at rest and only accessible to our application runtime."

**[Action: Switch to code editor showing .gitignore]**

> "In our repository, we explicitly exclude `.env` files from version control. This ensures no developer can accidentally commit secrets."

**[Action: Show .gitignore file with .env entries highlighted]**

---

### Section 1D: Database Connection (1 minute)

**[Screen: Switch to database dashboard]**

**Script:**

> "Finally, let's verify our PostgreSQL database connection. This is our managed PostgreSQL instance."

**[Action: Show database overview - connections, size, etc.]**

> "We're using PostgreSQL because it offers:
> - **ACID compliance** for data integrity
> - **Concurrent user support** — unlike SQLite
> - **Production-grade** reliability for enterprise use
> 
> Our database is backed up automatically, and we have connection pooling configured for optimal performance."

**[Action: Show a simple query or table list if possible]**

> "As you can see, we have live data with incident tickets, users, and assets all stored securely."

---

### Transition to Member 2

**Script:**

> "So that's our cloud infrastructure — secure, scalable, and production-ready. Now I'll hand it over to [Member 2's Name], who will demonstrate our **REST API and JWT authentication system** for automated incident reporting."

**[Member 1 stops sharing, Member 2 starts sharing]**

---

## 🔐 Part 2: API & IAM (6 minutes) - Member 2

### Section 2A: Introduction (30 seconds)

**[Screen: Postman open with AegisDesk collection loaded]**

**Script:**

> "Thank you [Member 1's Name]. I'm [Name], and I developed our **REST API and Identity Access Management** layer.
> 
> While the web interface serves human users, our API enables **automated incident ingestion** from monitoring tools, SIEM systems, and security sensors.
> 
> Let me demonstrate how a remote monitoring tool would authenticate and report incidents programmatically."

---

### Section 2B: JWT Token Generation (2 minutes)

**[Screen: Postman - Token Obtain Endpoint]**

**Script:**

> "First, any API client must authenticate. We use **JSON Web Tokens** — an industry standard for stateless authentication.
> 
> Here's our token endpoint: `POST /incidents/api/token/`"

**[Action: Show request body with username/password]**

> "I'll authenticate as a monitoring service account."

**[Action: Click Send]**

> "And here's the response: we get two tokens.
> 
> 1. **Access Token** — used for API requests, expires in 5 minutes
> 2. **Refresh Token** — used to get new access tokens, expires in 24 hours
> 
> This short-lived access token design minimizes the impact of token theft."

**[Action: Copy the access token]**

> "Let me copy this access token and use it to make an authenticated request."

---

### Section 2C: Authenticated API Call (2 minutes)

**[Screen: Postman - Log Incident Endpoint]**

**Script:**

> "Now I'll demonstrate automated incident logging. This is the endpoint: `POST /incidents/api/v1/log-incident/`"

**[Action: Show the Authorization header with Bearer token]**

> "I'm passing the access token in the Authorization header as a **Bearer token**."

**[Action: Show request body]**

> "And here's the incident payload:
> ```json
> {
>   'title': 'Suspicious Login Detected',
>   'description': 'Multiple failed login attempts from IP 203.0.113.45',
>   'severity': 'HIGH',
>   'affected_asset': 3,
>   'nist_stage': 'DETECTION_ANALYSIS'
> }
> ```"

**[Action: Click Send]**

> "Sending the request..."

**[Action: Show 201 Created response]**

> "Success! **201 Created**. The incident has been logged in our database."

**[Action: Switch to browser, navigate to manager dashboard]**

> "Let me verify this in the web UI. Refreshing the manager dashboard..."

**[Action: Show the new ticket appeared in the list]**

> "And there it is — our API-created incident now appears in the queue for IT managers to triage. The integration between API and web UI is seamless."

---

### Section 2D: Unauthorized Access Demonstration (1 minute)

**[Screen: Back to Postman]**

**Script:**

> "Now let me demonstrate our security enforcement. What happens if someone tries to access the API without authentication?"

**[Action: Remove Authorization header or use invalid token]**

> "I'll remove the Bearer token and send the same request."

**[Action: Click Send]**

> "**401 Unauthorized**. The API correctly rejects unauthenticated requests. No data is exposed without proper credentials."

---

### Section 2E: Token Refresh (30 seconds)

**[Screen: Postman - Token Refresh Endpoint]**

**Script:**

> "Finally, when the access token expires after 5 minutes, clients don't need to re-authenticate with username and password.
>
> They use the **refresh token** at this endpoint: `POST /incidents/api/token/refresh/`"

**[Action: Show refresh token in body, click Send]**

> "And we get a brand new access token — valid for another 5 minutes. This allows long-running monitoring services to maintain access without storing passwords."

---

### Transition to Member 3

**Script:**

> "So that's our API layer — secure, stateless JWT authentication with automated incident ingestion.
> 
> Now I'll hand it over to [Member 3's Name], who designed our **database architecture and role-based access control** to prevent unauthorized data access."

**[Member 2 stops sharing, Member 3 starts sharing]**

---

## 🗄️ Part 3: Database & RBAC (6 minutes) - Member 3

### Section 3A: Introduction (30 seconds)

**[Screen: VS Code open showing models.py or database diagram]**

**Script:**

> "Thank you [Member 2's Name]. I'm [Name], and I architected the database layer and implemented **role-based access control**.
> 
> Security isn't just about authentication — it's also about **authorization**. Our system prevents horizontal and vertical privilege escalation through careful query filtering and permission checks.
> 
> Let me demonstrate both the data model and our RBAC enforcement."

---

### Section 3B: Database Model Overview (1 minute)

**[Screen: models.py showing IncidentTicket model]**

**Script:**

> "Here's our core data model. The **IncidentTicket** contains:
> - `title`, `description` — incident details
> - `severity` — Low, Medium, High, Critical
> - `nist_stage` — tracks progression through the NIST lifecycle
> - `affected_asset` — foreign key to the Asset model
> - `reported_by` — foreign key to the User who created it
> 
> This `reported_by` field is critical for access control. It creates ownership, allowing us to filter 'my tickets' vs. 'all tickets'."

---

### Section 3C: "Mine" vs "All" Querysets (2 minutes)

**[Screen: Browser logged in as employee]**

**Script:**

> "Let me demonstrate query filtering in action. I'm logged in as **Employee User 1**.
> 
> When I navigate to 'My Tickets'..."

**[Action: Click My Tickets link]**

> "I see only the tickets I personally reported. Notice the URL: `/incidents/my-tickets/`"

**[Action: Open browser DevTools, show Network tab]**

> "Behind the scenes, our queryset is filtered:
> ```python
> tickets = IncidentTicket.objects.filter(reported_by=request.user)
> ```
> 
> This ensures Employee 1 can never see Employee 2's tickets — even if they share the same database."

**[Action: Note ticket IDs on screen]**

> "Now let me log out and log in as a **Manager**."

**[Action: Logout, login as manager, navigate to ticket queue]**

> "The manager sees **all tickets** from all employees. The queryset here is:
> ```python
> tickets = IncidentTicket.objects.all()
> ```
> 
> Role-based filtering happens at the query level — not in templates or JavaScript — making it tamper-proof."

---

### Section 3D: Anti-IDOR Demonstration (2 minutes)

**[Screen: Still logged in as employee]**

**Script:**

> "Now let me demonstrate **Insecure Direct Object Reference** protection.
> 
> I'm logged in as Employee 1. Let me open one of my tickets."

**[Action: Click a ticket belonging to Employee 1, note the URL]**

> "I can see ticket #5, which I own. The URL is: `/incidents/ticket/5/`
> 
> Now, what if I try to access ticket #8, which belongs to Employee 2?"

**[Action: Manually change URL to a different ticket ID]**

> "I'll change the URL to `/incidents/ticket/8/` and press Enter."

**[Action: Hit Enter, wait for page to load]**

> "**403 Forbidden**. Access denied. Here's the unauthorized page.
> 
> Our view checks ownership before rendering:
> ```python
> if ticket.reported_by != request.user and not _is_it_manager(request.user):
>     return render(request, 'unauthorized.html', status=403)
> ```
>
> This prevents **horizontal privilege escalation** — users can't access each other's data by guessing IDs."

**[Action: Log back in as manager, access the same ticket]**

> "But if a manager accesses ticket #8, they can see it because managers have elevated permissions for triage purposes."

---

### Section 3E: Bulk Operations (1 minute)

**[Screen: Manager ticket queue]**

**Script:**

> "Finally, let me demonstrate **manager-only bulk operations**.
> 
> When incidents are resolved, managers can close multiple tickets at once."

**[Action: Select 2-3 tickets via checkboxes]**

> "I'll select these three tickets and click **Bulk Close**."

**[Action: Click Bulk Close button]**

> "The tickets are now marked as CLOSED and removed from the queue. This bulk action is **only available to managers** — employees don't have this capability."

**[Action: Show success message]**

> "And we get confirmation: '3 ticket(s) were closed successfully.' Each closure is logged in our audit trail for compliance."

---

### Transition to Member 4

**Script:**

> "That's our database and RBAC layer — secure by design with query-level filtering and ownership checks.
> 
> Now [Member 4's Name] will walk through our **user interface and front-end components**."

**[Member 3 stops sharing, Member 4 starts sharing]**

---

## 🎨 Part 4: Frontend UI & UX (6 minutes) - Member 4

### Section 4A: Introduction (30 seconds)

**[Screen: Browser on employee dashboard]**

**Script:**

> "Thank you [Member 3's Name]. I'm [Name], and I designed the front-end interface and user experience components.
> 
> A security tool is only effective if people actually use it. Our UI is built with **Bootstrap 5** for responsive design, **Django Crispy Forms** for consistent styling, and custom template tags for reusable components.
> 
> Let me walk you through the user experience from both employee and manager perspectives."

---

### Section 4B: Base Template & Navigation (1 minute)

**[Screen: VS Code showing base.html]**

**Script:**

> "Our UI is built on a **base template** that all pages extend. This provides:
> - Consistent navigation
> - Role-based menu items
> - Message alerts for user feedback
> - Mobile-responsive layout"

**[Action: Scroll through base.html showing navbar, message blocks]**

> "Notice how the navigation adapts based on user role. Let me show you in the browser."

**[Screen: Switch to browser, show navbar as employee]**

> "As an employee, I see 'Submit Ticket' and 'My Tickets' in the navigation."

**[Action: Logout, login as manager]**

> "As a manager, the nav changes to 'Dashboard', 'Ticket Queue', and 'Manager Guide'. This is controlled by template conditionals checking `user.is_staff`."

---

### Section 4C: Dashboard Metrics (1.5 minutes)

**[Screen: Manager dashboard]**

**Script:**

> "The manager dashboard provides real-time metrics for incident tracking.
> 
> On the left, we have **NIST stage distribution** — showing how many tickets are in each phase of the incident response lifecycle."

**[Action: Hover over or point to stage counts]**

> "On the right, **severity breakdown** — color-coded for quick threat assessment. Red for critical, orange for high, yellow for medium, green for low."

**[Action: Point to severity cards]**

> "And at the top, **key performance indicators** — total open tickets, critical/high priority alerts, and overall ticket count.
> 
> All of this updates in real-time as tickets are created and resolved."

**[Action: Switch to employee dashboard]**

> "The employee dashboard is simpler — focused on personal metrics. Total submitted, currently open, and resolved counts. Plus a quick view of their 5 most recent tickets."

---

### Section 4D: Interactive Forms & Validation (2 minutes)

**[Screen: Navigate to Submit Ticket page]**

**Script:**

> "Now let me show our ticket submission form. This uses **Django Crispy Forms** with Bootstrap 5 styling."

**[Action: Show form fields]**

> "The form includes:
> - **Title** and **Description** — required fields
> - **Category** — IT Support or Security Breach
> - **Severity** — dropdown with four levels
> - **Affected Asset** — which server, workstation, or network device is impacted
> - **NIST Stage** — defaults to 'Preparation'
> 
> All required fields are marked with asterisks."

**[Action: Try to submit empty form]**

> "Watch what happens if I try to submit without filling it out."

**[Action: Click Submit]**

> "We get **inline validation errors** — 'This field is required' appears right next to each missing field. This is client-side validation for immediate feedback."

**[Action: Fill out form with valid data]**

> "Now I'll fill it out properly and submit."

**[Action: Complete and submit form]**

> "Success! We're redirected to a confirmation page with a styled success message. The ticket is now in the system."

---

### Section 4E: Filtering & Pagination (1 minute)

**[Screen: Manager ticket queue with filters]**

**Script:**

> "For managers handling dozens of tickets, we provide **filtering and pagination**.
> 
> Let me filter by severity — only show HIGH severity tickets."

**[Action: Apply severity filter]**

> "The list updates to show only high-severity incidents. Notice the URL includes the filter parameter: `?severity=HIGH`"

**[Action: Scroll to pagination controls]**

> "And if we have more than 20 tickets, pagination appears. Let me go to page 2."

**[Action: Click page 2]**

> "The URL becomes: `?severity=HIGH&page=2` — the filter persists across pages. This is crucial for usability when searching through large incident queues."

---

### Section 4F: Responsive Design (30 seconds)

**[Screen: Browser DevTools, toggle device toolbar]**

**Script:**

> "Finally, our design is fully responsive. Let me show it on a mobile viewport."

**[Action: Toggle to mobile view, navigate through a few pages]**

> "The navigation collapses to a hamburger menu, cards stack vertically, and tables adapt to smaller screens. This allows managers to triage incidents on the go."

---

### Transition to Member 5

**Script:**

> "So that's our frontend — responsive, intuitive, and designed for rapid incident triage.
> 
> Now for the final demonstration, [Member 5's Name] will show our **security defenses and compliance features**."

**[Member 4 stops sharing, Member 5 starts sharing]**

---

## 🛡️ Part 5: DevSecOps & Compliance (6 minutes) - Member 5

### Section 5A: Introduction (30 seconds)

**[Screen: Terminal or VS Code open]**

**Script:**

> "Thank you [Member 4's Name]. I'm [Name], and I implemented our **active defense mechanisms and compliance controls**.
> 
> Security isn't just about preventing unauthorized access — it's also about detecting and logging suspicious activity.
>
> I'll demonstrate our rate limiting, audit logging, and automated security scanning."

---

### Section 5B: Rate Limiting Attack Simulation (2 minutes)

**[Screen: Browser on submit ticket page, DevTools Network tab open]**

**Script:**

> "First, let me demonstrate **rate limiting** — our defense against automated abuse and denial-of-service attacks.
> 
> Our ticket submission endpoint allows **5 submissions per minute per IP address**. Any more than that, and the request is blocked."

**[Action: Submit a ticket normally]**

> "Here's a normal submission — it goes through successfully."

**[Action: Rapidly submit 4 more tickets by refreshing and submitting]**

> "I'm submitting tickets rapidly... 2... 3... 4... 5..."

**[Action: Try to submit a 6th ticket within the same minute]**

> "Now for the 6th attempt..."

**[Action: Submit again]**

> "**Blocked!** I get the error message: 'Too many requests. Please wait before submitting another ticket.'
> 
> In the Network tab, you can see this returned a **429 Too Many Requests** status code."

**[Action: Show Network tab with 429 response]**

> "This prevents:
> - **Automated spam** from bots
> - **Denial-of-service** attacks flooding our system
> - **Brute force** ticket creation
> 
> After one minute, the counter resets and legitimate users can submit again."

---

### Section 5C: Audit Logging & Chain of Custody (2 minutes)

**[Screen: Open aegis_audit.log file]**

**Script:**

> "Every critical action in AegisDesk is logged to our **audit log** for compliance and forensic analysis.
> 
> Here's our `aegis_audit.log` file. Each entry includes:
> - **Timestamp** — when the action occurred
> - **User** — who performed it
> - **Action** — what happened
> - **Details** — affected ticket and changes"

**[Action: Scroll through log showing recent entries]**

> "Let me point out some key entries:
> 
> This one: `[User:employee] New incident registered. Title: 'VPN Outage' for Asset: Firewall-01`
> 
> And this: `[User:it_manager] Ticket #14 modified. Stage altered from 'PREPARATION' to 'DETECTION_ANALYSIS'.`"

**[Action: Create a new ticket in the browser]**

> "Now let me create a ticket in real-time and watch the log update."

**[Action: Submit a test ticket]**

> "Ticket submitted. Let me refresh the audit log..."

**[Action: Tail or refresh log file]**

> "And there it is — a new entry logged immediately with my username, timestamp, and ticket details.
> 
> This audit trail is **immutable** — it's append-only and cannot be modified through the UI. It provides a complete chain of custody for every incident from creation to resolution."

---

### Section 5D: NIST Compliance Demonstration (1 minute)

**[Screen: Browser showing a ticket's stage progression or manager dashboard]**

**Script:**

> "Our system enforces the **NIST 800-61 Incident Response Life Cycle** — the federal standard for handling security incidents.
> 
> Every ticket progresses through these stages:
> 1. **Preparation** — Initial report
> 2. **Detection & Analysis** — Under investigation
> 3. **Containment, Eradication & Recovery** — Threat isolated and removed
> 4. **Post-Incident Activity** — Lessons learned documented
> 5. **Closed** — Fully resolved
> 
> Managers update the stage as the response progresses, and every transition is logged."

**[Action: Show audit log entries for stage changes]**

> "Here in the audit log, you can see a ticket moving through the lifecycle:
> - `PREPARATION` → `DETECTION_ANALYSIS`
> - `DETECTION_ANALYSIS` → `CONTAINMENT_ERADICATION`
> - `CONTAINMENT_ERADICATION` → `POST_INCIDENT`
> 
> This ensures we follow best practices and maintain compliance with federal guidelines."

---

### Section 5E: Security Scanning (1 minute)

**[Screen: Terminal]**

**Script:**

> "Finally, let me show our automated security scanning. We use **Bandit** to scan for security issues in our Python code."

**[Action: Run command `bandit -r incident_core/ AegisDesk/`]**

> "Running Bandit scan now..."

**[Wait for results]**

> "**[If clean results]:** Clean scan! No security issues detected. Our code follows secure coding practices.
> 
> **[If warnings appear]:** We have some low-severity warnings here, but no critical issues. These are false positives related to [explain specific warnings].
> 
> We also run Django's deployment checklist:"

**[Action: Run command `python manage.py check --deploy`]**

> "This checks for production security misconfigurations..."

**[Wait for results]**

> "And we pass all critical checks. Any warnings here are related to local development settings — in production, we enable HTTPS, secure cookies, and all hardening features."

---

### Section 5F: Summary (30 seconds)

**Script:**

> "To summarize our security posture:
> - **Rate limiting** prevents abuse
> - **Audit logging** provides compliance and forensics
> - **NIST framework** ensures best-practice incident response
> - **Automated scanning** catches vulnerabilities before deployment
> - **Secure deployment** with encrypted secrets and HTTPS
> 
> AegisDesk is built with security as a first-class requirement, not an afterthought."

---

## 🎯 Closing (1 minute) - Member 1

**[Screen: Live application or team slide]**

**Script:**

> "Thank you, [Member 5's Name].
> 
> To wrap up, AegisDesk demonstrates the full stack of modern secure application development:
>
> - **Cloud-native deployment** with managed infrastructure
> - **RESTful API** with JWT authentication
> - **PostgreSQL database** with RBAC enforcement
> - **Responsive UI** built with modern frameworks
> - **Active defense** and compliance logging
> 
> Our system is production-ready, scalable, and follows industry security standards.
> 
> We're now happy to take your questions."

---

## ❓ Q&A Session (5-10 minutes) - All Members

### Q&A Strategy

**General approach:**
- Listen carefully to the full question before answering
- The team member whose area is most relevant should take the lead
- Others can add supporting details
- If unsure, say "Let me confer with my team" then discuss briefly

### Common Questions & Suggested Answers

---

**Q: "Why did you choose Django over other frameworks?"**

**Member 1 or 2 answers:**

> "We chose Django for several reasons:
> 1. **Security by default** — built-in CSRF protection, SQL injection prevention, and XSS filtering
> 2. **Battery included** — authentication, admin panel, and ORM out of the box
> 3. **Django REST Framework** — industry-standard API toolkit
> 4. **Mature ecosystem** — extensive documentation and community support
> 5. **Python** — readable, maintainable, and widely used in DevOps
> 
> For an enterprise security tool, we wanted a framework with proven security credentials."

---

**Q: "How do you handle database backups?"**

**Member 1 answers:**

> "Our managed PostgreSQL instance on [Render/Railway] provides **automated daily backups** with point-in-time recovery.
> 
> Backups are retained for 7 days, and we can restore to any point within that window. For additional protection, we could implement:
> - Weekly full backups to S3
> - Continuous WAL archiving
> - Disaster recovery replication to a secondary region
> 
> For an MVP, the managed backup solution meets our needs."

---

**Q: "What happens if someone steals a JWT token?"**

**Member 2 answers:**

> "Great question. JWT theft is a real concern, so we implemented several mitigations:
> 
> 1. **Short-lived access tokens** — 5 minutes only. Even if stolen, the window of abuse is minimal.
> 2. **HTTPS enforcement** — tokens are never transmitted over unencrypted connections in production.
> 3. **Refresh token rotation** — when a refresh token is used, we could issue a new one and invalidate the old (not implemented yet but planned).
> 4. **Token revocation** — we could implement a blacklist for compromised tokens.
> 
> The 5-minute expiration is the key defense — by the time an attacker discovers a token, it's likely already expired."

---

**Q: "How do you prevent SQL injection?"**

**Member 3 answers:**

> "Django's ORM uses **parameterized queries** automatically, which prevents SQL injection by design.
> 
> For example, when we query:
> ```python
> IncidentTicket.objects.filter(severity='HIGH')
> ```
> Django generates:
> ```sql
> SELECT * FROM incident_core_incidentticket WHERE severity = %s
> ```
> And binds the parameter safely.
> 
> We never concatenate user input into SQL strings. If we needed raw SQL, we'd use Django's parameterization:
> ```python
> cursor.execute("SELECT * FROM table WHERE id = %s", [user_input])
> ```
> 
> Additionally, Bandit scans for any SQL injection vulnerabilities in our security audit."

---

**Q: "What if a manager leaves the company? How do you revoke access?"**

**Member 1 or 2 answers:**

> "We follow standard identity management practices:
> 
> 1. **Deactivate the user account** — set `is_active = False` in Django's user model. This immediately invalidates all sessions and API tokens.
> 2. **Remove from staff group** — set `is_staff = False` to revoke manager permissions.
> 3. **Audit log** — all actions by that user remain in the audit log for forensic purposes.
> 
> For enterprise deployments, we'd integrate with:
> - **LDAP/Active Directory** for centralized user management
> - **SSO (SAML/OAuth)** to delegate authentication to the organization's identity provider
> 
> This ensures access is revoked when someone leaves or changes roles."

---

**Q: "How does your system scale under high load?"**

**Member 1 answers:**

> "Our PaaS platform provides **horizontal scaling** — we can increase the number of web server instances based on traffic.
> 
> Current optimizations:
> - **Database connection pooling** — reuse connections instead of opening new ones
> - **Query optimization** — use `select_related()` to reduce N+1 queries
> - **Caching** — we have Redis configured for session storage and rate limiting
> 
> For very high loads (1000+ concurrent users), we'd add:
> - **Read replicas** for the database
> - **CDN** for static assets
> - **Load balancer** to distribute traffic
> - **Background task queue** (Celery) for async processing
> 
> But for typical enterprise use (100-500 users), our current architecture handles it easily."

---

**Q: "What about penetration testing?"**

**Member 5 answers:**

> "We've implemented defensive measures, but you're right — penetration testing would be the next step.
> 
> We'd conduct:
> 1. **Automated vulnerability scanning** — tools like OWASP ZAP or Burp Suite
> 2. **Manual penetration testing** — ethical hackers testing for logic flaws
> 3. **Code review** — security experts auditing the codebase
> 
> Common attack vectors we'd test:
> - SQL injection (already protected by ORM)
> - XSS (protected by Django's auto-escaping)
> - CSRF (Django's built-in tokens)
> - Session hijacking (secure cookies + HTTPS)
> - Privilege escalation (our RBAC demo showed this is blocked)
> 
> We'd also pursue **security certifications** like SOC 2 for enterprise customers."

---

**Q: "Why PostgreSQL instead of NoSQL like MongoDB?"**

**Member 3 answers:**

> "Great question. We chose PostgreSQL because:
> 
> 1. **Relational data** — incidents have clear relationships to users and assets. SQL fits this naturally.
> 2. **ACID guarantees** — we need transactional integrity for audit logs and ticket updates.
> 3. **Mature tooling** — backups, replication, monitoring are all well-established.
> 4. **Query power** — complex filters and joins for manager dashboards.
> 
> NoSQL would make sense if we had:
> - Massive scale (millions of tickets per day)
> - Unstructured data (variable incident formats)
> - High-velocity writes (thousands per second)
> 
> For enterprise incident management, PostgreSQL is the right choice. Even GitHub, Uber, and Stripe use Postgres at massive scale."

---

**Q: "How do you handle password resets?"**

**Member 2 answers:**

> "Django provides a built-in password reset flow that we leverage:
> 
> 1. User clicks 'Forgot Password'
> 2. Enters their email
> 3. System sends a **time-limited, single-use token** via email
> 4. User clicks the link and sets a new password
> 
> Security features:
> - Token expires after 24 hours
> - Token is single-use (invalidated after password change)
> - Old password is irreversibly hashed with **PBKDF2** (Django default)
> - Email includes the user's IP and timestamp for anomaly detection
> 
> For production, we'd integrate with:
> - **Multi-factor authentication** (TOTP or SMS)
> - **Password complexity requirements** (already enforced)
> - **Breach detection** using HaveIBeenPwned API
>"

---

**Q: "What's the cost of running this in production?"**

**Member 1 answers:**

> "For a small to medium enterprise (up to 500 users), the monthly costs would be:
> 
> - **PaaS hosting** (Render/Railway): $15-25/month for web service
> - **PostgreSQL database**: $15-20/month for managed instance with backups
> - **Domain + SSL**: $12/year (SSL is free via Let's Encrypt)
> - **Email service** (for notifications): $10-15/month
> 
> **Total: ~$50-70/month**
> 
> This scales with usage:
> - More users → upgrade database tier
> - High traffic → add more web instances
> - Additional features → potentially add Redis or Celery
> 
> But compared to commercial incident management tools (which cost $5,000-50,000/year), our solution is extremely cost-effective for internal use."

---

**Q: "What if the audit log file fills up the disk?"**

**Member 5 answers:**

> "Excellent operational question. We'd implement **log rotation** using tools like `logrotate` on Linux:
> 
> ```
> /path/to/aegis_audit.log {
>     daily
>     rotate 90
>     compress
>     dateext
>     notifempty
> }
> ```
> 
> This:
> - Rotates logs daily
> - Keeps 90 days of history (compressed)
> - Older logs are archived to S3 or deleted
> 
> For compliance, we'd also:
> - **Forward logs to a SIEM** (Security Information and Event Management) like Splunk or ELK
> - **Immutable storage** (S3 Glacier) for long-term retention
> - **Disk monitoring** with alerts when usage exceeds 80%
> 
> For the MVP, file-based logging is fine, but production systems need centralized log management."

---

**Q: "Can you demo the API documentation?"**

**Member 2 answers:**

> "Absolutely. Django REST Framework provides **auto-generated API documentation**."

**[Action: Navigate to `/api/docs/` or show OpenAPI schema]**

> "Here's our API schema. It documents:
> - All endpoints
> - Required headers
> - Request/response formats
> - Authentication requirements
> 
> We can also generate a **Postman collection** or **OpenAPI 3.0 spec** for easy integration."

**[Action: Show the Postman collection or swagger UI if available]**

> "This makes it easy for monitoring tool vendors to integrate with AegisDesk without reading code."

---

**Q: "What about mobile app support?"**

**Member 4 answers:**

> "Our web interface is fully **responsive** and works on mobile browsers, as I demonstrated earlier.
> 
> For a native mobile app, we'd leverage our existing API:
> - **React Native** or **Flutter** for cross-platform development
> - Same JWT authentication
> - Push notifications for critical incidents
> - Offline support with local caching
