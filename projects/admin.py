from django.contrib import admin

from .models import Project, ProjectHardware

class ProjectHardwareInline(admin.TabularInline):
    model = ProjectHardware

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectHardwareInline]

