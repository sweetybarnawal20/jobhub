from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User
from .models import Job
from .forms import JobForm
from django.shortcuts import get_object_or_404


@login_required
def create_job(request):

    if request.user.role != User.Role.EMPLOYER:
        return redirect("candidate_dashboard")

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            return redirect("employer_dashboard")

    else:
        form = JobForm()

    return render(
        request,
        "jobs/create_job.html",
        {"form": form}
    )
    
@login_required
def manage_jobs(request):

    if request.user.role != User.Role.EMPLOYER:
        return redirect("candidate_dashboard")

    jobs = Job.objects.filter(
        employer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "jobs/manage_jobs.html",
        {"jobs": jobs}
    )
    
@login_required
def edit_job(request, job_id):

    if request.user.role != User.Role.EMPLOYER:
        return redirect("candidate_dashboard")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("manage_jobs")

    else:
        form = JobForm(instance=job)

    return render(
        request,
        "jobs/edit_job.html",
        {"form": form, "job": job}
    )
    
@login_required
def delete_job(request, job_id):

    if request.user.role != User.Role.EMPLOYER:
        return redirect("candidate_dashboard")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":
        job.delete()
        return redirect("manage_jobs")

    return render(
        request,
        "jobs/delete_job.html",
        {"job": job}
    )
    
def job_list(request):

    jobs = Job.objects.all().order_by("-created_at")

    search_query = request.GET.get("search", "")
    location_query = request.GET.get("location", "")
    job_type = request.GET.get("job_type", "")

    if search_query:
        jobs = jobs.filter(title__icontains=search_query)

    if location_query:
        jobs = jobs.filter(location__icontains=location_query)

    if job_type:
        jobs = jobs.filter(job_type=job_type)

    context = {
        "jobs": jobs,
        "search_query": search_query,
        "location_query": location_query,
        "selected_job_type": job_type,
        "job_types": Job.JobType.choices,
    }

    return render(
        request,
        "jobs/job_list.html",
        context
    )