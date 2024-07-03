from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.views import APIView



    



class UserSignUpView(APIView):
    
    """
    This view handles user sign up for both Employee and Company user types.

    Depending on the `user_type` provided in the request data, it delegates the 
    sign-up process to either `get_employee_data` or `get_company_data`.

    Methods
    -------
    post(request, *args, **kwargs)
        Handles the POST request for user sign-up.
    
    get_employee_data(request)
        Processes the sign-up for an Employee user type.
    
    get_company_data(request)
        Processes the sign-up for a Company user type.
    """

    def post(self, request, *args, **kwargs):
        
        """
        Handles the POST request for user sign-up.

        Parameters:
        ----------
        request : Request
            The HTTP request object containing user data.

        Returns:
        -------
        Response
            A Response object with the appropriate status and data.
        """
        
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
        
        """
        Processes the sign-up for an Employee user type.

        Parameters:
        ----------
        request : Request
            The HTTP request object containing employee data.

        Returns:
        -------
        Response
            A Response object with the status and data for the employee sign-up.
        """
        
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
        
        """
        Processes the sign-up for a Company user type.

        Parameters:
        ----------
        request : Request
            The HTTP request object containing company data.

        Returns:
        -------
        Response
            A Response object with the status and data for the company sign-up.
        """
        
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
    
    """
    Handle user login.

    This function processes a POST request to authenticate a user based on the 
    provided username and password. If the authentication is successful, the user
    is logged in and a success message is returned. Otherwise, an error message
    indicating invalid credentials is returned.

    Parameters:
    -----------
    request : Request
        The HTTP request object containing the user credentials.

    Returns:
    --------
    Response
        A Response object with a success message if login is successful,
        or an error message if authentication fails.
    """
    
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid username or password"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    
    """
    Handle changing user password.

    This function processes a POST request to change the password of the authenticated user.
    The user must be authenticated to access this endpoint. The old password is verified
    before changing it to the new password.

    Parameters:
    -----------
    request : Request
        The HTTP request object containing the user's old and new passwords.

    Returns:
    --------
    Response
        A Response object with a success message if password change is successful,
        or an error message if the old password is invalid.
    """
    
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_employee_profile(request):
    user = EmployeeProfileSerializer(request.user)

    return Response(user.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_company_profile(request):
    user = CompanyProfileSerializer(request.user)

    return Response(user.data)

