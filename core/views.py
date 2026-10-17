from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from items.models import Item, ItemRequest
from timeoff.models import LeaveRequest

@login_required
def dashboard(request):
    # --- 1. Stats ---
    total_items = Item.objects.filter(quantity__gt=0).count()
    pending_requests = ItemRequest.objects.filter(status='pending').count()
    active_requests = ItemRequest.objects.filter(status='approved').count()
    my_pending_requests = ItemRequest.objects.filter(item__owner=request.user, status='pending').count()

    today = timezone.localdate()
    approved_leaves = LeaveRequest.objects.filter(status='approved')
    absent_today_count = approved_leaves.filter(start_date__lte=today, end_date__gte=today).count()
    my_upcoming_leaves_count = approved_leaves.filter(user=request.user, end_date__gte=today).count()

    # --- 2. Showcase (search & filters) ---
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    # Only available items that don't belong to the current user
    items = Item.objects.filter(quantity__gt=0).exclude(owner=request.user)

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_filter:
        items = items.filter(category=category_filter)

    context = {
        'total_items': total_items,
        'pending_requests': pending_requests,
        'active_requests': active_requests,
        'my_pending_requests': my_pending_requests,
        'absent_today_count': absent_today_count,
        'my_upcoming_leaves_count': my_upcoming_leaves_count,
        
        # Showcase data
        'items': items,
        'categories': Item.CATEGORY_CHOICES,
        'current_q': query,
        'current_cat': category_filter
    }
    return render(request, 'dashboard.html', context)