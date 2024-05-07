from django.contrib import admin
from .models import Job
# Register your models here.


class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "job_level")
    list_filter = ("job_level", "job_type")
    search_fields = ("title", "company_name")


admin.site.register(Job, JobAdmin)