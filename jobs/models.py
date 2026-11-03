from django.db import models
from django.conf import settings


class Job(models.Model):

    class JobType(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        INTERNSHIP = "INTERNSHIP", "Internship"
        REMOTE = "REMOTE", "Remote"

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=150)
    salary = models.CharField(max_length=100, blank=True)
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title