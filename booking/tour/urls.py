from django.urls import path
from . import views, api_views, auth_views

urlpatterns = [
    # Landing & Public Pages
    path('', views.home_view, name='home'),
    path('tours/', views.public_tours, name='public_tours'),
    path('hotels/', views.hotels_view, name='hotels'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # Existing URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('post-login/', views.post_login, name='post_login'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    
    # Payment URLs
    path('payment/<int:booking_id>/', views.payment_gateway, name='payment_gateway'),
    path('payment/<int:booking_id>/process/', views.payment_process, name='payment_process'),

    # Authentication API URLs
    path('api/login/', auth_views.api_login, name='api_login'),
    path('api/logout/', auth_views.api_logout, name='api_logout'),
    
    # API URLs
    path('api/tours/', api_views.tours_list, name='api_tours'),
    
    # Booking API URLs
    path('api/bookings/create/', api_views.create_booking, name='api_create_booking'),
    path('api/bookings/', api_views.user_bookings, name='api_user_bookings'),
    path('api/bookings/<int:booking_id>/', api_views.booking_detail, name='api_booking_detail'),
    
    # Payment API URLs
    path('api/bookings/<int:booking_id>/initiate-payment/', api_views.initiate_payment, name='api_initiate_payment'),
    path('api/bookings/<int:booking_id>/process-payment/', api_views.process_payment, name='api_process_payment'),
]
