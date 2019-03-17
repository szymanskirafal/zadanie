from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from django.contrib.auth.models import AnonymousUser

from utilities.utilities import hundred_years_from_now, yesterday

from ..forms import EntryForm
from ..models import Entry
from ..views import (
    EntryCreateView,
    EntryCreatedTemplateView,
    EntryDeleteView,
    EntryDeletedTemplateView,
    EntryDetailView,
    EntryListView,
    EntryUpdateView,
)


class TestEntryListView(TestCase):

    def setUp(self):
        self.view = EntryListView()
        self.request = RequestFactory().get('/fake-url')
        self.response = EntryListView.as_view()(self.request)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.ListView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_context_object_name_attr(self):
        context_object_name_expected = 'entries'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(context_object_name_expected, context_object_name_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Entry
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'blog/entries.html'
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
        template_name_expected = 'blog/entries.html'
        template_name_given = self.response.template_name
        self.assertTrue(template_name_expected, template_name_given)

    def test_get_queryset(self):
        in_the_past = timezone.now() - timezone.timedelta(days = 1)
        in_the_future = timezone.now() + timezone.timedelta(days = 1)
        entry_published = Entry.objects.create(
            title = 'Genoa',
            body = 'published',
            pub_date = in_the_past,
        )
        entry_not_published = Entry.objects.create(
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


class TestEntryListViewResponse(TestCase):

    def setUp(self):
        self.entry_not_published = Entry.objects.create(
            title = 'uno',
            body = 'test'
        )
        self.entry_published_1 = Entry.objects.create(
            title = 'due',
            body = 'test',
            pub_date = yesterday()
        )
        self.entry_published_2 = Entry.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = yesterday()
        )
        url = reverse('blog:entries')
        self.response = self.client.get(url)
        self.entries_in_the_view = self.response.context.get('entries', None)

    def test_not_published_entries_not_in_the_view(self):
        condition = self.entry_not_published not in self.entries_in_the_view
        self.assertTrue(condition)

    def test_published_entries_only_in_the_view(self):
        condition_1 = self.entry_published_1 in self.entries_in_the_view
        condition_2 = self.entry_published_2 in self.entries_in_the_view
        self.assertTrue(condition_1 and condition_2)

    def test_correct_number_of_entries_are_in_the_view(self):
        number_of_entries_published = 2
        number_of_entries_in_the_view = len(self.entries_in_the_view)
        condition = number_of_entries_published == number_of_entries_in_the_view
        self.assertTrue(condition)

    def test_template_used(self):
        response = self.response
        template_name = 'blog/entries.html'
        self.assertTemplateUsed(response, template_name)

    def test_correct_text_in_response(self):
        response = self.response
        text1 = self.entry_published_1.title
        text2 = self.entry_published_2.title
        self.assertContains(response, text1)
        self.assertContains(response, text2)

    def test_not_expected_text_not_in_response(self):
        response = self.response
        text1 = self.entry_published_1.body
        text2 = self.entry_not_published.title
        self.assertNotContains(response, text1)
        self.assertNotContains(response, text2)

class TestEntryDeleteView(TestCase):

    def setUp(self):
        url = '/fake-url'
        self.request = RequestFactory().get(url)
        self.view = EntryDeleteView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.DeleteView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_template(self):
        template_name_expected = 'blog/entry-delete.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_view_uses_correct_success_url(self):
        success_url_expected = '/blog/entries/deleted/'
        success_url_given = self.view.success_url
        self.assertEqual(success_url_expected, success_url_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Entry
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_status_code(self):
        status_code_expected = 200
        entry_published_1 = Entry.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = yesterday()
        )
        pk = entry_published_1.pk
        request = self.request
        view = self.view.__class__.as_view()
        response = view(request, pk = pk)
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)


class TestEntryDetailViewConstruction(TestCase):

    def setUp(self):
        self.view = EntryDetailView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.DetailView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_attrs(self):
        self.assertEqual(self.view.context_object_name, 'entry')
        self.assertEqual(self.view.model, Entry)
        self.assertEqual(self.view.template_name, 'blog/entry-detail.html')


class TestEntryDetailViewResponse(TestCase):

    def setUp(self):
        entry_published_1 = Entry.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = yesterday()
        )
        self.request = RequestFactory().get('/fake-url')
        pk = entry_published_1.pk
        request = self.request
        self.response = EntryDetailView.as_view()(request, pk = pk)

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
        self.request.template_name = 'blog/entry-detail.html'
        template_name_expected = 'blog/entry-detail.html'
        template_name_given = self.response.template_name
        self.assertTrue(template_name_expected, template_name_given)



class TestEntryDetailViewResponseClient(TestCase):

    def setUp(self):
        self.entry_not_published = Entry.objects.create(
            title = 'uno',
            body = 'test'
        )
        self.entry_published_1 = Entry.objects.create(
            title = 'due',
            body = 'test',
            pub_date = yesterday()
        )
        kwargs = {'pk': self.entry_published_1.pk}
        path = reverse('blog:entry-detail', kwargs = kwargs)
        self.response = self.client.get(path)
        self.entry_in_the_view = self.response.context.get('entry', None)

    def test_not_published_entries_not_in_the_view(self):
        condition = self.entry_not_published != self.entry_in_the_view
        self.assertTrue(condition)

    def test_published_entry_only_in_the_view(self):
        condition = self.entry_published_1 == self.entry_in_the_view
        self.assertTrue(condition)

    def test_template_used(self):
        response = self.response
        template_name = 'blog/entry-detail.html'
        self.assertTemplateUsed(response, template_name)

    def test_correct_text_in_response(self):
        response = self.response
        text = self.entry_published_1.title
        self.assertContains(response, text)

    def test_not_expected_text_not_in_response(self):
        response = self.response
        text = self.entry_not_published.title
        self.assertNotContains(response, text)


