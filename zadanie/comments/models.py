from django.db import models

class Comment(models.Model):
    body = models.TextField(max_length = 300, default = 'some comment')
    created = models.DateTimeField(auto_now_add = True)
