"""
Views for the birthday APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Birthday
from . import serializers

class BirthdayViewSet(viewsets.ModelViewSet):
    """View fot manage birthday APIs"""

    serializer_class = serializers.BirthdaySerializer
    queryset = Birthday.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve birthdays for authenticated user."""

        return self.queryset.filter(user=self.request.user).order_by('-id')


