from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone
from django.views import generic, View

from django.contrib.auth.models import AnonymousUser

from ..forms import ArticleForm
from ..models import Article
from ..views import (
    ArticleCreateView,
    ArticleCreatedTemplateView,
    ArticleDeleteView,
    ArticleDeletedTemplateView,
    ArticleDetailView,
    ArticleDetailAddCommentView,
    ArticleDetailJustDisplayView,
    ArticlesListView,
    ArticleUpdateView,
)


class TestArticleCreateView(TestCase):

    def setUp(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        self.path = reverse('articles:create')
        self.view = ArticleCreateView()
        self.data_to_post = {
            'title': 'Pizza',
            'body': 'some text',
            'pub_date': in_the_past.strftime('%Y-%m-%d'),
        }
        self.request = RequestFactory().post(self.path, data=self.data_to_post)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.CreateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_form_class(self):
        form_class_expected = ArticleForm
        form_class_given = self.view.form_class
        self.assertEqual(form_class_expected, form_class_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Article
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'articles/article-create.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_get_success_url(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article = Article.objects.create(
            title = 'milano',
            body = 'test',
            pub_date = in_the_past
        )
        self.view.object = article
        viewname = 'articles:created'
        get_success_url_expected = reverse(viewname)
        get_success_url_given = self.view.get_success_url()
        self.assertEqual(get_success_url_expected, get_success_url_given)

    def test_view_creates_published_instance(self):
        self.assertEqual(Article.objects.count(), 0)
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        Article.objects.create(
            title = 'milano',
            body = 'test',
            pub_date = in_the_past
        )
        self.assertEqual(Article.published.count(), 1)

    def test_view_returns_expected_code_after_creating_instance(self):
        status_code_expected = 302
        response = ArticleCreateView.as_view()(self.request)
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_view_creates_not_published_instance(self):
        self.assertEqual(Article.objects.count(), 0)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        data_to_post = self.data_to_post
        data_to_post['pub_date'] = in_the_future.strftime('%Y-%m-%d')
        request = RequestFactory().post(self.path, data = data_to_post)
        response = ArticleCreateView.as_view()(request)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.published.count(), 0)
        self.assertEqual(response.status_code, 302)


class TestArticleCreatedTemplateView(TestCase):

    def setUp(self):
        factory = RequestFactory()
        url = '/fake-url'
        request = factory.get(url)
        self.view = ArticleCreatedTemplateView()
        self.response = ArticleCreatedTemplateView.as_view()(request)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.TemplateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_template_name_attr(self):
        template_name_expected = 'articles/article-created.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_view_uses_correct_template(self):
        template_name_expected = ['articles/article-created.html']
        template_name_given = self.response.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_status_code(self):
        status_code_expected = 200
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)


class TestArticleDetailView(TestCase):

    def test_view_inherits_from_correct_class(self):
        class_expected = View
        class_given = ArticleDetailView().__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_get_method_runs_another_view(self):
        view_class_expected = ArticleDetailJustDisplayView
        url = '/fake-url'
        request = RequestFactory().get(url)
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = in_the_past,
        )
        pk = article_published.pk
        response = ArticleDetailView.get(self, request, pk = pk)
        view_used_after_get = response.__dict__['context_data']['view']
        view_class_given = view_used_after_get.__class__
        self.assertEqual(view_class_expected, view_class_given)

    def test_view_post_method_runs_another_view(self):
        view_class_expected = ArticleDetailAddCommentView
        url = '/fake-url'
        request = RequestFactory().post(url)
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = in_the_past,
        )
        pk = article_published.pk
        response = ArticleDetailView.post(self, request, pk = pk)
        view_used_after_post = response.context_data['view']
        view_class_given = view_used_after_post.__class__
        self.assertEqual(view_class_expected, view_class_given)


class TestArticleDetailJustDisplayView(TestCase):

    def setUp(self):
        self.view = ArticleDetailJustDisplayView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.DetailView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_context_object_name_attr(self):
        context_object_name_expected = 'article'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(
            context_object_name_expected,
            context_object_name_given
        )

    def test_view_queryset_attr(self):
        queryset_expected = Article.published
        queryset_given = self.view.queryset
        self.assertEqual(queryset_expected, queryset_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'articles/article-detail.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_get_context_data_should_return_variables_in_context(self):
        url = '/fake-url'
        request = RequestFactory().get(url)
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = in_the_past,
        )
        article_published.comments.create(body = 'few words')
        pk = article_published.pk
        response = ArticleDetailView.get(self, request, pk = pk)
        self.assertTrue(response.context_data['form'])
        self.assertTrue(response.context_data['comments'])

    def test_status_code(self):
        status_code_expected = 200
        url = '/fake-url'
        request = RequestFactory().get(url)
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = in_the_past,
        )
        article_published.comments.create(body = 'few words')
        pk = article_published.pk
        response = ArticleDetailView.get(self, request, pk = pk)
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)


