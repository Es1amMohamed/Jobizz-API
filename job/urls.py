from django.urls import path
from . import views


app_name = 'job'

urlpatterns = [
    path('add_job', views.add_job, name='add_job'),
    path('delete_job/<int:id>', views.delete_job, name='delete_job'),
]

