from django.db import models

# Create your models here.
Job_type = (
    ("Full Time", "Full Time"),
    ("Part Time", "Part Time"),
    ("Internship", "Internship"),
    ("Contract", "Contract"),
    ("Freelance", "Freelance"),
)

Job_level = (
    ("Junior", "Junior"),
    ("Mid Level", "Mid Level"),
    ("Senior Level", "Senior Level"),
)
# class Job(models.Model):
#     company_name = ''
#     title = models.CharField(max_length=200)
#     job_type = models.CharField(max_length=100,choices=Job_type)
#     job_level = models.CharField(max_length=100, choices=Job_level)
#     salary = models.IntegerField()
#     location = models.CharField(max_length=200)
#     description = models.TextField()
#     requirement = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
