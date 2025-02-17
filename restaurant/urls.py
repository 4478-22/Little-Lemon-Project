from django.urls import path
from . import views
from .views import UserRegistrationView, AuthTokenView
from rest_framework.authtoken.views import obtain_auth_token
from .views_api import login_view

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings/', views.bookings, name='bookings'),
    path('api/register/', UserRegistrationView.as_view(), name='user-register'),
    path('api/login/', AuthTokenView.as_view(), name='user-login'),
    path('api/auth/token/login/', obtain_auth_token, name='api-token-auth'),
    path('api/auth/token/logout/', AuthTokenView.as_view(), name='api-token-logout'),
    path('api/custom-login/', login_view, name='custom-login'),
]