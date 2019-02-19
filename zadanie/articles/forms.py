from django.forms import ModelForm

from .models import Article


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = [
            'title',
            'body',
            'pub_date',
        ]
