# Testing the RBAC Fix

## Quick Test Guide

This guide will help you verify that managers can no longer access employee-only pages.

---

## Setup

### 1. Start the development server

```bash
python manage.py runserver
```

### 2. Make sure you have test accounts

**Employee Account:**
- Username: `employee` (or any non-staff user)
- Password: your password
- `is_staff`: False ❌

**Manager/Admin Account:**
- Username: `admin` (or any staff user)
- Password: your password  
- `is_staff`: True ✅

If you don't have an employee account, create one:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# Create employee user
employee = User.objects.create_user(
    username='employee',
    password='testpass123',
    email='employee@example.com'
)
employee.is_staff = False  # Important: NOT a staff member
employee.save()

print("Employee user created!")
exit()
```

---

## Test Cases

### ✅ Test 1: Manager Cannot Access Submit Ticket Page

**Steps:**
1. Log in as **manager/admin**
2. Try to access: `http://localhost:8000/incidents/submit/`

**Expected Result:**
- ❌ You should be redirected to manager dashboard
- ✅ Warning message appears: "Managers cannot submit tickets. This page is for employees only."

---

### ✅ Test 2: Manager Cannot Access My Tickets

**Steps:**
1. Log in as **manager/admin**
2. Try to access: `http://localhost:8000/incidents/my-tickets/`

**Expected Result:**
- ❌ You should be redirected to manager ticket queue
- ✅ Info message appears: "Managers should use the Manager Ticket Queue."

---

### ✅ Test 3: Manager Cannot Access Employee Dashboard

**Steps:**
1. Log in as **manager/admin**
2. Try to access: `http://localhost:8000/incidents/employee/dashboard/`

**Expected Result:**
- ❌ You should be redirected to manager dashboard
- ✅ No error message (silent redirect)

---

### ✅ Test 4: Manager Cannot Access Ticket Success Page

**Steps:**
1. Log in as **manager/admin**
2. Try to access: `http://localhost:8000/incidents/submit/success/`

**Expected Result:**
- ❌ You should be redirected to manager dashboard
- ✅ No error message (silent redirect)

---

### ✅ Test 5: Manager Cannot Access Employee Guide

**Steps:**
1. Log in as **manager/admin**
2. Try to access: `http://localhost:8000/incidents/employee/guide/`

**Expected Result:**
- ❌ You should be redirected to manager guide
- ✅ No error message (silent redirect)

---

### ✅ Test 6: Original Bug - Update Flow

**This was the original reported issue. Let's verify it's fixed:**

**Steps:**
1. Log in as **manager/admin**
2. Go to: `http://localhost:8000/incidents/manager/dashboard/` (Manager Dashboard)
3. Click "View Incident Queue" or go to: `http://localhost:8000/incidents/manager/tickets/`
4. Click on a ticket to view details
5. Click "Update Stage" or go to update page
6. Update the NIST stage
7. Click Save
8. After redirect, try clicking "Back" or manually navigate to: `http://localhost:8000/incidents/my-tickets/`

**Expected Result:**
- ❌ Manager should be blocked from "My Tickets"
- ✅ Redirected to: `http://localhost:8000/incidents/manager/tickets/` (Manager Queue)
- ✅ Message: "Managers should use the Manager Ticket Queue."

---

### ✅ Test 7: Employee Can Still Access All Employee Pages

**Steps:**
1. Log in as **employee** (non-staff user)
2. Access these URLs one by one:

| URL | Expected Result |
|-----|----------------|
| `/incidents/employee/dashboard/` | ✅ Shows employee dashboard |
| `/incidents/submit/` | ✅ Shows ticket submission form |
| `/incidents/my-tickets/` | ✅ Shows employee's personal tickets |
| `/incidents/employee/guide/` | ✅ Shows employee guide |

3. Submit a ticket
4. Check that success page appears: `/incidents/submit/success/`

**Expected Result:**
- ✅ All pages load normally
- ✅ Employee can submit tickets
- ✅ Employee sees their own tickets only

