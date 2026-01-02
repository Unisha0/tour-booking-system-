from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Tourist, Tour, Booking
from .forms import TouristSignupForm, TouristDetailForm, LoginForm, BookingForm


# Signup
def signup_view(request):
    if request.method == 'POST':
        user_form = TouristSignupForm(request.POST)
        tourist_form = TouristDetailForm(request.POST)

        if user_form.is_valid() and tourist_form.is_valid():
            user = User.objects.create_user(
                username=user_form.cleaned_data['username'],
                email=user_form.cleaned_data['email'],
                password=user_form.cleaned_data['password']
            )

            tourist = tourist_form.save(commit=False)
            tourist.user = user
            tourist.save()

            return redirect('login')
    else:
        user_form = TouristSignupForm()
        tourist_form = TouristDetailForm()

    return render(request, 'tour/signup.html', {
        'user_form': user_form,
        'tourist_form': tourist_form
    })


# Login
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'tour/login.html', {'form': form})


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


# Tourist Dashboard
@login_required
def dashboard(request):
    tours = Tour.objects.all()
    return render(request, 'tour/dashboard.html', {'tours': tours})


# Book Tour
@login_required
def book_tour(request, tour_id):
    tour = Tour.objects.get(id=tour_id)
    tourist = Tourist.objects.get(user=request.user)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tourist = tourist
            booking.tour = tour
            booking.save()
            return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, 'tour/book_tour.html', {
        'tour': tour,
        'form': form
    })