from django.contrib import admin
from django.urls import path, include                 
from rest_framework import routers                    
# from todo import views
from django.conf.urls.static import static                            
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views as veews

# router = routers.DefaultRouter()                      
# router.register(r'todos', views.TodoView, 'todo')     

# Yes, this issue is due to the JWT. You can checkout the discussion for it https://github.com/GetBlimp/django-rest-framework-jwt/issues/45 To fix this you will have to create a custom middleware which will set the request.user. Here is one I am using in my code:

from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from . import views


class JWTAuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda:self.__class__.get_jwt_user(request))
        return self.get_response(request)

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        jwt_authentication = JSONWebTokenAuthentication()
        if jwt_authentication.get_jwt_value(request):
            user, jwt = jwt_authentication.authenticate(request)
        return user

urlpatterns = [
    path('', include("pages.urls")),
    path('admin/', admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/changedetection/", include("changedetection.urls")),
    path("api/earthenticate/", include("changedetection_mobile.urls")),
    path('api/rrm/', include("rrm.urls")),
    path("api-token-auth/", veews.obtain_auth_token),
    path("token-auth/", obtain_jwt_token),
    path("auth/", include('rest_framework_social_oauth2.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)