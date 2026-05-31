from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django_ratelimit.decorators import ratelimit
from .forms import TicketSubmissionForm

@ratelimit(key='ip', rate='5/m', block=False)
@login_required
def submit_ticket(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return HttpResponseForbidden("Rate limit exceeded. You are restricted to 5 tickets per minute.")

    if request.method == "POST":
        form = TicketSubmissionForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket._current_user = request.user.username
            ticket.reported_by = request.user
            ticket.save()
            return redirect('ticket_success')
    else:
        form = TicketSubmissionForm()
        
    return render(request, 'incident_core/submit_ticket.html', {'form': form})

def ticket_success(request):
    return render(request, 'incident_core/success.html')