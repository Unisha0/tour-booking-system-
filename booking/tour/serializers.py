from rest_framework import serializers
from .models import Tour, TourPlace, TourImage, Hotel, Addon, Booking, Payment, Tourist

# Serializer for TourPlace
class TourPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPlace
        fields = ['title', 'description']

# Serializer for TourImage
class TourImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TourImage
        fields = ['image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None

# Serializer for Hotel
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['name', 'price_per_day', 'hotel_image']

# Serializer for Addon
class AddonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addon
        fields = ['name', 'price']

# Serializer for Tour
class TourSerializer(serializers.ModelSerializer):
    places = TourPlaceSerializer(many=True, read_only=True)
    images = TourImageSerializer(many=True, read_only=True)

    class Meta:
        model = Tour
        fields = [
            'id', 'title', 'destination', 'duration_days',
            'base_price', 'description', 'places', 'images'
        ]


# Serializer for Payment
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'booking', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'created_at', 'transaction_id']


# Serializer for Booking
class BookingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = ['id', 'tour', 'hotel', 'addons', 'days', 'persons', 'total_price', 'status', 'booking_date', 'payment']
        read_only_fields = ['id', 'booking_date', 'status']
    
    def get_total_price(self, obj):
        return obj.computed_total_price
