from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import random
import string
from django.utils import timezone
from .models import Tour, Booking, Payment, Tourist
from .serializers import TourSerializer, BookingSerializer, PaymentSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def tours_list(request):
    tours = Tour.objects.filter(is_active=True).prefetch_related('places', 'images')
    serializer = TourSerializer(tours, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    """Create a new booking"""
    try:
        tourist = Tourist.objects.get(user=request.user)
    except Tourist.DoesNotExist:
        return Response({'error': 'Tourist profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if user already has an active booking (pending or confirmed)
    existing_booking = Booking.objects.filter(
        tourist=tourist,
        status__in=['pending', 'confirmed']
    ).first()
    
    if existing_booking:
        return Response({
            'error': 'You already have an active booking. Please complete or cancel it before making a new booking.',
            'existing_booking_id': existing_booking.id,
            'existing_tour': existing_booking.tour.title
        }, status=status.HTTP_400_BAD_REQUEST)
    
    tour_id = request.data.get('tour')
    days = request.data.get('days', 1)
    persons = request.data.get('persons', 1)
    hotel_id = request.data.get('hotel')
    addon_ids = request.data.get('addons', [])
    
    try:
        tour = Tour.objects.get(id=tour_id)
    except Tour.DoesNotExist:
        return Response({'error': 'Tour not found'}, status=status.HTTP_404_NOT_FOUND)
    
    booking = Booking.objects.create(
        tourist=tourist,
        tour=tour,
        days=days,
        persons=persons,
        hotel_id=hotel_id if hotel_id else None,
        status='pending'
    )
    
    if addon_ids:
        booking.addons.set(addon_ids)
    
    booking.total_price = booking.computed_total_price
    booking.save()
    
    # Create payment record
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.computed_total_price,
        payment_method=request.data.get('payment_method', 'esewa'),
        status='pending'
    )
    
    serializer = BookingSerializer(booking, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_bookings(request):
    """Get all bookings for current user"""
    try:
        tourist = Tourist.objects.get(user=request.user)
    except Tourist.DoesNotExist:
        return Response({'error': 'Tourist profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    bookings = Booking.objects.filter(tourist=tourist).prefetch_related('payment')
    serializer = BookingSerializer(bookings, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def booking_detail(request, booking_id):
    """Get booking details"""
    try:
        tourist = Tourist.objects.get(user=request.user)
    except Tourist.DoesNotExist:
        return Response({'error': 'Tourist profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        booking = Booking.objects.get(id=booking_id, tourist=tourist)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookingSerializer(booking, context={'request': request})
    return Response(serializer.data)


def generate_transaction_id():
    """Generate unique transaction ID"""
    return 'TXN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request, booking_id):
    """Initiate payment for a booking"""
    try:
        tourist = Tourist.objects.get(user=request.user)
    except Tourist.DoesNotExist:
        return Response({'error': 'Tourist profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        booking = Booking.objects.get(id=booking_id, tourist=tourist)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if booking.status != 'pending':
        return Response({'error': 'Booking is not pending'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        payment = Payment.objects.get(booking=booking)
    except Payment.DoesNotExist:
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.computed_total_price,
            payment_method=request.data.get('payment_method', 'esewa'),
            status='pending'
        )
    
    payment_method = request.data.get('payment_method', 'esewa')
    payment.payment_method = payment_method
    payment.save()
    
    # Generate payment page data
    payment_data = {
        'booking_id': booking.id,
        'amount': booking.computed_total_price,
        'payment_method': payment_method,
        'transaction_id': generate_transaction_id(),
        'payment_url': f'/payment/gateway/{payment_method}/?booking_id={booking.id}'
    }
    
    return Response(payment_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def process_payment(request, booking_id):
    """Process demo payment (Success/Failure)"""
    try:
        tourist = Tourist.objects.get(user=request.user)
    except Tourist.DoesNotExist:
        return Response({'error': 'Tourist profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        booking = Booking.objects.get(id=booking_id, tourist=tourist)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    payment_status = request.data.get('status', 'completed')  # completed or failed
    
    try:
        payment = Payment.objects.get(booking=booking)
    except Payment.DoesNotExist:
        return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if payment_status == 'completed':
        payment.status = 'completed'
        payment.transaction_id = generate_transaction_id()
        payment.save()
        
        booking.status = 'confirmed'
        booking.save()
        
        return Response({
            'status': 'success',
            'message': 'Payment completed successfully',
            'booking': BookingSerializer(booking, context={'request': request}).data
        }, status=status.HTTP_200_OK)
    else:
        payment.status = 'failed'
        payment.save()
        
        return Response({
            'status': 'failed',
            'message': 'Payment failed. Please try again.',
            'booking': BookingSerializer(booking, context={'request': request}).data
        }, status=status.HTTP_400_BAD_REQUEST)
