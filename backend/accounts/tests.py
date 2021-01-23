from django.test import TestCase
from django.urls import reverse, resolve
from .views import *

class ProfileTests(TestCase):
    def test_profile_view_status_code(self):
        url = reverse("profile", kwargs={"username": "wildfishy"})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_profile_url_resolves_profile_view(self):
        view = resolve("/accounts/profile/wildfishy")
        self.assertEquals(view.func, profile)

class SettingsTests(TestCase):
    def test_settings_view_status_code(self):
        url = reverse("user_settings")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_settings_url_resolves_settings_view(self):
        view = resolve("/accounts/user_settings")
        self.assertEquals(view.func, user_settings)

class CuratorTests(TestCase):
    def test_curator_view_status_code(self):
        url = reverse("curator")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_curator_url_resolves_curator_view(self):
        view = resolve("/accounts/curator")
        self.assertEquals(view.func, curator)