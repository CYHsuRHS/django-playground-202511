from django.shortcuts import render

from blog.models import Article, Author, Tag


# article_list(request)表示是一個function view
def article_list(request):
    articles = Article.objects.all()  # 把Article這張表的所有物件撈出來放在articles變數
    return render(
        request, "blog/article_list.html", {"articles": articles}
    )  # 透過render function將articles變數丟到"articles" template裡面，要渲染的畫面是"blog/article_list.html"，並且挾帶articles變數到"articles" template裡


# 用path傳進來的article_id去尋找該篇文章存不存在
def article_detail(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, "blog/article_detail.html", {"article": article})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, "blog/author_detail.html", {"author": author})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "blog/tag_list.html", {"tags": tags})
