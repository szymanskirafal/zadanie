from django.test import TestCase

from django.urls import get_script_prefix, resolve, reverse

class TestEntryCreateUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/create/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:create')
        url_expected = '/articles/create/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleCreateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'create'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:create'
        self.assertEqual(view_name_given, view_name_expected)


class TestArticleCreatedUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/created/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:created')
        url_expected = '/articles/created/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleCreatedTemplateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'created'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:created'
        self.assertEqual(view_name_given, view_name_expected)



class TestArticlesDetailUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/1/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:detail', kwargs = {'pk': 1})
        url_expected = '/articles/1/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleDetailView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'detail'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:detail'
        self.assertEqual(view_name_given, view_name_expected)

    def test_url_kwargs(self):
        kwargs_given = self.url_resolved.kwargs
        kwargs_expected = {'pk': 1}
        self.assertEqual(kwargs_given, kwargs_expected)

class TestArticlesDeletelUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/1/delete/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:delete', kwargs = {'pk': 1})
        url_expected = '/articles/1/delete/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleDeleteView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'delete'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:delete'
        self.assertEqual(view_name_given, view_name_expected)

    def test_url_kwargs(self):
        kwargs_given = self.url_resolved.kwargs
        kwargs_expected = {'pk': 1}
        self.assertEqual(kwargs_given, kwargs_expected)


class TestArticleDeletedUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/deleted/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:deleted')
        url_expected = '/articles/deleted/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleDeletedTemplateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'deleted'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:deleted'
        self.assertEqual(view_name_given, view_name_expected)


class TestArticlesUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:list')
        url_expected = '/articles/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticlesListView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'list'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:list'
        self.assertEqual(view_name_given, view_name_expected)


class TestArticleUpdateUrl(TestCase):

    def setUp(self):
        self.url_resolved = resolve('/articles/1/update/')

    def test_url_app_name(self):
        app_name_given = self.url_resolved.app_name
        app_name_expected = 'articles'
        self.assertEqual(app_name_given, app_name_expected)

    def test_url_reverse(self):
        url_given = reverse('articles:update', kwargs = {'pk': 1})
        url_expected = '/articles/1/update/'
        self.assertEqual(url_given, url_expected)

    def test_url_func_name(self):
        func_name_given = self.url_resolved.func.__name__
        func_name_expected = 'ArticleUpdateView'
        self.assertEqual(func_name_given, func_name_expected)

    def test_url_name(self):
        url_name_given = self.url_resolved.url_name
        url_name_expected = 'update'
        self.assertEqual(url_name_given, url_name_expected)

    def test_url_namespace(self):
        namespace_given = self.url_resolved.namespace
        namespace_expected = 'articles'
        self.assertEqual(namespace_given, namespace_expected)

    def test_url_view_name(self):
        view_name_given = self.url_resolved.view_name
        view_name_expected = 'articles:update'
        self.assertEqual(view_name_given, view_name_expected)

    def test_url_kwargs(self):
        kwargs_given = self.url_resolved.kwargs
        kwargs_expected = {'pk': 1}
        self.assertEqual(kwargs_given, kwargs_expected)
