from django.forms import ModelForm
from django.test import TestCase

from ..forms import CommentForm
from ..models import Comment


class TestArticleForm(TestCase):

    def test_form_inherits_from_proper_class(self):
        class_expected = ModelForm
        class_given = CommentForm.__class__
        self.assertEqual(class_expected, class_given)

    def test_form_refers_to_correct_model(self):
        model_expected = Comment
        model_given = CommentForm._meta.model
        self.assertEqual(model_expected, model_given)

    def test_form_defines_correct_fields_set(self):
        fields_set_expected = ['body', ]
        fields_set_given = CommentForm._meta.fields
        self.assertEqual(fields_set_expected, fields_set_given)
