# from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import ArticleForm
from blog.models import Article, Author, Tag


# article_list(request)表示是一個function view
def article_list(request):
    # articles = Article.objects.all()  # 把Article這張表的所有物件撈出來放在articles變數
    # 修正作者N+1查詢問題使用select_related，其參數是要載入的關聯欄位名稱，使用SQL LEFT JOIN的技巧，同時把有作者的資料一起撈回來
    # articles = Article.objects.select_related("author").all()
    # 修正標籤N+1查詢問題使用prefetch_related，因關聯方式不同author與tags是多對多
    articles = Article.objects.select_related("author").prefetch_related("tags")
    # 透過render function將articles變數丟到"articles" template裡面，要渲染的畫面是"blog/article_list.html"，並且挾帶articles變數到"articles" template裡
    return render(request, "blog/article_list.html", {"articles": articles})


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
    # article = get_object_or_404(Article, id=article_id)
    article = get_object_or_404(
        Article.objects.select_related("author").prefetch_related("tags"),
        id=article_id,
    )
    print(article)  # 可用於debug，print結果會顯示於PowerShell
    return render(request, "blog/article_detail.html", {"article": article})


def article_create(request):
    # request.POST如果有的話，就產生一個以request.POST為資料需要被驗證的表單，否則給一個None表完全乾淨的表單如同request.GET來建立一個form
    form = ArticleForm(request.POST or None)
    # 若驗證合法就直接存起來
    if form.is_valid():
        article = form.save()
        return redirect("blog:article_detail", article_id=article.id)
    # 若驗證不合法就直接render畫面
    return render(request, "blog/article_create.html", {"form": form})


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 使用者按下save時，並非建立全新的物件，而是更新instance
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "blog/author_list.html", {"authors": authors})


def author_detail(request, author_id):
    # author = Author.objects.get(id=author_id)
    author = get_object_or_404(Author, id=author_id)
    return render(request, "blog/author_detail.html", {"author": author})


def tag_list(request):
    # tags = Tag.objects.all()
    # tags修正N+1查詢問題不可使用select_related，因關聯的方式不一樣
    tags = Tag.objects.prefetch_related("articles").all()
    return render(request, "blog/tag_list.html", {"tags": tags})
