from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Article
from blog.serializers import ArticleSerializer


class ArticleListAPIView(APIView):
    """文章列表 API"""

    def get(self, request):
        # 取得所有文章
        articles = Article.objects.all()
        # 將資料丟入序列化當中，若沒有下many=True，它會理解articles裡面只有一筆資料，many=True時，它會把articles裡每篇文章都用序列化過濾，故無需定義list
        # 使用articles表知道資料是乾淨的，請轉為json
        serializer = ArticleSerializer(articles, many=True)
        # 將serializer.data序列過的資料回應給使用者
        return Response(serializer.data)

    def post(self, request):
        # 出現data=表示不知道這批資料是否乾淨，請你幫我做驗證，如果是拿payload就使用request.data拿就好
        serializer = ArticleSerializer(data=request.data)
        # 若傳入的資料都是乾淨且可被使用
        if serializer.is_valid():
            # 呼叫save，序列化自己會判斷要呼叫新增或更新模式，如果只給data沒有instance代表沒有東西要更新，就會呼叫建立
            serializer.save(created_by=request.user)  # save時還可以額外給created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 若不合法要把serializer.errors告訴前端
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailAPIView(APIView):
    """文章詳情 API"""

    # 將最核心的邏輯抽出
    def get_object(self, pk):
        return Article.objects.get(pk=pk)

    def get(self, request, pk):
        # 用try...except包住，處理文章不存在的情況
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            # 先取得物件
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        # 用序列化過濾使用者傳進來的資料request.data，額外給article這個instance
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()  # serializer有instance就會呼叫update的方法
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            article = self.get_object(pk)
        except Article.DoesNotExist:
            return Response(
                {"detail": "找不到該文章"}, status=status.HTTP_404_NOT_FOUND
            )
        article.delete()
        # 回傳204，表示你刪除成功了，但我沒有訊息要告訴你
        return Response(status=status.HTTP_204_NO_CONTENT)
