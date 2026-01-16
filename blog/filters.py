import django_filters

from blog.models import Article


class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            "title": ["exact", "icontains"],  # 可針對同一個欄位做不同的篩選
            "author": ["exact"],
            "tags": ["exact"],
        }
