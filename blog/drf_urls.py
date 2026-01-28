from rest_framework.routers import DefaultRouter

from blog import drf_views

app_name = "drf-blog"

# trailing_slash=False表示不要結尾的斜線
router = DefaultRouter(trailing_slash=False)
router.register("articles", drf_views.ArticleViewSet)
router.register("authors", drf_views.AuthorViewSet)

urlpatterns = router.urls
