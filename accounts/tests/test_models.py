from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import User

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user_successfull(self):
        """Test creating a regular user with email and password."""

        user = User.objects.create_user(
            email="STUDENT@ju.ac.bd",
            full_name="Test Student",
            password="secret1234",
        )
        self.assertEqual(user.email, "student@ju.ac.bd")

        self.assertTrue(user.check_password("secret1234"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_missing_email_raises_error(self):
        """Test that creating a user with no email raises a ValueError."""

        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                full_name="No Email User",
                password="password123",
            )

    def test_create_superuser_successfull(self):
        """Test creating a superuser with email and password."""
        admin_user = User.objects.create_superuser(
            email="admin@ju.ac.bd",
            full_name="System Admin",
            password="admin1234",
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_superuser_invalid_flags_raises_error(self):
        """Test that superuser creation fails if staff or superuser flags are False."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="fakeadmin@ju.ac.bd",
                full_name="Fake Admin",
                password="password123",
                is_staff=False,
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="fakeadmin2@ju.ac.bd",
                full_name="Fake Admin 2",
                password="password123",
                is_staff=False,
            )

    def test_duplicate_email_case_insensitive_raises_integrity_error(self):
        """Test that our PostgreSQL constraint prevents duplicate emails regardless of casing."""
        User.objects.create_user(
            email="kazi@ju.ac.bd",
            full_name="Kazi First",
            password="password123",
        )
        # Attempting to insert a user with different case should violate the unique constraint
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="KAZI@JU.AC.BD",
                full_name="Kazi Duplicate",
            )