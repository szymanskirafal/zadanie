from django.test import RequestFactory, TestCase
from django.views import generic
from django.urls import reverse

from django.contrib.auth.models import AnonymousUser

from ..forms import EntryForm
from ..models import Entry
from ..views import EntryCreateView, EntryDetailView, EntryListView, EntryUpdateView
from ..utils import yesterday


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


class TestEntryListViewFactoried(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/blog/entries/')
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
        self.entries_in_the_view = self.response.context['entries']

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

    def test_number_of_queries(self):
        entries = Entry.published.all()
        for e in entries:
            print(e)

        print('________  num  __________________')
        self.assertNumQueries(1)
        print('________  num  __________________')


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
        entry = Entry.objects.create(title = 'uno', body = 'some text')
        view_name = 'blog:entry-detail'
        kwargs = {'pk': entry.pk}
        url = reverse(view_name, kwargs = kwargs)
        self.response = self.client.get(url)
"""
    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'blog/entry-detail.html')
"""
"""
    def test_status_code(self):
        status_code_expected = 200
        status_code_given = self.response.status_code
        self.assertEqual(status_code_expected, status_code_given)
"""
"""
    def test_object_in_context(self):
        self.assertIn('entry', self.response.context)
"""