---

### ✅ Test 8: Employee Cannot Access Manager Pages

**Steps:**
1. Log in as **employee** (non-staff user)
2. Try to access manager pages:

| URL | Expected Result |
|-----|----------------|
| `/incidents/manager/dashboard/` | ❌ 403 Unauthorized page |
| `/incidents/manager/tickets/` | ❌ 403 Unauthorized page |
| `/incidents/manager/guide/` | ❌ 403 Unauthorized page |

**Expected Result:**
- ❌ Access denied (403 Forbidden)
- ✅ Unauthorized page appears

---

## Quick Command Line Test

You can also test via Python shell:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from incident_core.views import _is_it_manager

# Get users
admin = User.objects.get(username='admin')
employee = User.objects.get(username='employee')

# Test the helper function
print(f"admin is_it_manager: {_is_it_manager(admin)}")  # Should be True
print(f"employee is_it_manager: {_is_it_manager(employee)}")  # Should be False

# Verify staff status
print(f"\nadmin.is_staff: {admin.is_staff}")  # Should be True
print(f"employee.is_staff: {employee.is_staff}")  # Should be False
```

---

## Automated Test Script

Create a file `test_rbac.py` in your project root:

```python
import requests

BASE_URL = "http://localhost:8000"

def test_manager_blocked_from_employee_pages():
    """Test that managers cannot access employee pages"""
    
    # Create a session (login as manager first)
    session = requests.Session()
    
    # Login as manager
    session.post(f"{BASE_URL}/accounts/login/", data={
        "username": "admin",
        "password": "your_password",
        "csrfmiddlewaretoken": "test"
    })
    
    # Test employee-only pages
    pages_to_test = [
        "/incidents/submit/",
        "/incidents/my-tickets/",
        "/incidents/employee/dashboard/",
    ]
    
    for page in pages_to_test:
        response = session.get(f"{BASE_URL}{page}", allow_redirects=False)
        if response.status_code == 302:  # Redirect
            print(f"✅ {page} - Manager correctly redirected")
        else:
            print(f"❌ {page} - Manager NOT redirected (status: {response.status_code})")

if __name__ == "__main__":
    test_manager_blocked_from_employee_pages()
```

Run it:
```bash
pip install requests
python test_rbac.py
```

---

## Success Criteria

All tests pass if:

- ✅ Managers are blocked from all employee pages
- ✅ Appropriate messages are shown
- ✅ Managers are redirected to relevant manager pages
- ✅ Employees can still access all their pages normally
- ✅ Employees are still blocked from manager pages

---

## If Tests Fail

### Manager can still access employee pages:

1. Check if `is_staff` is set correctly:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   admin = User.objects.get(username='admin')
   print(admin.is_staff)  # Should be True
   ```

2. Clear your browser cookies/cache and try again

3. Restart the Django server:
   ```bash
   Ctrl+C  # Stop server
   python manage.py runserver  # Start again
   ```

### Employees cannot access employee pages:

1. Check if employee's `is_staff` is False:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   employee = User.objects.get(username='employee')
   print(employee.is_staff)  # Should be False
   
   # If it's True, fix it:
   employee.is_staff = False
   employee.save()
   ```

---

## Reporting Results

After testing, fill out this checklist:

```
[ ] Test 1: Manager blocked from submit ticket - PASS/FAIL
[ ] Test 2: Manager blocked from my tickets - PASS/FAIL
[ ] Test 3: Manager blocked from employee dashboard - PASS/FAIL
[ ] Test 4: Manager blocked from ticket success - PASS/FAIL
[ ] Test 5: Manager blocked from employee guide - PASS/FAIL
[ ] Test 6: Original bug fixed (update flow) - PASS/FAIL
[ ] Test 7: Employee can access all employee pages - PASS/FAIL
[ ] Test 8: Employee blocked from manager pages - PASS/FAIL
```

---

**Happy Testing!** 🎉
