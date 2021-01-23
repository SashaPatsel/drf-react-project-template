from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("analysis", views.Analysis.as_view()),
    path("aoi", views.AOI.as_view())
]