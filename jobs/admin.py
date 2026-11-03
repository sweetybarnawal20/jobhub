from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "employer",
        "location",
        "job_type",
        "created_at",
    )

    list_filter = (
        "job_type",
        "created_at",
    )

    search_fields = (
        "title",
        "location",
        "employer__username",
    )