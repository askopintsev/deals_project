from django.urls import path

from . import views


urlpatterns = [
    path("upload", views.UploadFileView.as_view()),
    path("results", views.ResultsView.as_view()),
    ]
