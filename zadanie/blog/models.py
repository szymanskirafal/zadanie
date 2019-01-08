from django.db import models
from django.utils.timezone import now



class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(pub_date__lt = now)


class Entry(models.Model):
    title = models.CharField(max_length = 30)
    body = models.TextField(max_length = 1000)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    pub_date = models.DateTimeField(blank = True)
    comments_count = models.PositiveSmallIntegerField(default = 0)

    published = PublishedEntryManager()
