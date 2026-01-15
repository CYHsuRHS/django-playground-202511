import django_filters

from blog.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            "title": ["icontains"],
            "author": ["exact"],
        }
