from django.urls import path
from .views import profile_view, upgrade_me

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('upgrade/', upgrade_me, name='upgrade'),
]