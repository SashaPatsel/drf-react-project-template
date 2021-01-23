from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import *
from django.db.models import Q
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .forms import AccountUpdateForm, FileUploadForm
from django.http import JsonResponse, HttpResponse
import json
from .helpers import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework.authtoken.models import Token
from backend.utils.emails import email_notification, send_email


class Activate(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, req, format=None):
        try:
            uidb64 = req.data["uid"]
            token = req.data["token"]
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            stored_token = Token.objects.get(user=user).key
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and token == stored_token:

            user.is_active = True
            user.save()       
            account = Account(first_name=user.first_name, last_name=user.last_name, user=user, photo=get_default_img())
            account.save()

            return Response(UserSerializer(user).data)
        else:
            return Response({"message": "error"})

class Register(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, req, format=None):
        first_name = req.data["first_name"]
        last_name = req.data["last_name"]
        username= req.data["username"]
        email = req.data["email"]
        password = req.data["password"]
        password2 = req.data["password2"]
        # # Password validation
        try:
            invalid = validate_password(password)
        except ValidationError:
            return Response({"message": "invalid password"})
        #check if passwords match
        if password == password2:
            #check username
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "Email already exists"})
            else:
                serializer = UserSerializerWithToken(data=req.data)
                if serializer.is_valid():
                    serializer.save()
                    user = User.objects.get(username=username)
                else: 
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                subject = 'Activate your account'
                token = Token.objects.create(user=user)
                token = token.key
                to_list = [email, settings.EMAIL_HOST_USER]
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                send_email("Confirm your account.", f"<div>Hi {username},</div><div>Thanks for signing up with conservationist.io. To finish your registration, <a href='https://conservationist.io/accounts/activate?uid={uid}&token={token}'>please click here to confirm your registration.</a></div>", to_list)

                return JsonResponse({"message": "success"})
        else: 
            return JsonResponse({"message": "passwords don't match"})



class RequestReset(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, req, format=None):
        email = req.data["email"]
        user = User.objects.get(email=email)
        message = "Please click on the link below to finish reseting your password."
        token = Token.objects.get_or_create(user=user)
        try:
            token = token.key
        except:
            token = token[0].key
        link = "/accounts/password_reset?token=" + token
        link += "&username=" + user.username
        email_notification(user, message, link)
        return Response({
            "message": "success"
        })

class ResetPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, req, format=None):
        new_password = req.data["password"]
        username = req.data["username"]
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return Response({})

    def get(self, req, format=None):
        token = req.query_params["token"]
        key = Token.objects.get(key=token)
        return Response({ "message": "success"})

class UserAccount(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, req, format=None):
        user = req.user
        if req.user.is_authenticated:
            account = get_serialized_account(user)
            account["username"] = user.username
            return Response(account)
        else: 
            return Response({
                "anonymous": "not authenticated" 
            })
class Users(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, req, format=None):
        q = req.query_params["q"]
        usernames = User.objects.filter(username__icontains=q)
        username_serializer = UserSerializer(usernames, many=True).data
        return Response(username_serializer)