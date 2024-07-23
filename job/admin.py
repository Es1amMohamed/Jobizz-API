from django.contrib import admin
from .models import *

# Register your models here.


class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "job_level")
    list_filter = ("job_level", "job_type")
    search_fields = ("title", "company_name")


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job", "employee")
    list_filter = ("job", "employee")
    search_fields = ("job", "employee")


admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
