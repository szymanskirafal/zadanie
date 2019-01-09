from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path(
        route = 'entries/<int:pk>/',
        view = views.EntryDetailView.as_view(),
        name = 'entry-detail'),
    path(
        route = 'entries/',
        view = views.EntryListView.as_view(),
        name = 'entries'),




]
