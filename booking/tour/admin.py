from django.contrib import admin
from .models import (
    Tourist,
    Tour,
    TourPlace,
    TourImage,
    Booking,
    Hotel,
    Addon,
    Payment
)

# ======================================================
# Tourist Admin
# ======================================================
@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'phone', 'dob', 'created_at')
    list_display_links = ('username', 'name')
    list_editable = ('email', 'phone')
    search_fields = ('user__username', 'user__first_name', 'name', 'email', 'phone')
    list_filter = ('dob', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    list_per_page = 25

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
    username.admin_order_field = 'user__username'

    def name(self, obj):
        return obj.name or obj.user.first_name or '-'
    name.short_description = 'Name'

    def email(self, obj):
        return obj.email or obj.user.email or '-'
    email.short_description = 'Email'


# ======================================================
# INLINE MODELS (IMPORTANT PART)
# ======================================================

class TourPlaceInline(admin.TabularInline):
    model = TourPlace
    extra = 1
    fields = ('title', 'description')


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 1
    fields = ('image',)


# ======================================================
# Tour Admin (PACKAGE ADMIN)
# ======================================================
@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'destination',
        'duration_days',
        'base_price',
        'is_active',
        'created_at'
    )
    list_display_links = ('title',)
    search_fields = ('title', 'destination')
    list_filter = ('destination', 'is_active')
    ordering = ('-created_at',)
    list_per_page = 25

    readonly_fields = ('created_at',)

    # 🔥 THIS IS WHAT YOU NEEDED
    inlines = [TourPlaceInline, TourImageInline]


# ======================================================
# Booking Admin
# ======================================================
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'tourist_username',
        'tour_title',
        'days',
        'persons',
        'total_price',
        'booking_date'
    )
    list_display_links = ('tourist_username', 'tour_title')
    search_fields = ('tourist__user__username', 'tour__title', 'tourist__name')
    list_filter = ('booking_date', 'tour__destination')
    ordering = ('-booking_date',)
    list_per_page = 25

    def tourist_username(self, obj):
        return obj.tourist.user.username
    tourist_username.short_description = 'Username'

    def tour_title(self, obj):
        return obj.tour.title
    tour_title.short_description = 'Tour Package'


# ======================================================
# Hotel Admin
# ======================================================
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_day', 'hotel_image')
    search_fields = ('name',)


# ======================================================
# Addon Admin
# ======================================================
@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


# ======================================================
# Payment Admin
# ======================================================
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at')
    list_display_links = ('id', 'booking')
    search_fields = ('booking__id', 'transaction_id', 'booking__tourist__user__username')
    list_filter = ('payment_method', 'status', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25
    readonly_fields = ('created_at', 'updated_at')
