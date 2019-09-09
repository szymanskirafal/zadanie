from django.contrib.auth import get_user_model
from django.test import TestCase


class CustomUserTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='anna',
            email='anna@anna.com',
            password='somepass',
        )
        self.assertEqual(user.username, 'anna')
        self.assertEqual(user.email, 'anna@anna.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
