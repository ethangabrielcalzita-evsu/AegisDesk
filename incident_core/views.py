from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django.db.models import Q, Count
from .forms import TicketSubmissionForm, NistTriageForm, BulkCloseForm
from .models import IncidentTicket


def _is_it_manager(user):
    return user.is_authenticated and user.is_staff


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


@login_required
def employee_dashboard(request):
    """
    End-User / Employee Dashboard
    Shows personal ticket metrics and recent submissions
    """
    user_tickets = IncidentTicket.objects.filter(reported_by=request.user).order_by('-created_at')
    
    # Personal stats
    total_submitted = user_tickets.count()
    open_tickets = user_tickets.exclude(nist_stage='CLOSED').count()
    resolved_tickets = user_tickets.filter(nist_stage='CLOSED').count()
    
    # Recent tickets
    recent_tickets = user_tickets[:5]
    
    context = {
        'total_submitted': total_submitted,
        'open_tickets': open_tickets,
        'resolved_tickets': resolved_tickets,
        'recent_tickets': recent_tickets,
        'user_type': 'employee',
    }
    return render(request, 'employee_dashboard.html', context)


@login_required
def employee_guide(request):
    return render(request, 'employee_guide.html')


@login_required
@ratelimit(key='ip', rate='5/m', block=False)
def submit_ticket(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        messages.error(request, 'Too many requests. Please wait before submitting another ticket.')

    if request.method == 'POST':
        form = TicketSubmissionForm(request.POST)
        if not was_limited and form.is_valid():
            ticket = form.save(commit=False)
            ticket._current_user = request.user.username
            ticket.reported_by = request.user
            ticket.save()
            messages.success(request, 'Your ticket has been securely submitted.')
            return redirect('ticket_success')
    else:
        form = TicketSubmissionForm()

    return render(request, 'tickets/submit_ticket.html', {'form': form})


@login_required
def ticket_success(request):
    return render(request, 'tickets/success.html')


@login_required
def my_tickets(request):
    tickets = IncidentTicket.objects.filter(reported_by=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})


@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(IncidentTicket, pk=ticket_id)
    if ticket.reported_by != request.user and not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})


@login_required
def manager_dashboard(request):
    """
    IT Manager / SecOps Dashboard
    NIST Incident Response Framework tracking and incident metrics
    """
    if not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)

    all_tickets = IncidentTicket.objects.all()
    
    # NIST stage breakdown
    stage_counts = {
        label: all_tickets.filter(nist_stage=value).count()
        for value, label in IncidentTicket.NIST_STAGES
    }
    
    # Key metrics
    total_tickets = all_tickets.count()
    total_open = all_tickets.exclude(nist_stage='CLOSED').count()
    total_closed = all_tickets.filter(nist_stage='CLOSED').count()
    critical_high = all_tickets.filter(severity__in=['CRITICAL', 'HIGH']).count()
    
    # Severity breakdown
    severity_breakdown = {
        'critical': all_tickets.filter(severity='CRITICAL').count(),
        'high': all_tickets.filter(severity='HIGH').count(),
        'medium': all_tickets.filter(severity='MEDIUM').count(),
        'low': all_tickets.filter(severity='LOW').count(),
    }
    
    context = {
        'stage_counts': stage_counts,
        'total_open': total_open,
        'total_tickets': total_tickets,
        'total_closed': total_closed,
        'critical_high': critical_high,
        'severity_breakdown': severity_breakdown,
        'user_type': 'manager',
    }
    return render(request, 'manager/manager_dashboard.html', context)


@login_required
def manager_guide(request):
    if not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)
    return render(request, 'manager/manager_guide.html')


@login_required
def ticket_list(request):
    if not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)

    open_tickets = IncidentTicket.objects.exclude(nist_stage='CLOSED').order_by('-created_at')
    form = BulkCloseForm(request.POST or None, queryset=open_tickets)

    if request.method == 'POST' and form.is_valid():
        tickets_to_close = form.cleaned_data.get('selected_tickets')
        for ticket in tickets_to_close:
            ticket._current_user = request.user.username
            ticket.nist_stage = 'CLOSED'
            ticket.save()
        if tickets_to_close:
            messages.success(request, f'{tickets_to_close.count()} ticket(s) were closed successfully.')
            return redirect('ticket_list')
        messages.warning(request, 'No tickets were selected for bulk close.')

    return render(request, 'manager/ticket_list.html', {
        'tickets': open_tickets,
        'bulk_form': form,
    })


@login_required
def update_incident(request, ticket_id):
    if not _is_it_manager(request.user):
        return render(request, 'unauthorized.html', status=403)

    ticket = get_object_or_404(IncidentTicket, pk=ticket_id)
    if request.method == 'POST':
        form = NistTriageForm(request.POST, instance=ticket)
        if form.is_valid():
            updated_ticket = form.save(commit=False)
            updated_ticket._current_user = request.user.username
            updated_ticket.save()
            messages.success(request, 'Ticket stage updated and chain-of-custody recorded.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = NistTriageForm(instance=ticket)

    return render(request, 'manager/update_incident.html', {
        'form': form,
        'ticket': ticket,
    })


def unauthorized_view(request, exception=None):
    return render(request, 'unauthorized.html', status=403)