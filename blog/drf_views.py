from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.models import Article, Author
from blog.serializers import ArticleSerializer, AuthorSerializer


class ArticleListAPIView(ListCreateAPIView):
    """文章列表 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        """在建立物件時設定 created_by"""
        # 為了告訴rest framework的serializer存檔時，請把created_by關聯到它設定的User
        serializer.save(created_by=self.request.user)


class ArticleDetailAPIView(RetrieveUpdateDestroyAPIView):
    """文章詳情 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class AuthorListAPIView(ListCreateAPIView):
    """作者列表 API"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetailAPIView(RetrieveUpdateDestroyAPIView):
    """作者詳情 API"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
