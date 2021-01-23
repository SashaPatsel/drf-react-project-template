from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path("activate", views.Activate.as_view()),
    path("feedback", views.FeedbackView.as_view()),
    path("notifications", views.Notifications.as_view()),
    path("pass_reset", views.ResetPassword.as_view()),
    path("register", views.Register.as_view()),
    path("request_pass_reset", views.RequestReset.as_view()),
    path("useraccount", views.UserAccount.as_view()),
    path("users", views.Users.as_view())
]