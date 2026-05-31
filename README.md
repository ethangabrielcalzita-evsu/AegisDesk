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

## Author

**AegisDesk Development Team**

GitHub: https://github.com/shan-silvestrece/AegisDesk
