from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import EntryForm
from .models import Entry

"""



class EntryDeleteView(generic.DeleteView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-delete.html'






"""
class EntryCreateView(generic.CreateView):
    form_class = EntryForm
    model = Entry
    success_url = reverse_lazy('blog:entries')
    template_name = 'blog/entry-create.html'


class EntryDetailView(generic.DetailView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-detail.html'


class EntryListView(generic.ListView):
    context_object_name = 'entries'
    model = Entry
    template_name = 'blog/entries.html'


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
