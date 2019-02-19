from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import ArticleForm
from .models import Article

class ArticleCreateView(generic.CreateView):
    form_class = ArticleForm
    model = Article
    success_url = '/articles/created/'
    template_name = 'articles/article-create.html'


class ArticleCreatedTemplateView(generic.TemplateView):
    template_name = 'articles/article-created.html'


class ArticleDetailView(generic.DetailView):
    context_object_name = 'article'
    model = Article
    template_name = 'articles/article-detail.html'

    def get_queryset(self):
        self.queryset = Article.published.all()
        queryset = super().get_queryset()
        return queryset

class ArticleDeleteView(generic.DeleteView):
    form_class = ArticleForm
    model = Article
    success_url = '/articles/deleted/'
    template_name = 'articles/article-delete.html'

class ArticleDeletedTemplateView(generic.TemplateView):
    template_name = 'articles/article-deleted.html'

class ArticlesListView(generic.ListView):
    context_object_name = 'articles'
    model = Article
    template_name = 'articles/articles.html'

    def get_queryset(self):
        self.queryset = Article.published.all()
        queryset = super().get_queryset()
        return queryset

class ArticleUpdateView(generic.UpdateView):
    context_object_name = 'article'
    form_class = ArticleForm
    model = Article
    template_name = 'articles/article-update.html'

    def get_success_url(self):
        viewname = 'articles:detail'
        kwargs = {'pk': self.object.pk}
        success_url = reverse(viewname, kwargs = kwargs)
        return success_url
