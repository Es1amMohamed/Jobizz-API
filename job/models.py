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
    """
    Job Model to represent a job listing.

        This model represents a job listing with various details such as title, type,
        level, salary, location, description, requirements, and timestamps for creation
        and updates.

    """

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

    company_name = models.ForeignKey(
        User, related_name="jobs", on_delete=models.CASCADE
    )
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
        """
        Save method override.

        This method overrides the save method to generate a slug for the job title
        if it doesn't already exist.

        Returns:
        --------
        None
        """

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_application_count(self):
        """
        This method returns the total number of applicants for this job.

        It uses the related name 'applicants' defined in the Applicant model's ForeignKey relationship
        to count how many Applicant instances are linked to this particular Job instance.

        Returns:
            int: The count of applicants for the job.
        """

        return self.applications.count()


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employee_applications"
    )
    ##cv = models.FileField(upload_to="cv") ' i comment this field because i don't want to upload cv. '
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Apply For Job"
        verbose_name_plural = "Apply For Jobs"

    def __str__(self):
        return f"{self.job.title} - {self.employee.username}"
