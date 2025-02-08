import secrets
from unittest.mock import MagicMock

from django.test import TestCase

from core.permissions import IsSystemAdminUser, IsSystemAdminUserOrIsStaffUserReadOnly


class TestIsSystemAdminUser(TestCase):
    def test_user_is_admin(self):
        request = MagicMock()
        request.user.is_admin = True
        permission = IsSystemAdminUser()
        self.assertTrue(permission.has_permission(request, None))

    def test_user_is_not_admin(self):
        request = MagicMock()
        request.user.is_admin = False
        permission = IsSystemAdminUser()
        self.assertFalse(permission.has_permission(request, None))

    def test_no_user(self):
        request = MagicMock()
        request.user = None
        permission = IsSystemAdminUser()
        self.assertFalse(permission.has_permission(request, None))


class TestIsSystemAdminUserOrIsStaffUserReadOnly(TestCase):

    def test_user_is_admin(self):
        request = MagicMock()
        request.user.is_admin = True
        permission = IsSystemAdminUserOrIsStaffUserReadOnly()
        self.assertTrue(permission.has_permission(request, None))

    def test_request_method_is_not_get(self):
        non_get_methods = ["POST", "PUT", "PATCH", "DELETE"]

        request = MagicMock()
        request.method = secrets.choice(non_get_methods)
        request.user.is_staff = True
        request.user.is_admin = False
        permission = IsSystemAdminUserOrIsStaffUserReadOnly()
        self.assertFalse(permission.has_permission(request, None))

    def test_no_user(self):
        request = MagicMock()
        request.method = "GET"
        request.user = None
        permission = IsSystemAdminUserOrIsStaffUserReadOnly()
        self.assertFalse(permission.has_permission(request, None))

    def test_user_is_not_staff(self):
        request = MagicMock()
        request.method = "GET"
        request.user.is_staff = False
        request.user.is_admin = False
        permission = IsSystemAdminUserOrIsStaffUserReadOnly()
        self.assertFalse(permission.has_permission(request, None))

    def test_request_method_is_get_and_user_is_staff(self):
        request = MagicMock()
        request.method = "GET"
        request.user.is_staff = True
        request.user.is_admin = False
        permission = IsSystemAdminUserOrIsStaffUserReadOnly()
        self.assertTrue(permission.has_permission(request, None))
