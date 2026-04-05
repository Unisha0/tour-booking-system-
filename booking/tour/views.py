from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Tourist, Tour, Booking, Hotel, Addon, Payment
from .forms import TouristSignupForm, TouristDetailForm, TouristLoginForm, BookingForm
import random
import string


# ---------- Signup ----------
def signup_view(request):
    if request.method == 'POST':
        form = TouristSignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']

            if User.objects.filter(username=phone).exists():
                form.add_error('phone_number', "Phone number already registered.")
            else:
                user = User.objects.create_user(username=phone, email=email, password=password, first_name=name)
                Tourist.objects.create(user=user, name=name, email=email, phone=phone)
                messages.success(request, 'Signup successful. Please login.')
                return redirect('login')
    else:
        form = TouristSignupForm()

    return render(request, 'tour/signup.html', {'form': form})


# ---------- Login ----------
def login_view(request):
    if request.method == 'POST':
        form = TouristLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier'].strip()
            password = form.cleaned_data['password']

            # Try username
            user = authenticate(username=identifier, password=password)

            # Try phone number if username fails
            if not user and identifier.isdigit() and len(identifier) == 10:
                try:
                    tourist = Tourist.objects.get(phone=identifier)
                    user = authenticate(username=tourist.user.username, password=password)
                except Tourist.DoesNotExist:
                    user = None

            if user:
                login(request, user)
                tourist, _ = Tourist.objects.get_or_create(user=user)
                if not tourist.phone:
                    return redirect('complete_profile')
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid credentials')
    else:
        form = TouristLoginForm()

    return render(request, 'tour/login.html', {'form': form})


# ---------- Logout ----------
def logout_view(request):
    logout(request)
    return redirect('login')


# ---------- Dashboard / Tours List ----------
def dashboard(request):
    # Get all active tours with images
    tours_qs = Tour.objects.prefetch_related('images').filter(is_active=True)

    # Convert QuerySet to JSON-serializable list of dictionaries
    tours = []
    for tour in tours_qs:
        tours.append({
            'id': tour.id,
            'title': tour.title,
            'destination': tour.destination,
            'duration_days': tour.duration_days,
            'description': tour.description,
            'base_price': tour.base_price,
            'images': [{'image': img.image.url} for img in tour.images.all()]
        })
    
    # Check if user has an active booking
    has_active_booking = False
    active_booking = None
    if request.user.is_authenticated:
        try:
            tourist = Tourist.objects.get(user=request.user)
            active_booking = tourist.get_active_booking()
            has_active_booking = active_booking is not None
        except Tourist.DoesNotExist:
            pass

    context = {
        'tours': tours,
        'has_active_booking': has_active_booking,
        'active_booking': active_booking,
    }
    return render(request, 'tour/dashboard.html', context)


