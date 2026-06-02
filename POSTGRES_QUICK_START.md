# PostgreSQL Quick Start Guide

**5-Minute Setup for AegisDesk**

---

## Prerequisites

- PostgreSQL installed and running
- Virtual environment activated

---

## Quick Steps

### 1. Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

This installs `psycopg2-binary` and `dj-database-url`.

---

### 2. Create Database (1 minute)

```bash
# Open PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE aegisdesk;
CREATE USER aegisdesk_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE aegisdesk TO aegisdesk_user;

# For PostgreSQL 15+ (grant schema permissions)
\c aegisdesk
GRANT ALL ON SCHEMA public TO aegisdesk_user;

# Exit
\q
```

---

### 3. Set Environment Variable (30 seconds)

**Windows (CMD):**
```cmd
set DATABASE_URL=postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk
```

**Windows (PowerShell):**
```powershell
$env:DATABASE_URL="postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk"
```

**macOS/Linux:**
```bash
export DATABASE_URL="postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk"
```

---

### 4. Migrate Database (1 minute)

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_incidents  # Optional: sample data
```

---

### 5. Run Server (30 seconds)

```bash
python manage.py runserver
```

Visit `http://localhost:8000` ✅

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `psycopg2` not found | `pip install psycopg2-binary` |
| Connection refused | Start PostgreSQL service |
| Permission denied | Run `GRANT ALL ON SCHEMA public TO aegisdesk_user;` |
| DATABASE_URL not working | Make sure no spaces in the URL string |

---

## Permanent Environment Variable (Optional)

Instead of setting `DATABASE_URL` every time:

### Option A: Create .env file

```bash
# Create .env in project root
echo DATABASE_URL=postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk > .env

# Install python-dotenv
pip install python-dotenv
```

Add to `settings.py` (top):
```python
from dotenv import load_dotenv
load_dotenv()
```

### Option B: System Environment Variable

**Windows:**
1. Search "Environment Variables" in Start Menu
2. Click "Environment Variables" button
3. Under "User variables", click "New"
4. Variable name: `DATABASE_URL`
5. Variable value: `postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk`
6. Restart terminal/IDE

**macOS/Linux:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export DATABASE_URL="postgresql://aegisdesk_user:yourpassword@localhost:5432/aegisdesk"
```

---

## Verification Commands

```bash
# Test database connection
python manage.py check --database default

# View database tables
python manage.py dbshell
\dt

# Check applied migrations
python manage.py showmigrations
```

---

## Switch Back to SQLite

Unset the environment variable:

**Windows (CMD):** `set DATABASE_URL=`  
**Windows (PowerShell):** `Remove-Item Env:\DATABASE_URL`  
**macOS/Linux:** `unset DATABASE_URL`

Then restart the server - SQLite will be used automatically.

---

**Need more details?** See `POSTGRESQL_MIGRATION_GUIDE.md`
