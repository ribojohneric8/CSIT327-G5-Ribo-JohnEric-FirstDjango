from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class ProfileUpdateViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="student",
            password="test-password",
            role=CustomUser.Role.STUDENT,
        )
        self.client.force_login(self.user)

    def test_profile_update_changes_only_allowed_fields_for_current_user(self):
        response = self.client.post(
            reverse("profile"),
            {
                "first_name": "Alex",
                "last_name": "Student",
                "email": "alex@example.com",
                "course": "BSIT",
                "role": CustomUser.Role.ADMIN,
            },
        )

        self.assertRedirects(response, reverse("dashboard"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Alex")
        self.assertEqual(self.user.last_name, "Student")
        self.assertEqual(self.user.email, "alex@example.com")
        self.assertEqual(self.user.course, "BSIT")
        self.assertEqual(self.user.role, CustomUser.Role.STUDENT)

    def test_profile_page_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("profile"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('profile')}",
        )


class SignUpFeedbackTests(TestCase):
    def test_successful_signup_shows_message_on_login_page(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "first_name": "New",
                "last_name": "Student",
                "course": "BSIT",
                "password1": "CampusConnect!2026Strong",
                "password2": "CampusConnect!2026Strong",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("login"))
        self.assertContains(response, "Your account was created successfully.")
