from django.db import models
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from utilities.utilities import hundred_years_from_now

from ..models import Article, PublishedArticleManager



class TestEntry(TestCase):

    def setUp(self):
        self.model = Article

    def test_title_field(self):
        field = self.model._meta.get_field('title')
        field_type_expected = models.CharField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        field_max_length_expected = 30
        field_max_length_given = field.max_length
        self.assertEqual(field_max_length_expected, field_max_length_given)

    def test_body_field(self):
        field = self.model._meta.get_field('body')
        field_type_expected = models.TextField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        field_max_length_expected = 1000
        field_max_length_given = field.max_length
        self.assertEqual(field_max_length_expected, field_max_length_given)
        field_default_expected = "some text"
        field_default_given = field.default
        self.assertEqual(field_default_expected, field_default_given)

    def test_created_field(self):
        field = self.model._meta.get_field('created')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        self.assertTrue(field.auto_now_add)

    def test_modified_field(self):
        field = self.model._meta.get_field('modified')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        self.assertTrue(field.auto_now)

    def test_pub_date_field(self):
        field = self.model._meta.get_field('pub_date')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        default_expected = hundred_years_from_now
        default_given = field.default
        self.assertEqual(default_expected, default_given)

    def test_comments_count_field(self):
        field = self.model._meta.get_field('comments_count')
        field_type_expected = models.PositiveSmallIntegerField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        default_expected = 0
        default_given = field.default
        self.assertEqual(default_expected, default_given)

    def test_model_objects_attr_is_proper_class(self):
        class_expected = models.Manager
        class_given = self.model.objects.__class__
        self.assertEqual(class_expected, class_given)

    def test_model_custom_manager_attr(self):
        class_expected = PublishedArticleManager
        class_given = self.model.published.__class__
        self.assertEqual(class_expected, class_given)

    def test_model_ordering(self):
        ordering_expected = ['-modified']
        ordering_given = self.model._meta.ordering
        self.assertEqual(ordering_expected, ordering_given)

    def test_model_verbose_name_plural(self):
        verbose_name_plural_expected = "Articles"
        verbose_name_plural_given = self.model._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural_expected, verbose_name_plural_given)

    def test_str_method(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article = self.model.objects.create(
            title = 'Firenze',
            body = 'test',
            pub_date = in_the_past
        )
        string_expected = 'Firenze'
        string_given = article.__str__()
        self.assertEqual(string_expected, string_given)

    def test_get_absolut_url(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article = self.model.objects.create(
            title = 'Firenze',
            body = 'test',
            pub_date = in_the_past
        )
        viewname = 'articles:detail'
        kwargs = {'pk': article.id}
        get_absolut_url_expected = reverse(viewname, kwargs = kwargs)
        get_absolut_url_given = article.get_absolut_url()
        self.assertEqual(get_absolut_url_expected, get_absolut_url_given)


class TestPublishedArticleManager(TestCase):

    def test_manager_inherits_from_proper_class(self):
        class_expected = models.Manager
        class_given = Article.published.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_manager_returns_proper_queryset(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        article_published_1 = Article.objects.create(
            title = 'uno_publshed',
            body = 'test',
            pub_date = in_the_past
        )
        article_published_2 = Article.objects.create(
            title = 'due_published',
            body = 'test',
            pub_date = in_the_past
        )
        article_not_published_1 = Article.objects.create(
            title = 'uno_not_published',
            body = 'test',
            pub_date = in_the_future
        )
        article_not_published_2 = Article.objects.create(
            title = 'due_not_published',
            body = 'test',
            pub_date = in_the_future
        )
        queryset_returned = Article.published.all()
        self.assertIn(article_published_1, queryset_returned)
        self.assertIn(article_published_2, queryset_returned)
        self.assertNotIn(article_not_published_1, queryset_returned)
        self.assertNotIn(article_not_published_1, queryset_returned)
