from django.urls import path

from .views import (
    FormTemplateListAPIView,
    FormTemplateDetailAPIView,
    FormSubmissionCreateAPIView,
    FormSubmissionDetailAPIView,
    FormSubmissionVerifyAPIView,
    SubmissionDashboardListAPIView,
    SubmissionCertificateAPIView,
)

urlpatterns = [
    path("forms/", FormTemplateListAPIView.as_view(), name="form-list"),
    path("forms/<slug:slug>/", FormTemplateDetailAPIView.as_view(), name="form-detail"),

    path("submissions/", FormSubmissionCreateAPIView.as_view(), name="submission-create"),

    # Important: dashboard must come before submissions/<str:submission_ref>/
    path(
        "submissions/dashboard/",
        SubmissionDashboardListAPIView.as_view(),
        name="submission-dashboard",
    ),

    path(
        "certificates/<str:submission_ref>/",
        SubmissionCertificateAPIView.as_view(),
        name="submission-certificate",
    ),

    path(
        "submissions/<str:submission_ref>/verify/",
        FormSubmissionVerifyAPIView.as_view(),
        name="submission-verify",
    ),

    path(
        "submissions/<str:submission_ref>/",
        FormSubmissionDetailAPIView.as_view(),
        name="submission-detail",
    ),
]