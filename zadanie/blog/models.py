from django.db import models
from django.utils import timezone


def hundred_years_from_now():
    now = timezone.now()
    hundred_years = timezone.timedelta(days=100*365)
    hundred_years_from_now =  now + hundred_years
    return hundred_years_from_now


class PublishedEntryManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        now = timezone.now()
        queryset = queryset.filter(pub_date__lt = now)
        return queryset


class Entry(models.Model):
    title = models.CharField(max_length = 30)
    body = models.TextField(max_length = 1000)
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    pub_date = models.DateTimeField(default = hundred_years_from_now)
    comments_count = models.PositiveSmallIntegerField(default = 0)

    published = PublishedEntryManager()

    class Meta:
        verbose_name_plural = "Entries"
