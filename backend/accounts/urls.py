from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('google/', views.google_auth, name='google_auth'),
    path('status/', views.auth_status, name='auth_status'),
    path('logout/', views.logout, name='logout'),
]
