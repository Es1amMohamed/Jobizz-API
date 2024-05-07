from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.


@api_view(["POST"])
def signup(request):
    """
    this function is used to create a new user
    """
    data = request.data
    user_serializer = SignUpSerializer(data=data)

    if user_serializer.is_valid():
        email = data.get("email")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=email,
                password=make_password(data["password"]),
            )
            user.save()
            user_type = data.get("user_type")
            if user_type == "Company":
                company_profile_serializer = CompanyProfileSerializer(data=data)
                if company_profile_serializer.is_valid():
                    company_profile_serializer.save(user=user)
                    return Response(
                        {"message": "User and company profile created successfully, we will provide you an email shortly"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    user.delete()
                    return Response(
                        company_profile_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            elif user_type == "Employee":
                profile_serializer = ProfileSerializer(data=data)
                if profile_serializer.is_valid():
                    profile_serializer.save(user=user)
                    return Response(
                        {"message": "User and profile created successfully"},
                        status=status.HTTP_201_CREATED,
                    )
                else:
                    user.delete()
                    return Response(
                        profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                user.delete()
                return Response(
                    {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = UserSerializer(request.user)

    return Response(user.data)


@api_view(["POST"])
def login(request):
    data = request.data

    if User.objects.filter(username=data["username"]).exists():
        user = User.objects.get(username=data["username"])
        if user.check_password(data["password"]):
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = User.objects.get(id=request.user.id)

    if user.check_password(request.data["password"]):
        user.password = make_password(request.data["new_password"])
        user.save()
        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Invalid old password"}, status=status.HTTP_400_BAD_REQUEST
        )
