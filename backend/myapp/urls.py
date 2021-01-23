from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path("firstview", views.FirstView.as_view()),
]