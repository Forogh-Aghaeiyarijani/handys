from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Booking, Service # Import Service model
from .forms import CustomUserCreationForm, HandymanCreationForm, BookingForm

def home(request):
    services = Service.objects.all()
    context = {
        'services': services
    }
    return render(request, "index.htm", context)

@login_required
def user_page(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-date', '-time')
    context = {
        'user': user,
        'bookings': bookings,
    }
    return render(request, "user_page.html", context)

def handyman_page(request):
    return render(request, "handyman_page.html")

def client_signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to home page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'client_signup.html', {'form': form})

def handyman_signup_view(request):
    if request.method == 'POST':
        form = HandymanCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home') # Redirect to home page after signup
    else:
        form = HandymanCreationForm()
    return render(request, 'handyman_signup.html', {'form': form})

def role_selection_view(request):
    return render(request, 'role_selection.html')

@login_required
def book_service_view(request, service_id=None):
    initial_data = {}
    if service_id:
        try:
            service = Service.objects.get(id=service_id)
            initial_data['service'] = service
        except Service.DoesNotExist:
            pass

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('user_page') # Redirect to the user's dashboard after booking
    else:
        form = BookingForm(initial=initial_data)
    
    context = {'form': form}
    return render(request, 'book_service.html', context)

# Create your views here.
