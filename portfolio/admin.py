from django.contrib import admin
from .models import Profile, Category, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Project, ProjectAdmin)
