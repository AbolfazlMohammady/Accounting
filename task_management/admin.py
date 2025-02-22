from django.contrib import admin

from .models import Task,Project


admin.site.register(Task)

@admin.register(Project)
class ProgectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'created_at']
    search_fields = ['title']
