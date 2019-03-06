from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from comments.forms import CommentForm
from comments.models import Comment

from .forms import ArticleForm
from .models import Article

class ArticleCreateView(generic.CreateView):
    form_class = ArticleForm
    model = Article
    success_url = '/articles/created/'
    template_name = 'articles/article-create.html'


class ArticleCreatedTemplateView(generic.TemplateView):
    template_name = 'articles/article-created.html'


class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        view = ArticleDetailJustDisplayView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ArticleDetailAddCommentView.as_view()
        return view(request, *args, **kwargs)


class ArticleDetailJustDisplayView(generic.DetailView):
    context_object_name = 'article'
    model = Article
    queryset = Article.published
    template_name = 'articles/article-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context


class ArticleDetailAddCommentView(generic.detail.SingleObjectMixin, generic.FormView):
    form_class = CommentForm
    model = Article
    queryset = Article.published
    template_name = 'articles/article-detail.html'

    def form_valid(self, form):
        body = form.cleaned_data['body']
        Comment.objects.create(
            content_object = self.object,
            body = body,
        )
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        viewname = 'articles:detail'
        kwargs = {'pk': self.object.pk}
        success_url = reverse(viewname, kwargs = kwargs)
        return success_url


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
    queryset = Article.published
    template_name = 'articles/articles.html'


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
