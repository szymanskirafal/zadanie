from django.views import generic

from .models import Entry

"""
class EntryCreateView(generic.CreateView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-create.html'


class EntryDeleteView(generic.DeleteView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-delete.html'





class EntryUpdatelView(generic.UpdateView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-update.html'
"""
class EntryDetailView(generic.DetailView):
    context_object_name = 'entry'
    model = Entry
    template_name = 'blog/entry-detail.html'


    
class EntryListView(generic.ListView):
    context_object_name = 'entries'
    model = Entry
    template_name = 'blog/entries.html'
