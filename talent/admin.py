from django.contrib import admin

from talent.models import Talent


# Register your models here.

class TalentAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'reference_id']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Talent Info', {'fields': ['first_name', 'last_name', 'email', 'phone', 'reference_id']}),
        ('Important dates', {'fields': ['created_at', 'updated_at']}),
    ]
    save_as = True


admin.site.register(Talent, TalentAdmin)
