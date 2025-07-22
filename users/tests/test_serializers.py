from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker
from rest_framework import serializers

from users.models import User
from users.serializers import UserCreateSerializer


class TestUserCreateSerializer(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(UserCreateSerializer, serializers.ModelSerializer))

    def test_model(self):
        serializer = UserCreateSerializer()
        self.assertEqual(serializer.Meta.model, User)

    def test_fields(self):
        serializer = UserCreateSerializer()
        self.assertEqual(
            serializer.Meta.fields, ("first_name", "last_name", "email", "password")
        )

    @patch("users.serializers.validate_password")
    def test_validate(self, validate_password):
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123",
        }
        UserCreateSerializer().validate(data)
        self.assertTrue(validate_password.called)

    @patch("users.models.User.objects.create_user")
    def test_create(self, create_user):
        create_user.return_value = baker.make(User)
        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "password123",
        }
        UserCreateSerializer().create(data)
        create_user.assert_called_once_with(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data["password"],
        )


class TestUserSerializer(TestCase):
    def test_sub_class(self):
        from users.serializers import UserSerializer

        self.assertTrue(issubclass(UserSerializer, serializers.ModelSerializer))

    def test_model(self):
        from users.serializers import UserSerializer

        serializer = UserSerializer()
        self.assertEqual(serializer.Meta.model, User)

    def test_fields(self):
        from users.serializers import UserSerializer

        serializer = UserSerializer()
        self.assertEqual(
            serializer.Meta.fields,
            ("id", "first_name", "last_name", "email", "is_admin", "is_staff"),
        )
