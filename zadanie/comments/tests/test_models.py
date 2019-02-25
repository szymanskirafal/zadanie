from django.db import models
from django.urls import reverse
from django.test import TestCase

from ..models import Comment



class TestEntry(TestCase):

    def setUp(self):
        self.model = Comment

    def test_body_field(self):
        field = self.model._meta.get_field('body')
        field_type_expected = models.TextField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        field_max_length_expected = 300
        field_max_length_given = field.max_length
        self.assertEqual(field_max_length_expected, field_max_length_given)
        field_default_expected = "some comment"
        field_default_given = field.default
        self.assertEqual(field_default_expected, field_default_given)

    def test_created_field(self):
        field = self.model._meta.get_field('created')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        self.assertTrue(field.auto_now_add)
