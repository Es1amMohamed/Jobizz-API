from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
Job_type = (
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Internship", "Internship"),
    ("Contract", "Contract"),
    ("Freelance", "Freelance"),
)

SENIORITY_LEVEL = (
    ("Junior", "Junior"),
    ("Mid Level", "Mid Level"),
    ("Senior Level", "Senior Level"),
)


class Job(models.Model):
    company_name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    job_type = models.CharField(max_length=100, choices=Job_type)
    job_level = models.CharField(max_length=100, choices=SENIORITY_LEVEL)
    salary = models.IntegerField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    requirement = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job"
        verbose_name_plural = "Jobs"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
