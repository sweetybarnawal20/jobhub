from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect_user(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect_user(user)

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password."}
        )

    return render(request, "accounts/login.html")
def register_view(request):
    if request.user.is_authenticated:
        return redirect_user(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")

        if password != confirm_password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "Username already exists."}
            )

        if role not in ["CANDIDATE", "EMPLOYER"]:
            return render(
                request,
                "accounts/register.html",
                {"error": "Please select a valid role."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        login(request, user)

        return redirect_user(user)

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


def redirect_user(user):
    if user.role == "CANDIDATE":
        return redirect("candidate_dashboard")

    if user.role == "EMPLOYER":
        return redirect("employer_dashboard")

    return redirect("login")

@login_required
def candidate_dashboard(request):
    if request.user.role != "CANDIDATE":
        return redirect_user(request.user)

    return render(
        request,
        "accounts/candidate_dashboard.html"
    )


@login_required
def employer_dashboard(request):
    if request.user.role != "EMPLOYER":
        return redirect_user(request.user)

    return render(
        request,
        "accounts/employer_dashboard.html"
    )