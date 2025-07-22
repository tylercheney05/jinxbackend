from unittest.mock import patch

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.test import TestCase
from model_bakery import baker

from users.models import User, UserManager


class TestUser(TestCase):
    def test_sub_classes(self):
        self.assertTrue(issubclass(User, AbstractBaseUser))
        self.assertTrue(issubclass(User, PermissionsMixin))

    def test_str(self):
        user = baker.make(User)
        self.assertEqual(str(user), user.email)

    def test_first_name(self):
        user = baker.make(User)
        field = user._meta.get_field("first_name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_last_name(self):
        user = baker.make(User)
        field = user._meta.get_field("last_name")
        self.assertIsInstance(field, models.CharField)
        self.assertEqual(field.max_length, 255)

    def test_email(self):
        user = baker.make(User)
        field = user._meta.get_field("email")
        self.assertIsInstance(field, models.EmailField)
        self.assertEqual(field.max_length, 255)
        self.assertTrue(field.unique)

    def test_date_joined(self):
        user = baker.make(User)
        field = user._meta.get_field("date_joined")
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now_add)

    def test_last_login(self):
        user = baker.make(User)
        field = user._meta.get_field("last_login")
        self.assertIsInstance(field, models.DateTimeField)
        self.assertTrue(field.auto_now)

    def test_is_active(self):
        user = baker.make(User)
        field = user._meta.get_field("is_active")
        self.assertIsInstance(field, models.BooleanField)
        self.assertTrue(field.default)

    def test_is_admin(self):
        user = baker.make(User)
        field = user._meta.get_field("is_admin")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)

    def test_is_staff(self):
        user = baker.make(User)
        field = user._meta.get_field("is_staff")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)

    def test_is_superuser(self):
        user = baker.make(User)
        field = user._meta.get_field("is_superuser")
        self.assertIsInstance(field, models.BooleanField)
        self.assertFalse(field.default)

    def test_username_field(self):
        user = baker.make(User)
        self.assertEqual(user.USERNAME_FIELD, "email")

    def test_required_fields(self):
        user = baker.make(User)
        self.assertEqual(user.REQUIRED_FIELDS, ["first_name", "last_name"])

    def test_objects_is_user_manager(self):
        self.assertIsInstance(User.objects, UserManager)


class TestUserManager(TestCase):
    def test_sub_class(self):
        self.assertTrue(issubclass(UserManager, BaseUserManager))


class TestUserManagerCreateUser(TestCase):
    def test_if_not_email(self):
        with self.assertRaises(ValueError):
            UserManager().create_user(
                first_name="Test", last_name="User", email=None, password="password123"
            )

    @patch("users.models.User.set_password")
    @patch("users.models.UserManager.normalize_email")
    def test_if_email(self, normalize_email, set_password):
        normalize_email.return_value = "test@example.com"

        User.objects.create_user(
            first_name="Test",
            last_name="User",
            email="Test@example.com",
            password="password123",
        )

        self.assertTrue(normalize_email.called)
        self.assertTrue(set_password.called)
        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertEqual(user.email, "test@example.com")


class TestUserManagerCreateSuperuser(TestCase):
    def test_create_superuser(self):
        user = User.objects.create_superuser(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            password="password123",
        )

        self.assertEqual(User.objects.count(), 1)

        user = User.objects.first()
        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
