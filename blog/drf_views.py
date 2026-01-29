from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.viewsets import ModelViewSet

from blog.filters import ArticleFilter
from blog.models import Article, Author
from blog.serializers import ArticleSerializer, AuthorSerializer


class ArticleViewSet(ModelViewSet):
    """文章列表 API"""

    # 代表只有這個ViewSet是使用這個permission，若沒有寫下面這行程式，就表示是使用setting.py設定的permission
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search_fields設定search時要到哪些欄位找
    search_fields = ["title", "content"]
    # ordering_fields設定哪些欄位允許排序
    ordering_fields = ["created_at", "title"]
    # 通常會先寫簡單的篩選
    # filterset_fields = ["is_published", "author"]
    # 也可以寫很複雜的
    # filterset_fields = {
    #     "title": ["exact", "icontains"],
    #     "author": ["exact"],
    #     "tags": ["exact"],
    # }
    # 有需求出現才會回頭寫filterset_class
    filterset_class = ArticleFilter

    def perform_create(self, serializer):
        """在建立物件時設定 created_by"""
        # 為了告訴rest framework的serializer存檔時，請把created_by關聯到它設定的User
        serializer.save(created_by=self.request.user)


class AuthorViewSet(ModelViewSet):
    """作者列表 API"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
