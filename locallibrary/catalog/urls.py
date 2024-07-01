from django.urls import path
from . import views  # Import your catalog app views

urlpatterns = [
    path("", views.home, name="home"),
]

