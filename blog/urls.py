from django.urls import path

from blog import views

urlpatterns = [
    path("articles/", views.article_list, name="article_list"),
    # "articles/<int:article_id>/"表path會帶article_id並且其型態為int
    path("articles/<int:article_id>/", views.article_detail, name="article_detail"),
    path("authors/", views.author_list, name="author_list"),
    path("authors/<int:author_id>/", views.author_detail, name="author_detail"),
    path("tags/", views.tag_list, name="tag_list"),
]
