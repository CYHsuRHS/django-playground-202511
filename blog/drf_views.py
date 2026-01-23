# drf_views.py命名是為了與另一個api區隔，一般建立api，可以直接命名為views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView


# 只接受GET與POST方法，其他不接受
@api_view(["GET", "POST"])
def article_list(request):
    """文章列表 API"""
    if request.method == "GET":
        return Response({"message": "文章列表"})
    elif request.method == "POST":
        return Response({"message": "新增文章"}, status=201)


class ArticleListAPIView(APIView):
    """文章列表 API"""

    def get(self, request):
        return Response({"message": "文章列表"})

    def post(self, request):
        return Response({"message": "新增文章"}, status=201)


@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk):
    """文章詳情 API"""
    if request.method == "GET":
        return Response({"message": f"取得文章 {pk}"})
    elif request.method == "PUT":
        return Response({"message": f"更新文章 {pk}"})
    elif request.method == "DELETE":
        return Response({"message": f"刪除文章 {pk}"}, status=204)


class ArticleDetailAPIView(APIView):
    """文章詳情 API"""

    # 沒有寫post會自動知道不提供post
    def get(self, request, pk):
        return Response({"message": f"取得文章 {pk}"})

    def put(self, request, pk):
        return Response({"message": f"更新文章 {pk}"})

    def delete(self, request, pk):
        return Response({"message": f"刪除文章 {pk}"}, status=204)
