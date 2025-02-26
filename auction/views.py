from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Item
from .models import Bid
from django.contrib import messages
import json
from auction.fomrs import *


def index(request):
    most_expensive_items = Item.objects.order_by('-price')[:5]
    ending_soonest_items = sorted(Item.objects.all(), key=lambda x: x.get_time_left())[:5]
    most_viewed_items = Item.objects.order_by('-views_count')[:5]

    context = {
        'most_expensive_items': most_expensive_items,
        'ending_soonest_items': ending_soonest_items,
        'most_viewed_items': most_viewed_items,
    }

    return render(request, 'auction/index.html', context)

def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard') 
        else:
            context = {'error': 'نام کاربری یا رمز عبور اشتباه است.'}
            return render(request, 'auction/signin.html', context)
    return render(request, 'auction/signin.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auction/signup.html', {'form': form})   

@login_required
def dashboard(request):
    sort_by = request.GET.get('sortby', 'created_at')

    if sort_by == 'likes':
        order_field = '-likes_count'
    elif sort_by == 'price':
        order_field = '-price'
    elif sort_by == 'views':
        order_field = '-views_count'
    elif sort_by == 'bids':
        order_field = '-bid_count'
    else:
        order_field = '-created_at'

    user_items_queryset = Item.objects.filter(created_by=request.user).order_by(order_field)
    page = request.GET.get('page', 1)
    paginator = Paginator(user_items_queryset, 10)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    
    other_items = Item.objects.exclude(created_by=request.user).order_by('-created_at')[:5]
    liked_items = Item.objects.filter(likes_count__gt=0).exclude(created_by=request.user).order_by('-likes_count')[:5]

    context = {
        'items': items,
        'other_items': other_items,
        'liked_items': liked_items,
    }
    return render(request, 'auction/dashboard.html', context)



def item(request):
    return render(request,'auction/item.html')

@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES) 
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.created_by = request.user
            new_item.save()
            return redirect('dashboard')
    else:
        form = NewItemForm()
    return render(request, 'auction/new_item.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('index') 

def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    bids = Bid.objects.filter(item=item).order_by('created_at')
    bid_history = [{'time': bid.created_at.isoformat(), 'amount': float(bid.amount)} for bid in bids]

    if bid_history:
        bid_history.insert(0, {'time': item.created_at.isoformat(), 'amount': 0.0})

    context = {
        'item': item,
        'bid_history': json.dumps(bid_history),  
    }
    return render(request, 'auction/item.html', context)


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user != item.created_by:
        return redirect('item', item_id=item.id)
    
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item', item_id=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'auction/edit_item.html', {'form': form, 'item': item})


@login_required
def item_list(request):
    items_queryset = Item.objects.exclude(created_by=request.user).order_by('-created_at')
    paginator = Paginator(items_queryset, 9)
    page = request.GET.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)  
    except EmptyPage:
        items = paginator.page(paginator.num_pages)  

    return render(request, 'auction/item_list.html', {'items': items})


@login_required
def bid_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if item.get_time_left() == "Expired":
        messages.error(request, "This auction has ended. No more bids allowed.")
        return redirect('item', item_id=item.id)  
    
    if request.method == 'POST':
        try:
            bid_amount = float(request.POST.get('bid_amount', 0))
        except ValueError:
            messages.error(request, "Invalid bid amount.")
            return redirect('item', item_id=item.id)

        if bid_amount > item.price:
            new_bid = Bid.objects.create(
                item=item,
                bidder=request.user,
                amount=bid_amount,
                created_at=timezone.now()
            )
            item.price = bid_amount
            item.bid_count += 1
            item.save()
            messages.success(request, "Your bid has been placed successfully.")
        else:
            messages.error(request, "Your bid must be higher than the current highest bid.")

    return redirect('item', item_id=item.id)

def about(request):
    return render(request,'auction/about.html')

def contact(request):
    return render(request,'auction/contact.html')

def policy(request):
    return render(request,'auction/policy.html')

def search_results(request):
    query = request.GET.get('q', '') 
    results = Item.objects.filter(name__icontains=query) | Item.objects.filter(description__icontains=query)  
    context = {
        'query': query,
        'results': results
    }
    return render(request, 'auction/search_results.html', context)
