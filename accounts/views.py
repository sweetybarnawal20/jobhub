from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


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