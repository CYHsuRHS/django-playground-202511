from rest_framework.viewsets import ModelViewSet

from blog.models import Article, Author
from blog.serializers import ArticleSerializer, AuthorSerializer


class ArticleViewSet(ModelViewSet):
    """文章列表 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """在建立物件時設定 created_by"""
        # 為了告訴rest framework的serializer存檔時，請把created_by關聯到它設定的User
        serializer.save(created_by=self.request.user)


class AuthorViewSet(ModelViewSet):
    """作者列表 API"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
