from django.contrib import admin
from .models import Project, Contact


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'is_active']  # replace 'name' with 'title'

admin.site.register(Project, ProjectAdmin)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('email', 'subject')
