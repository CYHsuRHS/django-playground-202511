from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    path("articles/create/", views.article_create, name="article_create"),
    # "articles/<int:article_id>/"表path會帶article_id並且其型態為int
    # path("articles/<int:article_id>/", views.article_detail, name="article_detail"),
    # 只要符合Django預期的命名方式即可
    # path("articles/<int:pk>/", views.ArticleDetailView.as_view(), name="article_detail"),
    path(
        "articles/<int:article_id>/",
        views.ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path("articles/<int:article_id>/edit/", views.article_edit, name="article_edit"),
    path(
        "articles/<int:article_id>/delete/", views.article_delete, name="article_delete"
    ),
    path(
        "articles/bulk-delete/", views.article_bulk_delete, name="article_bulk_delete"
    ),
    path("authors/", views.author_list, name="author_list"),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path("tags/", views.tag_list, name="tag_list"),
]
