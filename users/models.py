from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save

# Create your models here.

"""
this lists is used for choices, 
every list has a name and a value to be used in the database and rendered in templates

"""

GENDER = [
    ("Male", "Male"),
    ("Female", "Female"),
]

NUMBER_OF_EMPLOYEES = [
    ("1-10", "1-10"),
    ("11-50", "11-50"),
    ("51-100", "51-100"),
    ("100-1000", "100-1000"),
    ("1000+", "1000+"),
]

INDUSTRY = [
    ("IT", "IT"),
    ("Backend", "Backend"),
    ("Frontend", "Frontend"),
    ("Full-stack", "Full-stack"),
    ("Data-science", "Data-science"),
    ("Data-engineering", "Data-engineering"),
    ("Devops", "Devops"),
    ("Mobile", "Mobile"),
    ("UI/UX", "UI/UX"),
    ("Marketing", "Marketing"),
    ("SEO", "SEO"),
    ("SEM", "SEM"),
    ("PPC", "PPC"),
    ("Finance", "Finance"),
    ("Accounting", "Accounting"),
    ("Audit", "Audit"),
    ("HR", "HR"),
    ("Recruiting", "Recruiting"),
    ("Hiring", "Hiring"),
    ("Recruitment", "Recruitment"),
    ("Sales", "Sales"),
    ("Digital Marketing", "Digital Marketing"),
    ("Other", "Other"),
]

USER_TYPE = [
    ("Employee", "Employee"),
    ("Company", "Company"),
]

SENIORITY_LEVEL = [
    ("Junior", "Junior"),
    ("Mid Level", "Mid Level"),
    ("Senior Level", "Senior Level"),
    ]



class EmployeeProfile(models.Model):
    
    """ 
    this model is used to create a profile for an employee, it is connected:
    - to the user model.
    - to the employee profile model.
    and contains:
    - some information about the employee
    - function to get the username of the user
    - class Meta to set the verbose name and plural names
    
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    Job_title = models.CharField(max_length=200)
    experience_level = models.CharField(max_length=200, choices=SENIORITY_LEVEL)
    gender = models.CharField(max_length=200, choices=GENDER)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def get_username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


class CompanyProfile(models.Model):
    
    """ 
    this model is used to create a profile for an company, it is connected:
    - to the user model.
    - to the company profile model.
    and contains:
    - some information about the company
    - function to get the username of the user
    - class Meta to set the verbose name and plural names
    
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    logo = models.ImageField(default="default2.jpg", upload_to="company_pics")
    industry = models.CharField(max_length=200, choices=INDUSTRY)
    location = models.CharField(max_length=200)
    number_of_employees = models.CharField(max_length=200, choices=NUMBER_OF_EMPLOYEES)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    is_active = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Companies Profile"

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def get_username(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    
    """ 
    this function is a signal to create a profile for a new user as a employee.
    
    """
    
    if created:
        EmployeeProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def company_user_profile(sender, instance, **kwargs):
    
    """ 
    this function is a signal to create a profile for a new user as a company.
    
    """
    if instance.is_active:
        CompanyProfile.objects.create(user=instance)
