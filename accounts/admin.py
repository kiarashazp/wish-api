from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Information', {'fields': ('email', 'username', 'password')}),
        ('Permission', {'fields': ('is_admin', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'confirm_password')}),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
