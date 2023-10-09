
"""
Serializers for birthday APIs
"""

from rest_framework import serializers

from core.models import Birthday


class BirthdaySerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model= Birthday
        fields = ['id', 'name', 'email', 'date_of_birth']
        read_only_fields = ['id']
