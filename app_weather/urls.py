# urls.py in store

from django.urls import path
from .views import weather



urlpatterns = [
    path('', weather),

]