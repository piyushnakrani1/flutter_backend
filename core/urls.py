from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    path('normalize', NormalizeView.as_view()),
]
