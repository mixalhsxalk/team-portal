from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Item, ItemRequest
from .forms import ItemForm

@login_required
def item_list(request):
    # Filters come from the URL (e.g. ?q=esp32&category=microcontrollers)
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    # Only items in stock
    items = Item.objects.filter(quantity__gt=0).exclude(owner=request.user)

    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    if category_filter:
        items = items.filter(category=category_filter)

    context = {
        'items': items,
        'categories': Item.CATEGORY_CHOICES,
        'current_q': query,
        'current_cat': category_filter
    }
    return render(request, 'items/list.html', context)

@login_required
def my_items(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, 'items/my_items.html', {'items': items})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Item added successfully!')
            return redirect('my-items')
    else:
        form = ItemForm()
    return render(request, 'items/form.html', {'form': form, 'title': 'New Item'})

@login_required
@require_POST
def request_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.owner == request.user:
        messages.error(request, "You can't request your own item.")
        return redirect('item-list')

    if item.quantity <= 0:
        messages.error(request, 'This item is no longer available.')
        return redirect('item-list')

    existing_req = ItemRequest.objects.filter(item=item, requester=request.user, status='pending').exists()
    
    if existing_req:
        messages.warning(request, 'You already have a pending request for this item.')
    else:
        ItemRequest.objects.create(item=item, requester=request.user)
        messages.success(request, f'Request for "{item.name}" sent to {item.owner.username}!')
        
    return redirect('item-list')

@login_required
def my_requests(request):
    outgoing = ItemRequest.objects.filter(requester=request.user).order_by('-created_at')
    incoming = ItemRequest.objects.filter(item__owner=request.user).order_by('-created_at')
    return render(request, 'items/requests.html', {'outgoing': outgoing, 'incoming': incoming})

@login_required
@require_POST
def respond_request(request, pk, action):
    req = get_object_or_404(ItemRequest, pk=pk, item__owner=request.user)

    # Allowed transitions: pending -> approved/rejected, approved -> returned
    allowed = {'approve': 'pending', 'reject': 'pending', 'return': 'approved'}
    if allowed.get(action) != req.status:
        messages.error(request, 'Invalid action for this request.')
        return redirect('my-requests')

    if action == 'approve':
        if req.item.quantity > 0:
            req.status = 'approved'
            req.item.quantity -= 1
            req.item.save()
            messages.success(request, f'You approved the request from {req.requester.username}!')
        else:
            messages.error(request, 'Not enough stock to approve this request.')
            
    elif action == 'reject':
        req.status = 'rejected'
        messages.error(request, 'Request rejected.')
        
    elif action == 'return':
        req.status = 'returned'
        req.item.quantity += 1
        req.item.save()
        messages.info(request, 'Item returned and stock updated.')
        
    req.save()
    return redirect('my-requests')