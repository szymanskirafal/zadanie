from django.db import models
from django.urls import reverse
from django.test import TestCase

from ..models import Entry, PublishedEntryManager
from ..utils import hundred_years_from_now, yesterday


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

    def test_model_objects_attr_is_proper_class(self):
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
        entry = Entry.objects.create(
            title = 'Roma',
            body = 'test',
            pub_date = yesterday()
        )
        string_expected = 'Roma'
        string_given = entry.__str__()
        self.assertEqual(string_expected, string_given)

    def test_get_absolut_url(self):
        entry = Entry.objects.create(
            title = 'Roma',
            body = 'test',
            pub_date = yesterday()
        )
        viewname = 'blog:entry-detail'
        kwargs = {'pk': entry.id}
        get_absolut_url_expected = reverse(viewname, kwargs = kwargs)
        get_absolut_url_given = entry.get_absolut_url()
        self.assertEqual(get_absolut_url_expected, get_absolut_url_given)
"""
    def get_absolut_url(self):

        return absolut_url
"""
