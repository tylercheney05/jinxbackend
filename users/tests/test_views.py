import random
import string

from django.test import TestCase
from model_bakery import baker
from rest_framework import permissions, views
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import User
from users.views import RegisterView, RetrieveUserView


class TestRegisterView(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(RegisterView, views.APIView))

    def test_permission_classes(self):
        view = RegisterView()
        self.assertEqual(view.permission_classes, [permissions.AllowAny])


class TestRegisterViewPost(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=10)
        )
        self.data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": random_string,
        }

    def test_if_not_valid(self):
        data = self.data.copy()
        data["email"] = ""  # Invalid email
        request = self.factory.post(
            "/register/",
            data,
            content_type="application/json",
        )

        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_if_valid(self):
        request = self.factory.post(
            "/register/",
            self.data,
        )

        view = RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)


class TestRetrieveUserView(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(RetrieveUserView, views.APIView))

    def test_permission_classes(self):
        view = RetrieveUserView()
        self.assertEqual(view.permission_classes, [permissions.IsAuthenticated])

    def test_get(self):
        user = baker.make(User)
        factory = APIRequestFactory()
        request = factory.get("/me/")
        force_authenticate(request, user=user)
        view = RetrieveUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
