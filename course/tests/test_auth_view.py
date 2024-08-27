from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.test import TestCase
from django.urls import reverse
from course.forms import CustomUserCreationForm

User = get_user_model()


class AuthViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="TestUser", password="Password123_"
        )

    def test_register_view_get(self):
        response = self.client.get(reverse("course:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course/register.html")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_register_view_post(self):
        form_data = {
            "username": "new_user",
            "first_name": "Test3",
            "last_name": "Driver3",
            "password1": "new_password123",
            "password2": "new_password123",
        }
        new_user = User.objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertTrue(new_user.check_password(form_data["password1"]))

    def test_login_view_get(self):
        response = self.client.get(reverse("course:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course/login.html")
        self.assertIsInstance(response.context["form"], AuthenticationForm)

    def test_login_view_post(self):
        login_data = {
            "username": "TestUser",
            "password": "Password123_",
        }
        response = self.client.post(reverse("course:login"), data=login_data)
        self.assertEqual(response.status_code, 302)

        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, "TestUser")

    def test_poster_view(self):
        response = self.client.get(reverse("course:poster"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course/poster.html")
