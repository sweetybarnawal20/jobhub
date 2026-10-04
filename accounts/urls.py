from django.urls import path

from .views import (
    candidate_dashboard,
    employer_dashboard,
    login_view,
    logout_view,
)


urlpatterns = [
    path("", login_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path(
        "candidate/",
        candidate_dashboard,
        name="candidate_dashboard"
    ),

    path(
        "employer/",
        employer_dashboard,
        name="employer_dashboard"
    ),
]