# ---------- Tour Details & Booking ----------
def book_tour(request, tour_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Please sign in to book a tour.')
        return redirect('login')

    tour = get_object_or_404(Tour, id=tour_id, is_active=True)
    tourist = Tourist.objects.filter(user=request.user).first()
    if not tourist:
        messages.info(request, 'Please complete your profile to continue.')
        return redirect('complete_profile')

    # Check if user already has an active booking (pending or confirmed)
    existing_booking = Booking.objects.filter(
        tourist=tourist,
        status__in=['pending', 'confirmed']
    ).first()
    
    if existing_booking:
        messages.warning(request, f'You already have an active booking for {existing_booking.tour.title}. Please complete or cancel it before making a new booking.')
        return redirect('my_bookings')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.tourist = tourist
            booking.tour = tour
            booking.status = 'pending'  # Set status to pending

            # Use Tour model method for price calculation
            booking.total_price = tour.get_price(booking.persons) * booking.days

            # Add hotel cost
            if booking.hotel:
                booking.total_price += booking.hotel.price_per_day * booking.days

            booking.save()
            form.save_m2m()  # save addons

            # Add addons price
            addon_total = sum(addon.price for addon in booking.addons.all())
            booking.total_price += addon_total
            booking.save()

            # Redirect to payment page instead of confirming booking
            return redirect('payment_gateway', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'tour/book_tour.html', {'tour': tour, 'form': form})


def generate_transaction_id():
    """Generate unique transaction ID"""
    return 'TXN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


# ---------- Payment Gateway ----------
@login_required
def payment_gateway(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user owns this booking
    if booking.tourist.user != request.user:
        messages.error(request, 'Unauthorized access')
        return redirect('my_bookings')
    
    # Get or create payment
    payment, created = Payment.objects.get_or_create(
        booking=booking,
        defaults={
            'amount': booking.computed_total_price,
            'payment_method': 'esewa',
            'status': 'pending'
        }
    )
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'esewa')
        payment.payment_method = payment_method
        payment.save()
        
        # Redirect to payment demo page
        return redirect('payment_process', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'payment': payment,
        'total_price': booking.computed_total_price,
        'payment_methods': ['esewa', 'khalti', 'bank']
    }
    return render(request, 'tour/payment_gateway.html', context)


# ---------- Payment Process (Demo) ----------
@login_required
def payment_process(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if user owns this booking
    if booking.tourist.user != request.user:
        messages.error(request, 'Unauthorized access')
        return redirect('my_bookings')
    
    payment = get_object_or_404(Payment, booking=booking)
    
    if request.method == 'POST':
        payment_status = request.POST.get('payment_status')  # 'success' or 'failed'
        
        # Get verification credentials
        verify_phone = request.POST.get('verify_phone', '').strip()
        verify_password = request.POST.get('verify_password', '').strip()
        
        # Demo credentials validation
        verification_failed = False
        error_message = ''
        
        # Check demo credentials based on payment method
        if payment.payment_method == 'esewa':
            if verify_phone != '9800000000' or verify_password != '1234':
                verification_failed = True
                error_message = 'Incorrect eSewa credentials. Use Phone: 9800000000, PIN: 1234'
        elif payment.payment_method == 'khalti':
            if verify_phone != '9811111111' or verify_password != '1234':
                verification_failed = True
                error_message = 'Incorrect Khalti credentials. Use Phone: 9811111111, PIN: 1234'
        elif payment.payment_method == 'bank':
            # For bank, any reference ID is accepted
            if not verify_phone:
                verification_failed = True
                error_message = 'Transaction Reference ID is required'
        
        if verification_failed:
            messages.error(request, error_message)
            return redirect('payment_process', booking_id=booking_id)
        
        if payment_status == 'success':
            # Mark payment as completed
            payment.status = 'completed'
            payment.transaction_id = generate_transaction_id()
            payment.save()
            
            # Confirm booking
            booking.status = 'confirmed'
            booking.save()
            
            messages.success(request, f'Payment successful! Your booking for {booking.tour.title} is confirmed.')
            return redirect('my_bookings')
        else:
            # Payment failed
            payment.status = 'failed'
            payment.save()
            
            messages.error(request, 'Payment failed. Please try again.')
            return redirect('payment_gateway', booking_id=booking_id)
    
    context = {
        'booking': booking,
        'payment': payment,
        'total_price': booking.computed_total_price,
    }
    return render(request, 'tour/payment_process.html', context)


# ---------- Complete Profile ----------
@login_required
def complete_profile(request):
    tourist, _ = Tourist.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = TouristDetailForm(request.POST, instance=tourist)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TouristDetailForm(instance=tourist)
    return render(request, 'tour/complete_profile.html', {'form': form})


# ---------- Post-login redirect ----------
@login_required
def post_login(request):
    tourist, _ = Tourist.objects.get_or_create(user=request.user)
    if not tourist.phone:
        return redirect('complete_profile')
    return redirect('dashboard')


# ---------- My Bookings ----------
@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(tourist__user=request.user)
        .select_related('tour', 'hotel')
        .order_by('-booking_date')
    )
    return render(request, 'tour/my_bookings.html', {'bookings': bookings})


# ---------- Home Page (Public) ----------
def home_view(request):
    """Landing page - public access"""
    featured_tours = (
        Tour.objects.filter(is_active=True)
        .prefetch_related('images')
        .order_by('-created_at')[:3]
    )
    featured_hotels = Hotel.objects.all().order_by('name')[:4]
    return render(
        request,
        'tour/home.html',
        {
            'featured_tours': featured_tours,
            'featured_hotels': featured_hotels,
        },
    )


# ---------- Public Tours (Browsable without login) ----------
def public_tours(request):
    """Browse tours without login - shows login prompt for booking"""
    tours = Tour.objects.filter(is_active=True).prefetch_related('images')
    return render(request, 'tour/public_tours.html', {'tours': tours})


# ---------- About Page (Public) ----------
def about_view(request):
    """About page - public access"""
    return render(request, 'tour/about.html')


# ---------- Contact Page (Public) ----------
def contact_view(request):
    """Contact page - public access"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # TODO: Send email to admin
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'tour/contact.html')


# ---------- Hotels Page (Public) ----------
def hotels_view(request):
    """List all hotels - public access"""
    hotels = Hotel.objects.all().order_by('name')
    return render(request, 'tour/hotels.html', {'hotels': hotels})
