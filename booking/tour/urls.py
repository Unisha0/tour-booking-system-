from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('book/<int:tour_id>/', views.book_tour, name='book_tour'),
]