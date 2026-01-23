from django.urls import path

from blog import drf_views

app_name = "drf-blog"

urlpatterns = [
    # REST API設計URL慣例在資源後不加斜線
    # path("articles", drf_views.article_list, name="article-list"),
    path("articles", drf_views.ArticleListAPIView.as_view(), name="article-list"),
    # path("articles/<int:pk>", drf_views.article_detail, name="article-detail"),
    path(
        "articles/<int:pk>",
        drf_views.ArticleDetailAPIView.as_view(),
        name="article-detail",
    ),
]
