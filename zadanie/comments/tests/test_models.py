from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.test import TestCase

from ..models import Comment



class TestComment(TestCase):

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

    def test_content_type_field(self):
        field = self.model._meta.get_field('content_type')
        field_type_expected = models.ForeignKey
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        field_related_model_expected = ContentType
        field_related_model_given = field.related_model
        self.assertEqual(field_related_model_expected, field_related_model_given)

    def test_object_id_field(self):
        field = self.model._meta.get_field('object_id')
        field_type_expected = models.PositiveIntegerField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)

    def test_content_object_field(self):
        field = self.model._meta.get_field('content_object')
        field_type_expected = GenericForeignKey
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
