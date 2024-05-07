from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *


class SignUpSerializer(serializers.ModelSerializer):
    
    """ 
    this class is used to create a new user when signing up
    
    """
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")
        extra_kwargs = {
            "username": {"required": True, "allow_blank": False},
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False, "min_length": 8},
        }


class UserSerializer(serializers.ModelSerializer):
    
    """
    this class is used to serialize and deserialize the user model 
    
    """
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    
    """ 
    this class is used to serialize and deserialize the profile model 
    
    """
    class Meta:
        model = EmployeeProfile
        exclude = ["slug"]


class CompanyProfileSerializer(serializers.ModelSerializer):
    
    """ 
    this class is used to serialize and deserialize the company profile model
     
    """
    class Meta:
        model = CompanyProfile
        exclude = ["is_active", "slug"]
