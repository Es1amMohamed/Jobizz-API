from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from rest_framework import viewsets
from .permissions import IsGroupMember
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import action, login_required


@login_required
@action(detail=False, methods=['post'], permission_classes=[ IsGroupMember])
def add_job(request):
    serializer = JobSerializer(data=request.data)
    user = request.user
    if serializer.is_valid():
         serializer.save(company_name=user)
         
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
@action(detail=False, methods=['post'])
def delete_job(request, id):
    user = request.user
    job = Job.objects.get(id=id)
    if user == job.company_name:
        job.delete()
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)

