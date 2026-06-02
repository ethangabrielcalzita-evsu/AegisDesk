# Using psycopg3 with AegisDesk

## ✅ Successfully Installed!

Your AegisDesk application is now using **psycopg3** (psycopg version 3.3.4) instead of psycopg2-binary.

## Why psycopg3?

- ✅ **Better Windows Support**: Installs without C++ build tools
- ✅ **Modern**: Latest PostgreSQL adapter for Python
- ✅ **Faster**: Improved performance over psycopg2
- ✅ **Python 3.14 Compatible**: Works with newest Python versions
- ✅ **Same Django API**: No code changes needed!

## How Django Detects It

Django automatically detects and uses psycopg3. Your existing code in `settings.py` works perfectly:

```python
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

## Key Differences from psycopg2

### Import Statement (if you need manual queries)

**Old (psycopg2):**
```python
import psycopg2
conn = psycopg2.connect(DATABASE_URL)
```

**New (psycopg3):**
```python
import psycopg
conn = psycopg.connect(DATABASE_URL)
```

### Django ORM - No Changes!

All your Django code works exactly the same:

```python
# These all work identically
IncidentTicket.objects.all()
IncidentTicket.objects.filter(severity='HIGH')
ticket.save()
```

## Verification

Test that psycopg3 is installed:

```bash
python -c "import psycopg; print('psycopg3 version:', psycopg.__version__)"
```

Expected output:
```
psycopg3 version: 3.3.4
```

## Next Steps for PostgreSQL Migration

1. ✅ **psycopg3 installed** (DONE!)
2. ✅ **dj-database-url installed** (DONE!)
3. ⬜ Install PostgreSQL database
4. ⬜ Create database and user
5. ⬜ Set DATABASE_URL environment variable
6. ⬜ Run migrations

Follow the steps in `POSTGRES_QUICK_START.md` to continue!

## Troubleshooting

### "ModuleNotFoundError: No module named 'psycopg'"

**Solution:**
```bash
pip install "psycopg[binary]"
```

### Still getting psycopg2 errors?

Make sure you're not importing psycopg2 directly anywhere in your code. Search for:

```bash
# Search project for psycopg2 imports
python -c "import os; [print(f) for r, d, files in os.walk('.') for f in files if f.endswith('.py') and 'psycopg2' in open(os.path.join(r,f)).read()]"
```

### Want to switch back to psycopg2?

If you later get access to C++ build tools, you can switch:

```bash
pip uninstall psycopg psycopg-binary
pip install psycopg2-binary==2.9.9
```

Then update `requirements.txt` accordingly.

## Requirements.txt Entry

Your `requirements.txt` now contains:

```
psycopg[binary]==3.1.18
dj-database-url==2.1.0
```

This ensures anyone installing your project gets psycopg3 automatically!

## Performance Notes

psycopg3 is generally **faster** than psycopg2:

- Faster connection pooling
- Better async support (if you use it later)
- More efficient binary data handling
- Improved prepared statement caching

## Production Deployment

psycopg3 works seamlessly on all cloud platforms:

- ✅ Render.com
- ✅ Railway.app  
- ✅ Heroku
- ✅ AWS/GCP/Azure
- ✅ Any PaaS with PostgreSQL

No special configuration needed!

## Documentation

- **psycopg3 Docs**: https://www.psycopg.org/psycopg3/docs/
- **Django PostgreSQL**: https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes
- **Migration from psycopg2**: https://www.psycopg.org/psycopg3/docs/basic/from_pg2.html

## Summary

✅ **You're all set!** psycopg3 is installed and ready to use with PostgreSQL.

Proceed with the PostgreSQL database setup steps in `POSTGRES_QUICK_START.md`.
