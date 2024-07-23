from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class EmployeeSignUpSerializer(serializers.ModelSerializer):
    """
    this class is used to create a new user when signing up

    """

    class Meta:
        model = EmployeeProfile
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirmation",
            "job_title",
            "experience_level",
            "gender",
            "user_type",
        )


class CompanySignUpSerializer(serializers.ModelSerializer):
    """
    this class is used to create a new user when signing up

    """

    class Meta:
        model = CompanyProfile
        fields = (
            "username",
            "company_name",
            "email",
            "password",
            "password_confirmation",
            "industry",
            "location",
            "number_of_employees",
            "website",
            "user_type",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    this class is used to serialize and deserialize the user model

    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """
    this class is used to serialize and deserialize the profile model

    """

    class Meta:
        model = EmployeeProfile
        exclude = [
            "slug",
            "username",
            "created_at",
            "user_type",
            "gender",
            "password",
            "password_confirmation",
        ]


class CompanyProfileSerializer(serializers.ModelSerializer):
    """
    this class is used to serialize and deserialize the company profile model

    """

    class Meta:
        model = CompanyProfile
        exclude = [
            "is_active",
            "slug",
            "created_at",
            "user_type",
            "password",
            "password_confirmation",
            "username",
        ]