class TestEntryCreateViewConstruction(TestCase):

    def setUp(self):
        self.path = reverse('blog:entry-create')
        self.view = EntryCreateView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.CreateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_form_class(self):
        form_class_expected = EntryForm
        form_class_given = self.view.form_class
        self.assertEqual(form_class_expected, form_class_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Entry
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'blog/entry-create.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_get_success_url(self):
        entry = Entry.objects.create(
            title = 'due',
            body = 'test',
            pub_date = yesterday()
        )
        self.view.object = entry
        viewname = 'blog:entry-created'
        get_success_url_expected = reverse(viewname)
        get_success_url_given = self.view.get_success_url()
        self.assertEqual(get_success_url_expected, get_success_url_given)


class TestEntryCreateViewResponse(TestCase):

    def setUp(self):
        self.data_to_post = {
            'title':'Pizza',
            'body':'some text',
            'pub_date': yesterday().strftime('%Y-%m-%d'),
            }
        self.path = reverse('blog:entry-create')
        self.request = RequestFactory().post(self.path, data = self.data_to_post)
        self.view = EntryCreateView.as_view()

    def test_view_creates_published_instance(self):
        self.assertEqual(Entry.objects.count(), 0)
        self.view(self.request)
        self.assertEqual(Entry.published.count(), 1)

    def test_view_returns_code_after_creating_instance(self):
        status_code_expected = 302
        response = self.view(self.request)
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_view_creates_published_instance(self):
        response = self.view(self.request)
        entry = Entry.objects.last()
        title_expected = entry.title
        title_given = self.data_to_post.get('title', None)
        self.assertEqual(title_expected, title_given)
        body_expected = entry.body
        body_given = self.data_to_post.get('body', None)
        self.assertEqual(body_expected, body_given)
        self.assertEqual(Entry.published.count(), 1)

    def test_view_creates_not_published_instance(self):
        self.assertEqual(Entry.objects.count(), 0)
        path = self.path
        data_to_post = self.data_to_post
        data_to_post['pub_date'] = hundred_years_from_now().strftime('%Y-%m-%d')
        request = RequestFactory().post(path, data = data_to_post)
        view = self.view
        response = view(request)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(Entry.published.count(), 0)
        self.assertEqual(response.status_code, 302)



class TestEntryCreatedTemplateView(TestCase):

    def setUp(self):
        factory = RequestFactory()
        url = '/fake-url'
        request = factory.get(url)
        self.view = EntryCreatedTemplateView()
        self.response = EntryCreatedTemplateView.as_view()(request)

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.TemplateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_template_name_attr(self):
        template_name_expected = 'blog/entry-created.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_view_uses_correct_template(self):
        template_name_expected = ['blog/entry-created.html']
        template_name_given = self.response.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_status_code(self):
        status_code_expected = 200
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)


class TestEntryUpdateView(TestCase):

    def setUp(self):
        self.view = EntryUpdateView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.UpdateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_has_correct_context_object_name_attr(self):
        context_object_name_expected = 'entry'
        context_object_name_given = self.view.context_object_name
        self.assertEqual(context_object_name_expected, context_object_name_given)

    def test_view_uses_correct_form_class(self):
        form_class_expected = EntryForm
        form_class_given = self.view.form_class
        self.assertEqual(form_class_expected, form_class_given)

    def test_view_refers_to_correct_model_class(self):
        model_class_expected = Entry
        model_class_given = self.view.model
        self.assertEqual(model_class_expected, model_class_given)

    def test_view_has_correct_template_name_attr(self):
        template_name_expected = 'blog/entry-update.html'
        template_name_given = self.view.template_name
        self.assertEqual(template_name_expected, template_name_given)

    def test_get_success_url(self):
        entry_published_1 = Entry.objects.create(
            title = 'due',
            body = 'test',
            pub_date = yesterday()
        )
        self.view.object = entry_published_1
        viewname = 'blog:entry-detail'
        kwargs = {'pk': entry_published_1.pk}
        get_success_url_expected = reverse(viewname, kwargs = kwargs)
        get_success_url_given = self.view.get_success_url()
        self.assertEqual(get_success_url_expected, get_success_url_given)

    def test_view_updates_field(self):
        entry = Entry.objects.create(
            title="Vernazza",
            body="nothing special",
        )
        field_value_before_update = entry.title
        viewname = 'blog:entry-update'
        kwargs = {'pk': entry.pk}
        path = reverse(viewname, kwargs = kwargs)
        data_to_post = {
            'title':'Pizza',
            'body':'some text',
            'pub_date':'2000-11-11',
        }
        response = self.client.post(path, data = data_to_post)
        self.assertEqual(response.status_code, 302)
        entry.refresh_from_db()
        field_value_after_update = entry.title
        field_value_changed_to = data_to_post.get('title', None)
        self.assertNotEqual(field_value_before_update, field_value_after_update)
        self.assertEqual(field_value_changed_to, field_value_after_update)
