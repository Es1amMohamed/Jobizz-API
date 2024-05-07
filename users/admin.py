from django.contrib import admin
from .models import *

# Register your models here.

class EmployeeAdmin(admin.ModelAdmin):
    
    '''
    Admin View for Employee Profile in django admin panel
    
    '''
    list_display = ('get_username','Job_title', 'experience_level')
    list_filter = ('Job_title', 'experience_level')
    search_fields = ["Job_title"]


class CompanyProfileAdmin(admin.ModelAdmin):
    
    """
    Admin View for Company Profile in django admin panel
    
    """
    
    list_display =  ['get_username',"industry"]
    list_filter = ( "location", "number_of_employees")
    search_fields = ('get_username', "industry", "location", "number_of_employees")

admin.site.register(EmployeeProfile, EmployeeAdmin)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
