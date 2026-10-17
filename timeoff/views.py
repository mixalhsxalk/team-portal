from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import LeaveRequest
from .forms import LeaveRequestForm

# 1. Ποιος λείπει σήμερα / αυτή την περίοδο (Για όλη την ομάδα)
@login_required
def team_status(request):
    today = timezone.localdate()
    
    # Βρίσκουμε όσους λείπουν *σήμερα* (εγκεκριμένες άδειες)
    absent_today = LeaveRequest.objects.filter(
        status='approved',
        start_date__lte=today,
        end_date__gte=today
    ).order_by('end_date')

    # Επερχόμενες άδειες (για να ξέρουμε ποιος θα λείψει σύντομα)
    upcoming_leaves = LeaveRequest.objects.filter(
        status='approved',
        start_date__gt=today
    ).order_by('start_date')[:5]

    return render(request, 'timeoff/team_status.html', {
        'absent_today': absent_today,
        'upcoming_leaves': upcoming_leaves,
        'today': today
    })

# 2. Το ιστορικό των αδειών μου
@login_required
def my_leaves(request):
    leaves = LeaveRequest.objects.filter(user=request.user).order_by('-start_date')
    return render(request, 'timeoff/my_leaves.html', {'leaves': leaves})

# 3. Αίτηση για νέα άδεια
@login_required
def request_leave(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            messages.success(request, 'Το αίτημα άδειας καταχωρήθηκε και εκκρεμεί έγκριση!')
            return redirect('my-leaves')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'timeoff/request_form.html', {'form': form})