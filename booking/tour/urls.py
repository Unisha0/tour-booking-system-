from django.urls import path
from . import views, api_views, auth_views, admin_views

urlpatterns = [
    # Landing & Public Pages
    path('', views.home_view, name='home'),
    path('tours/', views.public_tours, name='public_tours'),
    path('hotels/', views.hotels_view, name='hotels'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # User Authentication URLs
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
    
    # Admin URLs
    path('admin-panel/login/', admin_views.admin_login_view, name='admin_login'),
    path('admin-panel/signup/', admin_views.admin_signup_view, name='admin_signup'),
    path('admin-panel/logout/', admin_views.admin_logout_view, name='admin_logout'),
    path('admin-panel/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/bookings/', admin_views.admin_bookings_list, name='admin_bookings_list'),
    path('admin-panel/bookings/<int:booking_id>/', admin_views.admin_booking_detail, name='admin_booking_detail'),
    path('admin-panel/bookings/<int:booking_id>/cancel/', admin_views.admin_cancel_booking, name='admin_cancel_booking'),
    path('admin-panel/tourists/', admin_views.admin_tourists_list, name='admin_tourists_list'),
    path('admin-panel/tourists/<int:tourist_id>/', admin_views.admin_tourist_detail, name='admin_tourist_detail'),
    path('admin-panel/tours/', admin_views.admin_tours_list, name='admin_tours_list'),
    path('admin-panel/tours/create/', admin_views.admin_tour_create, name='admin_tour_create'),
    path('admin-panel/tours/<int:tour_id>/', admin_views.admin_tour_detail, name='admin_tour_detail'),
    path('admin-panel/tours/<int:tour_id>/edit/', admin_views.admin_tour_edit, name='admin_tour_edit'),
    path('admin-panel/tours/<int:tour_id>/toggle-status/', admin_views.admin_tour_toggle_status, name='admin_tour_toggle_status'),
    path('admin-panel/tours/image/<int:image_id>/delete/', admin_views.admin_tour_delete_image, name='admin_tour_delete_image'),
    path('admin-panel/reports/', admin_views.admin_reports, name='admin_reports'),
]
