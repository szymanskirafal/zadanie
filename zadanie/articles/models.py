from django.db import models
from django.urls import reverse
from django.utils import timezone

from blog.utils import hundred_years_from_now


class PublishedArticleManager(models.Manager):

    def get_queryset(self):
        now = timezone.now()
        queryset = super().get_queryset()
        queryset = queryset.filter(pub_date__lt = now)
        return queryset


class Article(models.Model):
    title = models.CharField(max_length = 30)
    body = models.TextField(max_length = 1000, default = 'some text')
    created = models.DateTimeField(auto_now_add = True)
    modified = models.DateTimeField(auto_now = True)
    pub_date = models.DateTimeField(default = hundred_years_from_now)
    comments_count = models.PositiveSmallIntegerField(default = 0)

    objects = models.Manager()
    published = PublishedArticleManager()

    class Meta:
        ordering = ['-modified']
        verbose_name_plural = "Entries"

    def __str__(self):
        return self.title
"""
    def get_absolut_url(self):
        viewname = 'articles:article-detail'
        kwargs = {'pk': self.id}
        absolut_url = reverse(viewname, kwargs = kwargs)
        return absolut_url
"""