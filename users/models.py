from django.db import models
from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from job.models import *
from django.core.validators import MinValueValidator, MaxValueValidator

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

    username = models.TextField(max_length=50, unique=True)
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=100)
    password_confirmation = models.CharField(
        validators=[MinLengthValidator(8)], max_length=100
    )
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    job_title = models.CharField(max_length=200)
    experience_level = models.CharField(max_length=200, choices=SENIORITY_LEVEL)
    gender = models.CharField(max_length=200, choices=GENDER)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.username} Profile"

    def clean(self):
        """
        this function will check if the password and password_confirmation are the same
        and if the age is not empty

        """

        if self.password != self.password_confirmation:
            raise ValidationError("passwords do not match")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_application_count(self):
        """
        This method returns the total number of job applications made by this employee.

        It uses the related name 'employee_applications' defined in the Application model's ForeignKey relationship
        to count how many Application instances are linked to this particular Employee instance.

        Returns:
            int: The count of job applications made by the employee.
        """

        return self.employee_applications.count()


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

    username = models.TextField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    company_name = models.TextField(max_length=150, default="Company")
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=100)
    password_confirmation = models.CharField(
        validators=[MinLengthValidator(8)], max_length=100
    )
    logo = models.ImageField(default="default2.jpg", upload_to="company_pics")
    industry = models.CharField(max_length=200, choices=INDUSTRY)
    location = models.CharField(max_length=200)
    number_of_employees = models.CharField(max_length=200, choices=NUMBER_OF_EMPLOYEES)
    website = models.URLField(max_length=255, blank=True)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    is_active = models.BooleanField(default=False)
    crated_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Companies Profile"

    def __str__(self):
        return f"{self.username} Profile"

    def clean(self):
        """
        this function will check if the password and password_confirmation are the same
        and if the age is not empty

        """

        if self.password != self.password_confirmation:
            raise ValidationError("passwords do not match")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def get_job_count(self):
        """
        This method returns the total number of jobs associated with the company.

        It uses the related name 'jobs' defined in the Job model's ForeignKey relationship
        to count how many Job instances are linked to this particular Company instance.

        Returns:
            int: The count of jobs associated with the company.
        """

        return self.jobs.count()


@receiver(post_save, sender=EmployeeProfile)
def create_user_profile(sender, instance, created, **kwargs):
    """
    this function is a signal to create a profile for a new user as a employee.

    """

    if created:
        user = User.objects.create_user(
            username=instance.username,
            email=instance.email,
            password=instance.password,
        )

    group_name = "Employees Group"

    try:
        group = Group.objects.get(name=group_name)
        group.permissions.clear()
    except Group.DoesNotExist:
        group = Group(name=group_name)
        group.save()

    user.groups.add(group)


@receiver(post_save, sender=CompanyProfile)
def company_user_profile(sender, instance, **kwargs):
    """
    this function is a signal to create a profile for a new user as a company.

    """
    if instance.is_active:
        user = User.objects.create_user(
            username=instance.username,
            email=instance.email,
            password=instance.password,
        )

        group_name = "Companies Group"

        try:
            group = Group.objects.get(name=group_name)
            group.permissions.clear()
        except Group.DoesNotExist:
            group = Group(name=group_name)
            group.save()

        user.groups.add(group)


@receiver(post_delete, sender=User)
def delete_user_with_profile(sender, instance, **kwargs):
    if instance.email:
        try:
            profile = EmployeeProfile.objects.get(email=instance.email)
            profile.delete()
        except EmployeeProfile.DoesNotExist:
            pass
        try:
            profile = CompanyProfile.objects.get(email=instance.email)
            profile.delete()
        except CompanyProfile.DoesNotExist:
            pass
