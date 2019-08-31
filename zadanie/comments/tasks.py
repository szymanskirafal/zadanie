from celery import task

from django.apps import apps
from django.db.models import F

from articles.models import Article
from blog.models import Entry

from .models import Comment

@task
def increase_comments_count(app_name, model_name, pk):
    model_class = apps.get_model(app_name, model_name)
    object_instance = model_class.objects.get(pk = pk)
    object_instance.comments_count = F('comments_count') + 1
    return object_instance.save()
