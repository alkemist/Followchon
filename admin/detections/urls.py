from django.urls import path

from . import views

app_name = "detections"
urlpatterns = [
    path("", views.index, name="index"),
    path("detections/<int:pk>", views.DetailView.as_view(), name="detail"),
]
