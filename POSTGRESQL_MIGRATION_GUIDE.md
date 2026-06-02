# PostgreSQL Migration Guide

This guide will walk you through migrating AegisDesk from SQLite to PostgreSQL.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Migration](#step-by-step-migration)
3. [Common Errors & Solutions](#common-errors--solutions)
4. [Production Deployment](#production-deployment)
5. [Verification Steps](#verification-steps)
6. [Rollback Instructions](#rollback-instructions)

---

## Prerequisites

### Software Requirements

- **PostgreSQL 12+** installed on your system
- **Python 3.9+** with virtual environment
- **psycopg2** (PostgreSQL adapter for Python)

### Installing PostgreSQL

#### Windows:
1. Download PostgreSQL from: https://www.postgresql.org/download/windows/
2. Run the installer
3. During installation:
   - Set a password for the `postgres` user (remember this!)
   - Keep the default port: `5432`
   - Install pgAdmin (optional, but helpful)
4. Add PostgreSQL to PATH: `C:\Program Files\PostgreSQL\15\bin`

#### macOS:
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Create a default database
createdb aegisdesk
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

---

## Step-by-Step Migration

### Step 1: Backup Your Current SQLite Database

**IMPORTANT**: Always backup before migration!

```bash
# Copy your SQLite database
copy db.sqlite3 db.sqlite3.backup

# Or export data to JSON (recommended for complex migrations)
python manage.py dumpdata --natural-foreign --natural-primary --indent 4 > backup_data.json
```

### Step 2: Install PostgreSQL Python Dependencies

```bash
# Activate your virtual environment first
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install new requirements
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary==2.9.9` - PostgreSQL adapter
- `dj-database-url==2.1.0` - Database URL parser

### Step 3: Create PostgreSQL Database

#### Option A: Using psql (Command Line)

**Windows:**
```bash
# Open Command Prompt as Administrator
psql -U postgres

# In the PostgreSQL prompt:
CREATE DATABASE aegisdesk;
CREATE USER aegisdesk_user WITH PASSWORD 'your_secure_password';
ALTER ROLE aegisdesk_user SET client_encoding TO 'utf8';
ALTER ROLE aegisdesk_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE aegisdesk_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE aegisdesk TO aegisdesk_user;

# Grant schema permissions (PostgreSQL 15+)
\c aegisdesk
GRANT ALL ON SCHEMA public TO aegisdesk_user;

# Exit
\q
```

**macOS/Linux:**
```bash
# Switch to postgres user
sudo -u postgres psql

# Then run the same SQL commands as above
```

#### Option B: Using pgAdmin (GUI)

1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Database name: `aegisdesk`
4. Owner: `postgres` (or create a new user)
5. Click "Save"

### Step 4: Configure Environment Variables

Create a `.env` file in your project root:

```bash
# Copy the example file
copy .env.example .env
```

Edit `.env` and set your PostgreSQL connection:

```env
DATABASE_URL=postgresql://aegisdesk_user:your_secure_password@localhost:5432/aegisdesk
```

**Format breakdown:**
```
postgresql://[username]:[password]@[host]:[port]/[database_name]
```

**Examples:**
- Local: `postgresql://postgres:mypassword@localhost:5432/aegisdesk`
- Render: `postgresql://user:pass@dpg-abc123.oregon-postgres.render.com/aegisdesk_db`
- Railway: `postgresql://postgres:pass@containers-us-west-123.railway.app:5432/railway`

### Step 5: Load Environment Variables

Since we're not using `python-dotenv` yet, you need to set the environment variable manually:

**Windows (Command Prompt):**
```cmd
set DATABASE_URL=postgresql://aegisdesk_user:your_secure_password@localhost:5432/aegisdesk
```

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://aegisdesk_user:your_secure_password@localhost:5432/aegisdesk"
```

**macOS/Linux:**
```bash
export DATABASE_URL="postgresql://aegisdesk_user:your_secure_password@localhost:5432/aegisdesk"
```

**Alternative**: Install `python-dotenv` to auto-load `.env` files:

```bash
pip install python-dotenv
```

Then update `settings.py`:

```python
# At the very top of settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Load .env file
```

### Step 6: Verify Database Connection

Test that Django can connect to PostgreSQL:

```bash
python manage.py check --database default
```

Expected output:
```
System check identified no issues (0 silenced).
```

If you see connection errors, check your DATABASE_URL and PostgreSQL service status.

### Step 7: Run Migrations

Apply all migrations to the new PostgreSQL database:

```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, incident_core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  [... more migrations ...]
  Applying incident_core.0002_incidentticket_category... OK
```

### Step 8: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 9: Migrate Data (Optional)

If you backed up data from SQLite, restore it:

```bash
python manage.py loaddata backup_data.json
```

**Note**: You may encounter errors if your backup includes conflicting user IDs. In that case, create users manually and skip the auth data:

```bash
# Export specific apps only
python manage.py dumpdata incident_core --indent 4 > incidents_only.json

# Load specific data
python manage.py loaddata incidents_only.json
```

### Step 10: Populate Sample Data (Fresh Start)

If you're starting fresh without migrating old data:

```bash
python manage.py populate_incidents
```

### Step 11: Test the Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` and verify:
- [ ] You can log in
- [ ] Tickets display correctly
- [ ] You can create new tickets
- [ ] Manager dashboard shows data
- [ ] API endpoints work

---

## Common Errors & Solutions

### Error 1: `django.db.utils.OperationalError: could not connect to server`

**Cause**: PostgreSQL service is not running or wrong connection details.

**Solution**:
```bash
# Windows: Check if service is running
services.msc
# Look for "postgresql-x64-15" and ensure it's "Running"

# macOS:
brew services list
brew services start postgresql@15

# Linux:
sudo systemctl status postgresql
sudo systemctl start postgresql

# Verify connection manually:
psql -U postgres -h localhost -p 5432
```

### Error 2: `psycopg2.OperationalError: FATAL: password authentication failed`

**Cause**: Incorrect username or password in DATABASE_URL.

**Solution**:
- Double-check your DATABASE_URL string
- Verify PostgreSQL user exists:
  ```bash
  psql -U postgres
  \du  # Lists all users
  ```
- Reset password if needed:
  ```sql
  ALTER USER aegisdesk_user WITH PASSWORD 'newpassword';
  ```

### Error 3: `ImportError: No module named 'psycopg2'`

**Cause**: psycopg2 not installed.

**Solution**:
```bash
pip install psycopg2-binary==2.9.9
```

If that fails on Windows:
```bash
# Download pre-built wheel from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#psycopg
# Then install: pip install psycopg2‑2.9.9‑cp311‑cp311‑win_amd64.whl
```

### Error 4: `django.db.utils.ProgrammingError: permission denied for schema public`

**Cause**: PostgreSQL 15+ changed default schema permissions.

**Solution**:
```bash
psql -U postgres -d aegisdesk

# Grant permissions:
GRANT ALL ON SCHEMA public TO aegisdesk_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO aegisdesk_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO aegisdesk_user;
```

### Error 5: `IntegrityError: duplicate key value violates unique constraint`

**Cause**: Loading data with conflicting primary keys.

**Solution**:
```bash
# Reset sequences after loading data
python manage.py sqlsequencereset incident_core | python manage.py dbshell

# Or manually:
psql -U aegisdesk_user -d aegisdesk

SELECT setval('incident_core_incidentticket_id_seq', (SELECT MAX(id) FROM incident_core_incidentticket));
SELECT setval('incident_core_asset_id_seq', (SELECT MAX(id) FROM incident_core_asset));
```

### Error 6: `relation "table_name" does not exist`

**Cause**: Migrations not applied.

**Solution**:
```bash
# Check migration status
python manage.py showmigrations

# Apply all migrations
python manage.py migrate

# If migrations are out of sync:
python manage.py migrate --fake-initial
```

### Error 7: Different SQL Behavior Between SQLite and PostgreSQL

**Issue**: Case sensitivity, date handling, or boolean fields behave differently.

**Solutions**:

**Case-insensitive queries**:
```python
# SQLite: case-insensitive by default
# PostgreSQL: case-sensitive

# Use __iexact or __icontains:
IncidentTicket.objects.filter(title__icontains='security')
```

**Boolean fields**:
```python
# SQLite: accepts 0/1
# PostgreSQL: requires True/False

# Always use Python booleans:
ticket.is_active = True  # Not 1
```

**Date/Time handling**:
```python
# PostgreSQL is stricter about timezones
# Make sure USE_TZ = True in settings.py
from django.utils import timezone
ticket.created_at = timezone.now()  # Not datetime.now()
```

### Error 8: `LoadData Error: Could not load auth.User`

**Cause**: User IDs conflict or auth data is malformed.

**Solution**:
```bash
# Skip auth data and load only app-specific data
python manage.py dumpdata incident_core --natural-foreign --natural-primary > data.json
python manage.py loaddata data.json
```

---

## Production Deployment

### Cloud Platforms with Managed PostgreSQL

#### Render.com

1. Create a PostgreSQL database in Render dashboard
2. Copy the "Internal Database URL"
3. Add environment variable in your web service:
   ```
   DATABASE_URL = [paste the internal URL]
   ```
4. Deploy your app - migrations run automatically if configured

#### Railway.app

1. Add PostgreSQL plugin to your project
2. Railway auto-sets `DATABASE_URL` environment variable
3. Deploy - database connects automatically

#### Heroku

1. Add Heroku Postgres addon:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```
2. `DATABASE_URL` is set automatically
3. Run migrations:
   ```bash
   heroku run python manage.py migrate
   ```

### Environment Variables for Production

Set these in your hosting platform:

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
DJANGO_SECRET_KEY=your-production-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## Verification Steps

After migration, verify everything works:

### 1. Database Connection Test
```bash
python manage.py dbshell
```

Should open PostgreSQL prompt. Type `\dt` to see tables.

### 2. Admin Panel Check
```
http://localhost:8000/admin
```
- Log in
- View Assets
- View Incident Tickets
- Create a new ticket

### 3. API Test
```bash
# Get JWT token
curl -X POST http://localhost:8000/incidents/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_user", "password": "your_password"}'

# Test authenticated endpoint
curl http://localhost:8000/incidents/api/v1/log-incident/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Query Performance Check
```bash
# Enable query logging in settings.py temporarily
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        }
    }
}

# Check query execution times in console
```

### 5. Data Integrity Check
```bash
python manage.py shell

from incident_core.models import IncidentTicket, Asset
print(IncidentTicket.objects.count())
print(Asset.objects.count())

# Check foreign key relationships
ticket = IncidentTicket.objects.first()
print(ticket.affected_asset)
print(ticket.reported_by)
```

---

## Rollback Instructions

If something goes wrong, you can switch back to SQLite:

### Option 1: Unset DATABASE_URL

**Windows (Command Prompt):**
```cmd
set DATABASE_URL=
```

**Windows (PowerShell):**
```powershell
Remove-Item Env:\DATABASE_URL
```

**macOS/Linux:**
```bash
unset DATABASE_URL
```

Then restart the server - it will use SQLite automatically.

### Option 2: Comment Out in settings.py

Edit `settings.py` and force SQLite:

```python
# Temporarily disable PostgreSQL
# DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = None  # Force SQLite

if DATABASE_URL:
    # ...
```

### Option 3: Restore SQLite Backup

```bash
copy db.sqlite3.backup db.sqlite3
python manage.py runserver
```

---

## Performance Tips

### 1. Connection Pooling

For production, enable connection pooling:

```python
# settings.py
DATABASES = {
    'default': {
        # ... other settings
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000',  # 30 seconds
        },
        'CONN_MAX_AGE': 600,  # 10 minutes
    }
}
```

### 2. Database Indexes

PostgreSQL benefits from proper indexes:

```bash
python manage.py dbshell
```

```sql
-- Check existing indexes
\di

-- Add custom indexes for frequently queried fields
CREATE INDEX idx_incident_severity ON incident_core_incidentticket(severity);
CREATE INDEX idx_incident_stage ON incident_core_incidentticket(nist_stage);
CREATE INDEX idx_incident_created ON incident_core_incidentticket(created_at DESC);
```

### 3. Query Optimization

Use `select_related()` and `prefetch_related()`:

```python
# Bad: N+1 queries
tickets = IncidentTicket.objects.all()
for ticket in tickets:
    print(ticket.affected_asset.name)  # Extra query each time!

# Good: Single join query
tickets = IncidentTicket.objects.select_related('affected_asset', 'reported_by')
for ticket in tickets:
    print(ticket.affected_asset.name)  # No extra query!
```

---

## Troubleshooting Checklist

If things aren't working, check:

- [ ] PostgreSQL service is running
- [ ] DATABASE_URL is set correctly (no typos)
- [ ] Database and user exist in PostgreSQL
- [ ] User has proper permissions (GRANT ALL)
- [ ] Firewall allows connections on port 5432
- [ ] psycopg2-binary is installed (`pip list | grep psycopg2`)
- [ ] Migrations are applied (`python manage.py showmigrations`)
- [ ] No conflicting environment variables
- [ ] `.env` file is in the correct location (project root)

---

## Support & Resources

- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Django Database Settings**: https://docs.djangoproject.com/en/5.0/ref/settings/#databases
- **psycopg2 Docs**: https://www.psycopg.org/docs/
- **dj-database-url**: https://github.com/jazzband/dj-database-url

---

## Success! 🎉

If you've completed all steps and tests pass, congratulations! Your AegisDesk application is now running on PostgreSQL.

**Next Steps:**
1. Update your README to reflect PostgreSQL as the production database
2. Document your deployment process
3. Set up automated backups
4. Monitor database performance
5. Configure connection pooling for production

---

**Last Updated**: June 2026  
**Tested With**: PostgreSQL 15, Django 6.0.5, Python 3.11
