from django.urls import path

from . import views

app_name = 'articles'
urlpatterns = [
    path(
        '',
        views.ArticlesListView.as_view(),
        name = 'list'),
    path(
        'create/',
        views.ArticleCreateView.as_view(),
        name = 'create'),
    path(
        'created/',
        views.ArticleCreatedTemplateView.as_view(),
        name = 'created'),
    path(
        '<int:pk>/',
        views.ArticleDetailView.as_view(),
        name = 'detail'),
    path(
        '<int:pk>/delete/',
        views.ArticleDeleteView.as_view(),
        name = 'delete'),
    path(
        'deleted/',
        views.ArticleDeletedTemplateView.as_view(),
        name = 'deleted'),
    path(
        '<int:pk>/update/',
        views.ArticleUpdateView.as_view(),
        name = 'update'),



]
