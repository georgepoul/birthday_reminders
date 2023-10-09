"""
URL mappings for birthday App
"""

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter
from  . import views

router = DefaultRouter()
router.register('birthday', views.BirthdayViewSet)

app_name = 'birthday'

urlpatterns = [
    path('', include(router.urls)),
]
