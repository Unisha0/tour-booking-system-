from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import AdminUser, Tourist, Tour, Booking, Hotel, Addon, Payment, TourPlace, TourImage
from .forms import AdminLoginForm, AdminSignupForm
import json


# Admin Login
def admin_login_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'adminuser'):
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                admin_user = AdminUser.objects.get(email=email)
                user = authenticate(username=admin_user.user.username, password=password)
                
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome back, {admin_user.full_name}!')
                    return redirect('admin_dashboard')
                else:
                    messages.error(request, 'Invalid credentials')
            except AdminUser.DoesNotExist:
                messages.error(request, 'Admin account not found')
    else:
        form = AdminLoginForm()
    
    return render(request, 'tour/admin/login.html', {'form': form})


# Admin Signup
def admin_signup_view(request):
    if request.method == 'POST':
        form = AdminSignupForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=full_name
                )
                AdminUser.objects.create(
                    user=user,
                    full_name=full_name,
                    email=email,
                    is_super_admin=False
                )
                messages.success(request, 'Admin account created successfully. Please login.')
                return redirect('admin_login')
    else:
        form = AdminSignupForm()
    
    return render(request, 'tour/admin/signup.html', {'form': form})


# Admin Logout
@login_required
def admin_logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('admin_login')


# Check if user is admin
def is_admin(user):
    return hasattr(user, 'adminuser')


# Admin Dashboard
@login_required
def admin_dashboard(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Statistics
    total_bookings = Booking.objects.count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    
    total_tourists = Tourist.objects.count()
    total_tours = Tour.objects.count()
    active_tours = Tour.objects.filter(is_active=True).count()
    
    total_revenue = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    pending_revenue = Payment.objects.filter(status='pending').aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related(
        'tourist', 'tour', 'hotel'
    ).prefetch_related('addons').order_by('-booking_date')[:10]
    
    # Popular tours
    popular_tours = Tour.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:5]
    
    context = {
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'pending_bookings': pending_bookings,
        'cancelled_bookings': cancelled_bookings,
        'total_tourists': total_tourists,
        'total_tours': total_tours,
        'active_tours': active_tours,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
        'recent_bookings': recent_bookings,
        'popular_tours': popular_tours,
    }
    
    return render(request, 'tour/admin/dashboard.html', context)


