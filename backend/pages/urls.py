from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/activate", views.index, name="activate"),
    path("accounts/password_reset_req", views.index, name="password_reset_req"),
    path("accounts/password_reset", views.index, name="password_req"),
    path("habitatpatrol", views.index, name="cd"),
    path("earthenticate", views.index, name="cd_mobile"),
    # RRM
    path("rrm/dash", views.index, name="rrmdash"),
    path("rrm/map", views.index, name="rrm")
]
