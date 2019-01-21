from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path(
        'entries/<int:pk>/',
        views.EntryDetailView.as_view(),
        name = 'entry-detail'),
    path(
        'entries/<int:pk>/update/',
        views.EntryUpdateView.as_view(),
        name = 'entry-update'),
    path(
        'entries/create/',
        views.EntryCreateView.as_view(),
        name = 'entry-create'),
    path(
        'entries/created/',
        views.EntryCreatedTemplateView.as_view(),
        name = 'entry-created'),
    path(
        'entries/',
        views.EntryListView.as_view(),
        name = 'entries'),


]
