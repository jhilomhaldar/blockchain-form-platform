from django.urls import path
from .views import (
    FormTemplateListAPIView,
    FormTemplateDetailAPIView,
    FormSubmissionCreateAPIView,
    FormSubmissionDetailAPIView,
    FormSubmissionVerifyAPIView,
)

urlpatterns = [
    path("forms/", FormTemplateListAPIView.as_view(), name="api_forms"),
    path("forms/<slug:slug>/", FormTemplateDetailAPIView.as_view(), name="api_form_detail"),

    path("submissions/", FormSubmissionCreateAPIView.as_view(), name="api_submission_create"),
    path("submissions/<str:submission_ref>/", FormSubmissionDetailAPIView.as_view(), name="api_submission_detail"),
    path("submissions/<str:submission_ref>/verify/", FormSubmissionVerifyAPIView.as_view(), name="api_submission_verify"),
]