# View All Bookings
@login_required
def admin_bookings_list(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    status_filter = request.GET.get('status', '')
    search_query = request.GET.get('search', '')
    
    bookings = Booking.objects.select_related(
        'tourist', 'tour', 'hotel'
    ).prefetch_related('addons').order_by('-booking_date')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if search_query:
        bookings = bookings.filter(
            Q(tourist__name__icontains=search_query) |
            Q(tour__title__icontains=search_query) |
            Q(tourist__email__icontains=search_query)
        )
    
    context = {
        'bookings': bookings,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'tour/admin/bookings_list.html', context)


# View Booking Details
@login_required
def admin_booking_detail(request, booking_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    booking = get_object_or_404(
        Booking.objects.select_related('tourist', 'tour', 'hotel')
        .prefetch_related('addons'),
        id=booking_id
    )
    
    try:
        payment = Payment.objects.get(booking=booking)
    except Payment.DoesNotExist:
        payment = None
    
    context = {
        'booking': booking,
        'payment': payment,
    }
    
    return render(request, 'tour/admin/booking_detail.html', context)


# Cancel Booking
@login_required
def admin_cancel_booking(request, booking_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled')
        return redirect('admin_bookings_list')
    
    return render(request, 'tour/admin/cancel_booking.html', {'booking': booking})


# View All Tourists/Users
@login_required
def admin_tourists_list(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    
    tourists = Tourist.objects.select_related('user').annotate(
        booking_count=Count('booking')
    ).order_by('-created_at')
    
    if search_query:
        tourists = tourists.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    context = {
        'tourists': tourists,
        'search_query': search_query,
    }
    
    return render(request, 'tour/admin/tourists_list.html', context)


# View Tourist Details
@login_required
def admin_tourist_detail(request, tourist_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    tourist = get_object_or_404(Tourist, id=tourist_id)
    bookings = Booking.objects.filter(tourist=tourist).select_related(
        'tour', 'hotel'
    ).order_by('-booking_date')
    
    context = {
        'tourist': tourist,
        'bookings': bookings,
    }
    
    return render(request, 'tour/admin/tourist_detail.html', context)


# View All Tours
@login_required
def admin_tours_list(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    search_query = request.GET.get('search', '')
    active_filter = request.GET.get('active', '')
    
    tours = Tour.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-created_at')
    
    if search_query:
        tours = tours.filter(
            Q(title__icontains=search_query) |
            Q(destination__icontains=search_query)
        )
    
    if active_filter:
        tours = tours.filter(is_active=(active_filter == 'true'))
    
    context = {
        'tours': tours,
        'search_query': search_query,
        'active_filter': active_filter,
    }
    
    return render(request, 'tour/admin/tours_list.html', context)


# View Tour Details
@login_required
def admin_tour_detail(request, tour_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    tour = get_object_or_404(
        Tour.objects.prefetch_related('places', 'images'),
        id=tour_id
    )
    
    # Get tour statistics
    bookings = Booking.objects.filter(tour=tour)
    total_bookings = bookings.count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    total_revenue = Payment.objects.filter(
        booking__tour=tour,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent bookings for this tour
    recent_bookings = bookings.select_related('tourist').order_by('-booking_date')[:10]
    
    context = {
        'tour': tour,
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_revenue': total_revenue,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'tour/admin/tour_detail.html', context)


# Add New Tour
@login_required
def admin_tour_create(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        # Get basic tour data
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        duration_days = request.POST.get('duration_days')
        base_price = request.POST.get('base_price')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        
        # Create tour
        tour = Tour.objects.create(
            title=title,
            destination=destination,
            duration_days=duration_days,
            base_price=base_price,
            description=description,
            is_active=is_active
        )
        
        # Handle multiple images
        images = request.FILES.getlist('images')
        for image in images:
            TourImage.objects.create(tour=tour, image=image)
        
        # Handle places
        place_titles = request.POST.getlist('place_title[]')
        place_descriptions = request.POST.getlist('place_description[]')
        
        for title_text, desc in zip(place_titles, place_descriptions):
            if title_text and desc:
                TourPlace.objects.create(
                    tour=tour,
                    title=title_text,
                    description=desc
                )
        
        messages.success(request, f'Tour "{tour.title}" created successfully!')
        return redirect('admin_tour_detail', tour_id=tour.id)
    
    return render(request, 'tour/admin/tour_form.html', {'mode': 'create'})


# Edit Tour
@login_required
def admin_tour_edit(request, tour_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    tour = get_object_or_404(
        Tour.objects.prefetch_related('places', 'images'),
        id=tour_id
    )
    
    if request.method == 'POST':
        # Update basic tour data
        tour.title = request.POST.get('title')
        tour.destination = request.POST.get('destination')
        tour.duration_days = request.POST.get('duration_days')
        tour.base_price = request.POST.get('base_price')
        tour.description = request.POST.get('description')
        tour.is_active = request.POST.get('is_active') == 'on'
        tour.save()
        
        # Handle new images
        images = request.FILES.getlist('images')
        for image in images:
            TourImage.objects.create(tour=tour, image=image)
        
        # Handle places update
        # Delete old places if requested
        delete_place_ids = request.POST.getlist('delete_place[]')
        if delete_place_ids:
            TourPlace.objects.filter(id__in=delete_place_ids).delete()
        
        # Add new places
        place_titles = request.POST.getlist('place_title[]')
        place_descriptions = request.POST.getlist('place_description[]')
        
        for title_text, desc in zip(place_titles, place_descriptions):
            if title_text and desc:
                TourPlace.objects.create(
                    tour=tour,
                    title=title_text,
                    description=desc
                )
        
        messages.success(request, f'Tour "{tour.title}" updated successfully!')
        return redirect('admin_tour_detail', tour_id=tour.id)
    
    context = {
        'mode': 'edit',
        'tour': tour,
    }
    return render(request, 'tour/admin/tour_form.html', context)


# Delete Tour Image
@login_required
def admin_tour_delete_image(request, image_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    image = get_object_or_404(TourImage, id=image_id)
    tour_id = image.tour.id
    image.delete()
    
    messages.success(request, 'Image deleted successfully')
    return redirect('admin_tour_edit', tour_id=tour_id)


# Toggle Tour Active Status
@login_required
def admin_tour_toggle_status(request, tour_id):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    tour = get_object_or_404(Tour, id=tour_id)
    tour.is_active = not tour.is_active
    tour.save()
    
    status = "activated" if tour.is_active else "deactivated"
    messages.success(request, f'Tour "{tour.title}" has been {status}')
    return redirect('admin_tour_detail', tour_id=tour_id)


# Reports/Analytics
@login_required
def admin_reports(request):
    if not is_admin(request.user):
        messages.error(request, 'Access denied')
        return redirect('home')
    
    # Monthly booking statistics
    current_month = timezone.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_month_bookings = Booking.objects.filter(
        booking_date__gte=current_month
    ).count()
    
    last_month_bookings = Booking.objects.filter(
        booking_date__gte=last_month,
        booking_date__lt=current_month
    ).count()
    
    # Revenue statistics
    current_month_revenue = Payment.objects.filter(
        booking__booking_date__gte=current_month,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    last_month_revenue = Payment.objects.filter(
        booking__booking_date__gte=last_month,
        booking__booking_date__lt=current_month,
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Top destinations
    top_destinations = Tour.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:10]
    
    # Booking status distribution
    status_distribution = Booking.objects.values('status').annotate(
        count=Count('id')
    )
    
    context = {
        'current_month_bookings': current_month_bookings,
        'last_month_bookings': last_month_bookings,
        'current_month_revenue': current_month_revenue,
        'last_month_revenue': last_month_revenue,
        'top_destinations': top_destinations,
        'status_distribution': status_distribution,
    }
    
    return render(request, 'tour/admin/reports.html', context)
