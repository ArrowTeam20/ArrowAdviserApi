from myapi.views import *
from django.urls import path
urlpatterns = [
    path('advise',getResponse),
]