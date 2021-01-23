from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import requests
import json
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser



class FirstView(APIView):
  permission_classes = (permissions.AllowAny,)

  def get(self, req, format=None):
    return Response({})

  def post(self, req, format=None):
    return Response({})

  def put(self, req, format=None):
    return Response({})

  def delete(self, req, format=None):
    return Response({})