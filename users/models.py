from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import post_save

# Create your models here.

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
    (
        "IT",
        (
            "IT",
            "Backend",
            "Frontend",
            "Full-stack",
            "Data-science",
            "Data-engineering",
            "Devops",
            "Mobile",
            "UI/UX",
        ),
    ),
    ("Marketing", ("Marketing", "SEO", "SEM", "PPC")),
    ("Finance", ("Finance", "Accounting", "Audit")),
    ("HR", ("HR", "Recruiting", "Hiring", "Recruitment")),
    ("Sales", ("Sales", "Digital Marketing")),
    ("Other", "Other"),
]

USER_TYPE = [
    ("Employee", "Employee"),
    ("Company", "Company"),
]

SENIORITY_LEVEL = (
    ("Junior", "Junior"),
    ("Mid Level", "Mid Level"),
    ("Senior Level", "Senior Level"),
)


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    Job_title = models.CharField(max_length=200)
    experience_level = models.CharField(max_length=200, choices=SENIORITY_LEVEL)
    gender = models.CharField(max_length=200, choices=GENDER)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    logo = models.ImageField(default="default2.jpg", upload_to="company_pics")
    industry = models.CharField(max_length=200, choices=INDUSTRY)
    location = models.CharField(max_length=200)
    number_of_employees = models.CharField(max_length=200, choices=NUMBER_OF_EMPLOYEES)
    user_type = models.CharField(max_length=200, choices=USER_TYPE)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Companies Profile"

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        EmployeeProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_active:
        CompanyProfile.objects.create(user=instance)
