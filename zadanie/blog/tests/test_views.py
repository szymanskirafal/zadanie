from django.test import RequestFactory, TestCase
from django.urls import reverse, reverse_lazy
from django.views import generic

from django.contrib.auth.models import AnonymousUser

from ..forms import EntryForm
from ..models import Entry
from ..views import EntryCreateView, EntryCreatedTemplateView, EntryDetailView, EntryListView, EntryUpdateView
from ..utils import hundred_years_from_now, yesterday


class TestEntryListViewConstruction(TestCase):

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.ListView
        view = EntryListView()
        class_given = view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_attrs(self):
        view = EntryListView()
        self.assertEqual(view.context_object_name, 'entries')
        self.assertEqual(view.model, Entry)
        self.assertEqual(view.template_name, 'blog/entries.html')


class TestAsEntryListViewWithRequestFactory(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake-url')
        self.request.template_name = 'blog/entries.html'
        self.response = EntryListView.as_view()(self.request)

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



class TestEntryDetailViewWithRequestFactory(TestCase):

    def setUp(self):
        self.entry_published_1 = Entry.objects.create(
            title = 'tre',
            body = 'test',
            pub_date = yesterday()
        )
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake-url')
        self.request.template_name = 'blog/entry-detail.html'
        self.response = EntryDetailView.as_view()(
            self.request,
            pk = self.entry_published_1.pk
        )

    def test_status_code(self):
        status_code_expected = 200
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_status_code_for_anonymous_user(self):
        status_code_expected = 200
        request = self.request
        request.user = AnonymousUser()
        response = EntryDetailView.as_view()(
            request,
            pk = self.entry_published_1.pk
        )
        status_code_given = response.status_code
        self.assertEqual(status_code_expected, status_code_given)

    def test_template_used(self):
        template_name_expected = 'blog/entry-detail.html'
        template_name_given = self.response.template_name
        self.assertTrue(template_name_expected, template_name_given)



class TestEntryDetailViewResponse(TestCase):

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
        self.view = EntryCreateView()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.CreateView
        class_given = self.view.__class__.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_attrs(self):
        self.assertEqual(self.view.form_class, EntryForm)
        self.assertEqual(self.view.model, Entry)
        self.assertEqual(self.view.success_url, reverse('blog:entry-created'))
        self.assertEqual(self.view.template_name, 'blog/entry-create.html')



class TestEntryCreatedTemplateView(TestCase):

    def setUp(self):
        factory = RequestFactory()
        url = '/fake-url'
        self.request = factory.get(url)
        self.view = EntryCreatedTemplateView.as_view()

    def test_view_inherits_from_correct_class(self):
        class_expected = generic.TemplateView
        class_given = self.view.view_class.__base__
        self.assertEqual(class_expected, class_given)

    def test_view_uses_correct_template(self):
        response = self.view(self.request)
        template_name_expected = ['blog/entry-created.html']
        template_name_given = response.template_name
        self.assertEqual(template_name_expected, template_name_given)



class TestEntryCreateView(TestCase):

    def setUp(self):
        self.data = {'title':'Pizza', 'body':'some text',}

    def test_view_creates_instance(self):
        self.assertEqual(Entry.objects.count(), 0)
        path = reverse('blog:entry-create')
        self.data['pub_date'] = yesterday().strftime('%Y-%m-%d')
        response = self.client.post(path, data = self.data)
        self.assertEqual(Entry.objects.last().title, self.data.get('title', None))
        self.assertEqual(Entry.objects.last().body, self.data.get('body', None))
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_view_creates_published_instance(self):
        self.assertEqual(Entry.objects.count(), 0)
        path = reverse('blog:entry-create')
        self.data['pub_date'] = yesterday().strftime('%Y-%m-%d')
        response = self.client.post(path, data = self.data)
        self.assertEqual(Entry.published.last().title, self.data.get('title', None))
        self.assertEqual(Entry.published.last().body, self.data.get('body', None))
        self.assertEqual(Entry.published.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_view_creates_not_published_instance(self):
        self.assertEqual(Entry.objects.count(), 0)
        path = reverse('blog:entry-create')
        self.data['pub_date'] = hundred_years_from_now().strftime('%Y-%m-%d')
        response = self.client.post(path, data = self.data)
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(Entry.published.count(), 0)
        self.assertEqual(Entry.objects.last().title, self.data.get('title', None))
        self.assertEqual(Entry.objects.last().body, self.data.get('body', None))
        self.assertEqual(response.status_code, 302)


class TestEntryUpdateView(TestCase):

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
