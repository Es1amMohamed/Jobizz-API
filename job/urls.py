from django.urls import path
from .views import *
from . import views
from rest_framework.routers import DefaultRouter


app_name = 'job'

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='job')

urlpatterns = [
    path('add_job', JobViewSet.as_view({'post': 'add_job'}), name='add_job'),
    path('delete_job/<int:id>', JobViewSet.as_view({'post': 'delete_job'}), name='delete_job'),
    path('apply_job/<int:pk>', JobViewSet.as_view({'post': 'apply_job'}), name='apply_job'),
    path('all_jobs', JobViewSet.as_view({'get': 'all_jobs'}), name='all_jobs'),
]

