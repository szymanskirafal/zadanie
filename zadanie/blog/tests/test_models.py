from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from utilities.utilities import hundred_years_from_now

from comments.models import Comment

from ..models import Entry, PublishedEntryManager


class TestEntry(TestCase):

    def test_title_field(self):
        field = Entry._meta.get_field('title')
        field_type_expected = models.CharField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        field_max_length_expected = 30
        field_max_length_given = field.max_length
        self.assertEqual(field_max_length_expected, field_max_length_given)

    def test_body_field(self):
        field = Entry._meta.get_field('body')
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
        field = Entry._meta.get_field('created')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        self.assertTrue(field.auto_now_add)

    def test_modified_field(self):
        field = Entry._meta.get_field('modified')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        self.assertTrue(field.auto_now)

    def test_pub_date_field(self):
        field = Entry._meta.get_field('pub_date')
        field_type_expected = models.DateTimeField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        default_expected = hundred_years_from_now
        default_given = field.default
        self.assertEqual(default_expected, default_given)

    def test_comments_count_field(self):
        field = Entry._meta.get_field('comments_count')
        field_type_expected = models.PositiveSmallIntegerField
        field_type_given = field.__class__
        self.assertEqual(field_type_expected, field_type_given)
        default_expected = 0
        default_given = field.default
        self.assertEqual(default_expected, default_given)

    def test_comments_field(self):
        field = Entry._meta.get_field('comments')
        class_expected = GenericRelation
        class_given = field.__class__
        self.assertEqual(class_expected, class_given)
        related_model_expected = Comment
        related_model_given = field.related_model
        self.assertEqual(related_model_expected, related_model_given)

    def test_model_objects_manager_is_proper_class(self):
        class_expected = models.Manager
        class_given = Entry.objects.__class__
        self.assertEqual(class_expected, class_given)

    def test_model_custom_manager_attr(self):
        class_expected = PublishedEntryManager
        class_given = Entry.published.__class__
        self.assertEqual(class_expected, class_given)

    def test_model_ordering(self):
        ordering_expected = ['-modified']
        ordering_given = Entry._meta.ordering
        self.assertEqual(ordering_expected, ordering_given)

    def test_model_verbose_name_plural(self):
        verbose_name_plural_expected = "Entries"
        verbose_name_plural_given = Entry._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural_expected, verbose_name_plural_given)

    def test_str_method(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        entry = Entry.objects.create(
            title = 'Roma',
            body = 'test',
            pub_date = in_the_past
        )
        string_expected = 'Roma'
        string_given = entry.__str__()
        self.assertEqual(string_expected, string_given)

    def test_get_absolut_url(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        entry = Entry.objects.create(
            title = 'Roma',
            body = 'test',
            pub_date = in_the_past
        )
        viewname = 'blog:entry-detail'
        kwargs = {'pk': entry.id}
        get_absolut_url_expected = reverse(viewname, kwargs = kwargs)
        get_absolut_url_given = entry.get_absolut_url()
        self.assertEqual(get_absolut_url_expected, get_absolut_url_given)


class TestPublishedEntryManager(TestCase):

    def test_manager_inherits_from_proper_class(self):
        class_expected = models.Manager
        class_given = Entry.published.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_manager_returns_proper_queryset(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        entry_published_1 = Entry.objects.create(
            title = 'uno_publshed',
            body = 'test',
            pub_date = in_the_past
        )
        entry_published_2 = Entry.objects.create(
            title = 'due_published',
            body = 'test',
            pub_date = in_the_past
        )
        entry_not_published_1 = Entry.objects.create(
            title = 'uno_not_published',
            body = 'test',
            pub_date = in_the_future
        )
        entry_not_published_2 = Entry.objects.create(
            title = 'due_not_published',
            body = 'test',
            pub_date = in_the_future
        )
        queryset_returned = Entry.published.all()
        self.assertIn(entry_published_1, queryset_returned)
        self.assertIn(entry_published_2, queryset_returned)
        self.assertNotIn(entry_not_published_1, queryset_returned)
        self.assertNotIn(entry_not_published_1, queryset_returned)
