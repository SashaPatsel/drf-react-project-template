from .models import Account
from rest_framework import viewsets, permissions
from .serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
  permission_classes = [
    permissions.IsAuthenticated
  ] 

  serializer_class = AccountSerializer

  def get_queryset(self):
    return self.request.user.accounts.all()

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)