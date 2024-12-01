from rest_framework import serializers
from .models import *


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ["company_name", "created_at", "updated_at", "slug"]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        exclude = ["created_at", "cv"]
