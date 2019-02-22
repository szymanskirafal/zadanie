from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from django.contrib.auth.models import AnonymousUser

from ..forms import ArticleForm
from ..models import Article
from ..views import (
    ArticleCreateView,
    ArticleCreatedTemplateView,
    ArticleDeleteView,
    ArticleDeletedTemplateView,
    ArticleDetailView,
    ArticlesListView,
    ArticleUpdateView,
)
from utilities.utilities import hundred_years_from_now, yesterday


class TestArticleCreateView(TestCase):

    def setUp(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        self.path = reverse('articles:create')
        self.view = ArticleCreateView()
        self.data_to_post = {
            'title':'Pizza',
            'body':'some text',
            'pub_date': in_the_past.strftime('%Y-%m-%d'),
            }
        self.request = RequestFactory().post(self.path, data = self.data_to_post)

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
        articles = Article.objects.all()
        self.assertEqual(get_success_url_expected, get_success_url_given)

    def test_view_creates_published_instance(self):
        self.assertEqual(Article.objects.count(), 0)
        response = ArticleCreateView.as_view()(self.request)
        articles = Article.objects.all()
        self.assertEqual(Article.published.count(), 1)

    def test_view_returns_expected_code_after_creating_instance(self):
        status_code_expected = 302
        response = ArticleCreateView.as_view()(self.request)
        articles = Article.objects.all()
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_view_creates_not_published_instance(self):
        self.assertEqual(Article.objects.count(), 0)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        data_to_post = self.data_to_post
        data_to_post['pub_date'] = in_the_future.strftime('%Y-%m-%d')
        request = RequestFactory().post(self.path, data = data_to_post)
        response = ArticleCreateView.as_view()(request)
        articles = Article.objects.all()
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

    def setUp(self):
        self.view = ArticleDetailView()
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        article_published_1 = Article.objects.create(
            title = 'firenze',
            body = 'il duomo',
            pub_date = in_the_past,
        )
        self.request = RequestFactory().get('/fake-url')
        pk = article_published_1.pk
        request = self.request
        self.response = ArticleDetailView.as_view()(request, pk = pk)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.DetailView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_context_object_name_attr(self):
        context_object_name_expected = 'article'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(context_object_name_expected, context_object_name_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Article
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'articles/article-detail.html'
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
        template_name_expected = 'articles/article-detail.html'
        template_name_given = self.response.template_name
        self.assertTrue(template_name_expected, template_name_given)

    def test_get_queryset(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        article_published = Article.objects.create(
            title = 'uno_publshed',
            body = 'test',
            pub_date = in_the_past
        )
        article_not_published = Article.objects.create(
            title = 'uno_not_published',
            body = 'test',
            pub_date = in_the_future
        )
        queryset_returned = self.view.get_queryset()
        self.assertIn(article_published, queryset_returned)
        self.assertNotIn(article_not_published, queryset_returned)


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


class TestArticleListView(TestCase):

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
        self.assertEqual(context_object_name_expected, context_object_name_given)

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
        self.assertEqual(context_object_name_expected, context_object_name_given)

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
