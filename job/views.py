from .models import *
from .serializers import *
from .permissions import *
from .filters import JobFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action


class JobViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[IsGroupMember])
    def add_job(self, request):
        """
        Add a new job.

        This function allows a user to add a new job. The user must have the 'IsGroupMember' permission.

        Parameters:
        -----------
        request : Request
            The HTTP request object containing the job data.

        Returns:
        --------
        Response
            A Response object with the newly added job data if successful,
            or an error response if the data is invalid.
        """

        serializer = JobSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            serializer.save(company_name=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def delete_job(self, request, id=None):
        """
        Delete a job.

        This function allows a user to delete a job by its ID if the user is the owner of the job.

        Parameters:
        -----------
        request : Request
            The HTTP request object.
        id : int
            The ID of the job to be deleted.

        Returns:
        --------
        Response
            A Response object with a success status if the job is deleted successfully,
            or an error response if the job is not found or the user is not the owner.
        """

        user = request.user
        try:
            job = Job.objects.get(id=id)
        except Job.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if user == job.company_name:
            job.delete()
            return Response(
                {"message": "Job deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"], permission_classes=[IsEmployee])
    def apply_job(request, pk):
        """
        Apply for a job.

        This function allows an employee to apply for a job by its ID if the employee
        has not already applied for the job.

        Parameters:
        -----------
        request : Request
            The HTTP request object containing the user's data.
        pk : int
            The ID of the job to apply for.

        Returns:
        --------
        Response
            A Response object with the application data if successful,
            or an error response if the job is not found or the user has already applied.
        """

        user = request.user
        try:
            job = Job.objects.get(id=pk)
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if JobApplication.objects.filter(user=user, job=job).exists():
            return Response(
                {"error": "You have already applied for this job"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        application = JobApplication(employee=user, job=job)
        application.save()

        serializer = JobApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class JobFilterViewSet(viewsets.ReadOnlyModelViewSet):
    """
    JobFilterViewSet provides read-only access to Job model with filtering capabilities.

    This ViewSet allows retrieving job listings and filtering them based on various criteria like
    job title, publication date, company name, job type, and job level.
    """

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter

    def all_jobs(self, request):
        """
        Get all jobs.

        This function retrieves all jobs available.

        Parameters:
        -----------
        request : Request
            The HTTP request object.

        Returns:
        --------
        Response
            A Response object with a list of all jobs.
        """

        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
