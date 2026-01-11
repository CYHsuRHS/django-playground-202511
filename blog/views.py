# from django.http import Http404
from django.shortcuts import get_object_or_404, render

from blog.models import Article, Author, Tag


# article_list(request)表示是一個function view
def article_list(request):
    articles = Article.objects.all()  # 把Article這張表的所有物件撈出來放在articles變數
    return render(
        request, "blog/article_list.html", {"articles": articles}
    )  # 透過render function將articles變數丟到"articles" template裡面，要渲染的畫面是"blog/article_list.html"，並且挾帶articles變數到"articles" template裡


# 原始處裡DoesNotExist問題寫法，需使用try-except
# def article_detail(request, article_id):
#     try:
#         article = Article.objects.get(id=article_id)
#     except Article.DoesNotExist:
#         raise Http404

#     return render(request, "blog/article_detail.html", {"article": article})


# 用path傳進來的article_id去尋找該篇文章存不存在
def article_detail(request, article_id):
    # get_object_or_404可以給一個queryset或是一個model，目前是給Article這個model，並使用article_id去搜尋，找得到就給物件，找不到就給404
    article = get_object_or_404(Article, id=article_id)
    return render(request, "blog/article_detail.html", {"article": article})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


def author_detail(request, author_id):
    # author = Author.objects.get(id=author_id)
    author = get_object_or_404(Author, id=author_id)
    return render(request, "blog/author_detail.html", {"author": author})


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "blog/tag_list.html", {"tags": tags})
