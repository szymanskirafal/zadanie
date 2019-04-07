from django.test import TestCase

from django.urls import resolve, reverse


class TestEntriesUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entries')
        url_expected = '/blog/entries/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryListView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entries'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entries'
        self.assertEqual(view_name_given, view_name_expected)


class TestEntryCreateUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/create/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entry-create')
        url_expected = '/blog/entries/create/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryCreateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entry-create'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entry-create'
        self.assertEqual(view_name_given, view_name_expected)


class TestEntryCreatedUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/created/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entry-created')
        url_expected = '/blog/entries/created/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryCreatedTemplateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entry-created'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entry-created'
        self.assertEqual(view_name_given, view_name_expected)


class TestEntryDetailUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/1/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entry-detail', kwargs = {'pk': 1})
        url_expected = '/blog/entries/1/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryDetailView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entry-detail'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entry-detail'
        self.assertEqual(view_name_given, view_name_expected)

    def test_url_kwargs(self):
        kwargs_given = self.url_resolved.kwargs
        kwargs_expected = {'pk': 1}
        self.assertEqual(kwargs_given, kwargs_expected)


class TestEntryDeletedUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/deleted/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entry-deleted')
        url_expected = '/blog/entries/deleted/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryDeletedTemplateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entry-deleted'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entry-deleted'
        self.assertEqual(view_name_given, view_name_expected)


class TestEntryUpdateUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/blog/entries/1/update/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'blog'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('blog:entry-update', kwargs = {'pk': 1})
        url_expected = '/blog/entries/1/update/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'EntryUpdateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'entry-update'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'blog'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'blog:entry-update'
        self.assertEqual(view_name_given, view_name_expected)

    def test_url_kwargs(self):
        kwargs_given = self.url_resolved.kwargs
        kwargs_expected = {'pk': 1}
        self.assertEqual(kwargs_given, kwargs_expected)
