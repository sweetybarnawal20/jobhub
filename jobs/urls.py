from django.urls import path
from .views import create_job, manage_jobs, edit_job, delete_job, job_list

urlpatterns = [
    path("create/", create_job, name="create_job"),
    path("manage/", manage_jobs, name="manage_jobs"),
    path("edit/<int:job_id>/", edit_job, name="edit_job"),
    path("delete/<int:job_id>/", delete_job, name="delete_job"),
    path("list/", job_list, name="job_list"),
]