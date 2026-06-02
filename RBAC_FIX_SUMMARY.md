# RBAC Access Control Fix

## Problem Identified

Managers/admins were able to access employee-only pages through navigation flow:
1. Admin Dashboard → View Incident Queue → Update Incident Stage
2. Incident Updated → Back to "My Tickets" 
3. Opens My Ticket History → **Admin gains access to Submit New Ticket page**

This violated role separation principles where only employees should submit tickets.

---

## Solution Implemented

Added manager access restrictions to **all employee-only views**:

### Views Protected:

1. **`submit_ticket`** - Ticket submission form
2. **`ticket_success`** - Success confirmation page
3. **`my_tickets`** - Personal ticket history
4. **`employee_dashboard`** - Employee dashboard
5. **`employee_guide`** - Employee help guide

### How It Works:

Each protected view now checks if the user is a manager using `_is_it_manager(request.user)`:

```python
if _is_it_manager(request.user):
    # Redirect to appropriate manager page with message
    messages.warning(request, 'This page is for employees only.')
    return redirect('manager_dashboard')
```

---

## Code Changes

### 1. `submit_ticket` View

**Before:**
```python
@login_required
@ratelimit(key='ip', rate='5/m', block=False)
def submit_ticket(request):
    # No manager check
    ...
```

**After:**
```python
@login_required
@ratelimit(key='ip', rate='5/m', block=False)
def submit_ticket(request):
    # Block managers from submitting tickets
    if _is_it_manager(request.user):
        messages.warning(request, 'Managers cannot submit tickets. This page is for employees only.')
        return redirect('manager_dashboard')
    ...
```

### 2. `my_tickets` View

**Before:**
```python
@login_required
def my_tickets(request):
    tickets = IncidentTicket.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})
```

**After:**
```python
@login_required
def my_tickets(request):
    # Redirect managers to their ticket queue
    if _is_it_manager(request.user):
        messages.info(request, 'Managers should use the Manager Ticket Queue.')
        return redirect('ticket_list')
    
    tickets = IncidentTicket.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})
```

### 3. `employee_dashboard` View

**After:**
```python
@login_required
def employee_dashboard(request):
    # Managers redirected to manager dashboard
    if _is_it_manager(request.user):
        return redirect('manager_dashboard')
    ...
```

### 4. `ticket_success` View

**After:**
```python
@login_required
def ticket_success(request):
    # Managers should not see success page
    if _is_it_manager(request.user):
        return redirect('manager_dashboard')
    
    return render(request, 'tickets/success.html')
```

### 5. `employee_guide` View

**After:**
```python
@login_required
def employee_guide(request):
    # Redirect managers to manager guide
    if _is_it_manager(request.user):
        return redirect('manager_guide')
    
    return render(request, 'employee_guide.html')
```

---

## Access Control Matrix

| Page/View | Employee Access | Manager Access | Redirect Destination (Manager) |
|-----------|----------------|----------------|--------------------------------|
| **Employee Dashboard** | ✅ Allowed | ❌ Blocked | `manager_dashboard` |
| **Submit Ticket** | ✅ Allowed | ❌ Blocked | `manager_dashboard` (with warning) |
| **My Tickets** | ✅ Allowed | ❌ Blocked | `ticket_list` (Manager Queue) |
| **Ticket Success** | ✅ Allowed | ❌ Blocked | `manager_dashboard` |
| **Employee Guide** | ✅ Allowed | ❌ Blocked | `manager_guide` |
| **Manager Dashboard** | ❌ Blocked | ✅ Allowed | N/A |
| **Manager Ticket Queue** | ❌ Blocked | ✅ Allowed | N/A |
| **Update Incident** | ❌ Blocked | ✅ Allowed | N/A |
| **Ticket Detail** | ✅ Own tickets only | ✅ All tickets | N/A |

---

## User Experience Flow

### Employee Flow (Unchanged):
```
Login → Employee Dashboard → Submit Ticket → Success
           ↓
        My Tickets → View Ticket Detail
```

### Manager Flow (Fixed):
```
Login → Manager Dashboard → Ticket Queue → Update Ticket → Ticket Detail
           ↓
   [Blocked from Employee Pages]
```

### Attempting to Access Employee Page as Manager:
```
Manager tries to access: /incidents/submit/
     ↓
   Access Denied
     ↓
   Redirected to: Manager Dashboard
     ↓
   Message displayed: "Managers cannot submit tickets. This page is for employees only."
```

---

## Security Benefits

1. **Principle of Least Privilege**: Managers can't access employee functions
2. **Role Separation**: Clear boundary between employee and manager capabilities
3. **Audit Trail Integrity**: Tickets always submitted by employees, never managers
4. **User Experience**: Appropriate redirects prevent confusion

---

## Testing Checklist

### As Manager/Admin:

- [ ] Try accessing `/incidents/submit/` → Should redirect to manager dashboard
- [ ] Try accessing `/incidents/my-tickets/` → Should redirect to ticket list
- [ ] Try accessing `/incidents/employee/dashboard/` → Should redirect to manager dashboard
- [ ] Try accessing `/incidents/employee/guide/` → Should redirect to manager guide
- [ ] Try accessing `/incidents/submit/success/` → Should redirect to manager dashboard
- [ ] Update a ticket → Should redirect to ticket detail (NOT my tickets)

### As Employee:

- [ ] Access `/incidents/submit/` → Should show form
- [ ] Submit ticket → Should show success page
- [ ] Access `/incidents/my-tickets/` → Should show personal tickets
- [ ] Try accessing `/incidents/manager/dashboard/` → Should show 403 Unauthorized
- [ ] Try accessing `/incidents/manager/tickets/` → Should show 403 Unauthorized

---

## Implementation Notes

### Helper Function Used:

```python
def _is_it_manager(user):
    return user.is_authenticated and user.is_staff
```

This function checks if a user has `is_staff` flag, which designates them as a manager/admin.

### Message Framework:

The fix uses Django's messages framework to inform users why they're being redirected:

- `messages.warning()` - For access denied scenarios
- `messages.info()` - For informational redirects

---

## Rollback Instructions

If you need to revert this change (not recommended), remove the manager checks:

```python
# Remove these blocks from each view:
if _is_it_manager(request.user):
    return redirect('...')
```

---

## Related Documentation

- Django Messages Framework: https://docs.djangoproject.com/en/5.0/ref/contrib/messages/
- Django Authentication: https://docs.djangoproject.com/en/5.0/topics/auth/
- Role-Based Access Control: https://en.wikipedia.org/wiki/Role-based_access_control

---

## Conclusion

✅ **Access control properly enforced**  
✅ **Managers blocked from employee-only pages**  
✅ **Appropriate redirects with user-friendly messages**  
✅ **Security and audit trail integrity maintained**

---

**Date Fixed**: June 3, 2026  
**Files Modified**: `incident_core/views.py`  
**Lines Changed**: 6 view functions updated with access control checks
