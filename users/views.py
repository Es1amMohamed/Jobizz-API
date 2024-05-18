from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserSignUpView(APIView):

    def post(self, request, *args, **kwargs):
        user_type = request.data.get("user_type")

        if user_type == "Employee":
            return self.get_employee_data(request)
        elif user_type == "Company":
            return self.get_company_data(request)
        else:
            return Response(
                {"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST
            )

    def get_employee_data(self, request):
        employee_serializer = EmployeeSignUpSerializer(data=request.data)
        employee_email = request.data.get("email")
        if not User.objects.filter(email=employee_email).exists():
            if employee_serializer.is_valid():
                employee_serializer.save()
                user = User.objects.get(email=employee_email)
                login(request, user)
                return Response(
                    employee_serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    def get_company_data(self, request):
        company_serializer = CompanySignUpSerializer(data=request.data)
        company_email = request.data.get("email")
        if not User.objects.filter(email=company_email).exists():
            if company_serializer.is_valid():
                company_serializer.save()
                user = User.objects.get(email=company_email)
                login(request, user)
                return Response(
                    {
                        "message": "Profile created successfully, We will approve you soon",
                        "company": company_serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                company_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )


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
            login(request, user)
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
