from django.contrib import admin
from django.contrib.auth.models import User

from controlpanel.models import AppUserSetting, AppUser


# Register your models here.

class AppUserSettingInline(admin.StackedInline):
    model = AppUserSetting
    extra = 1


class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('User Info', {'fields': ['username', 'email', 'password']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser']}),
        ('Important dates', {'fields': ['last_login', 'date_joined', 'created_at', 'updated_at']}),
    ]

    inlines = [AppUserSettingInline]

admin.site.unregister(User)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(AppUserSetting)