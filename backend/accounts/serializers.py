from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from .models import *
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
  username = serializers.CharField(source='user.username', read_only=True)

  # photo_url = serializers.SerializerMethodField('get_photo_url')

  class Meta:
    model = Account
    fields = ("id", "username", "first_name", "last_name", "organization", "photo", "email_subscribed", "expert_badge", "is_curator")

  # def get_photo_url(self, obj):
  #   return obj.photo.url

class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User 
    fields = "__all__"

class UserSerializerWithToken(serializers.ModelSerializer):
  """
  Used for signups
  """
  token = serializers.SerializerMethodField()
  password = serializers.CharField(write_only=True)

  def get_token(self, obj):
      jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
      jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

      payload = jwt_payload_handler(obj)
      token = jwt_encode_handler(payload)
      return token

  def create(self, validated_data):
      password = validated_data.pop('password', None)
      instance = self.Meta.model(**validated_data)
      if password is not None:
          instance.set_password(password)
      instance.save()
      return instance

  class Meta:
      model = User
      fields = "__all__"


def get_serialized_account(user):
    account = Account.objects.get(user=user)
    return AccountSerializer(account).data



class NotificationSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Notification 
    fields = "__all__"