class TestArticleDetailAddCommentView(TestCase):

    def setUp(self):
        self.view = ArticleDetailAddCommentView()

    def test_view_inherits_from_correct_classes(self):
        class_expected_as_first_on_the_left = generic.detail.SingleObjectMixin
        class_expected_as_second_on_the_left = generic.FormView
        classes_given = self.view.__class__.__bases__
        class_given_as_first_on_the_left = classes_given[0]
        class_given_as_second_on_the_left = classes_given[1]
        self.assertEqual(
            class_expected_as_first_on_the_left,
            class_given_as_first_on_the_left
        )
        self.assertEqual(
            class_expected_as_second_on_the_left,
            class_given_as_second_on_the_left
        )


class TestArticleDeleteView(TestCase):

    def setUp(self):
        url = '/fake-url'
        self.request = RequestFactory().get(url)
        self.view = ArticleDeleteView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.DeleteView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_template(self):
        template_name_expected = 'articles/article-delete.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_view_uses_correct_success_url(self):
        success_url_expected = '/articles/deleted/'
        success_url_given = self.view.success_url
        self.assertEqual(success_url_expected, success_url_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Article
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_status_code(self):
        status_code_expected = 200
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = in_the_past
        )
        pk = article_published.pk
        request = self.request
        view = self.view.__class__.as_view()
        response = view(request, pk = pk)
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)


class TestArticleDeletedTemplateView(TestCase):

    def setUp(self):
        url = '/fake-url'
        self.request = RequestFactory().get(url)
        self.view = ArticleDeletedTemplateView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.TemplateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_template(self):
        template_name_expected = 'articles/article-deleted.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)


class TestArticlesListView(TestCase):

    def setUp(self):
        self.view = ArticlesListView()
        self.request = RequestFactory().get('/fake-url')
        self.response = ArticlesListView.as_view()(self.request)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.ListView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_context_object_name_attr(self):
        context_object_name_expected = 'articles'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(
            context_object_name_expected,
            context_object_name_given
        )

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Article
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'articles/articles.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_status_code(self):
        status_code_expected = 200
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_status_code_for_anonymous_user(self):
        status_code_expected = 200
        self.request.user = AnonymousUser()
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_template_used(self):
        template_name_expected = 'articles/list.html'
        template_name_given = self.response.template_name
        self.assertTrue(template_name_expected, template_name_given)

    def test_get_queryset(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'Genoa',
            body = 'published',
            pub_date = in_the_past,
        )
        article_not_published = Article.objects.create(
            title = 'Verona',
            body = 'not published',
            pub_date = in_the_future,
        )
        view = self.view
        view.request = self.request
        queryset_given = view.get_queryset()
        object_supposed_to_be_in_queryset = article_published
        object_not_supposed_to_be_in_queryset = article_not_published
        self.assertIn(object_supposed_to_be_in_queryset, queryset_given)
        self.assertNotIn(object_not_supposed_to_be_in_queryset, queryset_given)


class TestArticleUpdateView(TestCase):

    def setUp(self):
        self.view = ArticleUpdateView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.UpdateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_context_object_name_attr(self):
        context_object_name_expected = 'article'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(
            context_object_name_expected,
            context_object_name_given
        )

    def test_view_uses_correct_form_class(self):
        form_class_expected = ArticleForm
        form_class_given = self.view.form_class
        self.assertEqual(form_class_expected, form_class_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Article
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'articles/article-update.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_get_success_url(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article = Article.objects.create(
            title = 'milano',
            body = 'test',
            pub_date = in_the_past
        )
        self.view.object = article
        viewname = 'articles:detail'
        kwargs = {'pk': article.pk}
        get_success_url_expected = reverse(viewname, kwargs = kwargs)
        get_success_url_given = self.view.get_success_url()
        self.assertEqual(get_success_url_expected, get_success_url_given)
