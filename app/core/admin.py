"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
           _('Permissions'),
           {
               'fields': (
                   'is_active',
                   'is_staff',
                   'is_superuser',
               )
           }
    ),
    )


admin.site.register(User, UserAdmin)