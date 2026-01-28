from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from blog.models import Article, Author
from blog.serializers import ArticleSerializer, AuthorSerializer


class ArticleListAPIView(GenericAPIView):
    """文章列表 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request):
        # 使用get_queryset()方便覆寫
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 出現data=表示不知道這批資料是否乾淨，請你幫我做驗證，如果是拿payload就使用request.data拿就好
        serializer = self.get_serializer(data=request.data)
        # 若傳入的資料都是乾淨且可被使用
        if serializer.is_valid():
            # 呼叫save，序列化自己會判斷要呼叫新增或更新模式，如果只給data沒有instance代表沒有東西要更新，就會呼叫建立
            serializer.save(created_by=request.user)  # save時還可以額外給created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 若不合法要把serializer.errors告訴前端
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(GenericAPIView):
    """文章詳情 API"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, pk):
        # 不用傳pk，它會自己找
        article = self.get_object()
        serializer = self.get_serializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object()
        serializer = self.get_serializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object()
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorListAPIView(GenericAPIView):
    """作者列表 API"""

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request):
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
