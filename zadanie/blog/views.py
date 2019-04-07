from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from comments.forms import CommentForm
from comments.models import Comment

from .forms import EntryForm
from .models import Entry


class EntryCreateView(generic.CreateView):
    form_class = EntryForm
    model = Entry
    success_url = '/blog/entries/created/'
    template_name = 'blog/entry-create.html'


class EntryCreatedTemplateView(generic.TemplateView):
    template_name = 'blog/entry-created.html'


class EntryDeleteView(generic.DeleteView):
    form_class = EntryForm
    model = Entry
    success_url = '/blog/entries/deleted/'
    template_name = 'blog/entry-delete.html'


class EntryDeletedTemplateView(generic.TemplateView):
    template_name = 'blog/entry-deleted.html'


class EntryDetailView(View):

    def get(self, request, *args, **kwargs):
        view = EntryDetailJustDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EntryDetailAddCommentView.as_view()
        return view(request, *args, **kwargs)


class EntryDetailJustDisplayView(generic.DetailView):
    context_object_name = 'entry'
    queryset = Entry.published
    template_name = 'blog/entry-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class EntryDetailAddCommentView(
    generic.detail.SingleObjectMixin,
    generic.FormView,
):

    form_class = CommentForm
    queryset = Entry.published
    template_name = 'blog/entry-detail.html'

    def form_valid(self, form):
        body = form.cleaned_data['body']
        Comment.objects.create(
            content_object = self.get_object(),
            body = body,
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        viewname = 'blog:entry-detail'
        obj = self.get_object()
        kwargs = {'pk': obj.pk}
        success_url = reverse(viewname, kwargs = kwargs)
        return success_url

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class EntryListView(generic.ListView):
    context_object_name = 'entries'
    model = Entry
    template_name = 'blog/entries.html'

    def get_queryset(self):
        queryset = Entry.published.all()
        return queryset


class EntryUpdateView(generic.UpdateView):
    context_object_name = 'entry'
    form_class = EntryForm
    model = Entry
    template_name = 'blog/entry-update.html'

    def get_success_url(self):
        viewname = 'blog:entry-detail'
        kwargs = {'pk': self.object.pk}
        success_url = reverse(viewname, kwargs = kwargs)
        return success_url
