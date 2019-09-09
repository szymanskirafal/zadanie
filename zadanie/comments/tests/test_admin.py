from django.contrib.admin import ModelAdmin
from django.test import TestCase

from ..admin import CommentAdmin


class TestArticleAdmin(TestCase):

    def test_admin_inherits_from_proper_class(self):
        class_expected = ModelAdmin.__class__
        class_given = CommentAdmin.__class__
        self.assertEqual(class_expected, class_given)

    def test_admin_fields_set(self):
        fields_set_expected = ('body', 'content_object',)
        fields_set_given = CommentAdmin.fields
        self.assertEqual(fields_set_expected, fields_set_given)
