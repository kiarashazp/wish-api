from django.contrib import admin
from .models import Wish


class WishAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'fulfilled')


admin.site.register(Wish, WishAdmin)
