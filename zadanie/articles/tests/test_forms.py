from django.forms import ModelForm
from django.test import TestCase

from ..forms import ArticleForm
from ..models import Article


class TestArticleForm(TestCase):

    def test_form_inherits_from_proper_class(self):
        class_expected = ModelForm.__class__
        class_given = ArticleForm.__class__
        self.assertEqual(class_expected, class_given)

    def test_form_refers_to_correct_model(self):
        model_expected = Article
        model_given = ArticleForm._meta.model
        self.assertEqual(model_expected, model_given)

    def test_form_defines_correct_fields_set(self):
        fields_set_expected = ['title', 'body', 'pub_date', ]
        fields_set_given = ArticleForm._meta.fields
        self.assertEqual(fields_set_expected, fields_set_given)
