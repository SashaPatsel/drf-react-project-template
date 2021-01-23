from django import forms
from .models import Account, File

class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', "photo"]

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = [ "data"]

# class BadgeApplicationForm(forms.ModelForm):
#     class Meta:
