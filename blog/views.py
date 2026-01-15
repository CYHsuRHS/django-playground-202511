from django.contrib import messages

# from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from blog.forms import ArticleForm
from blog.models import Article, Author, Tag


# article_list(request)表示是一個function view
def article_list(request):
    # 從 GET 參數取得篩選條件
    search = request.GET.get("search", "")
    author_id = request.GET.get("author", "")

    # 建立基本 QuerySet
    articles = Article.objects.select_related("author").prefetch_related("tags")

    # 根據搜尋關鍵字篩選標題
    if search:
        articles = articles.filter(title__icontains=search)

    # 根據作者篩選
    if author_id:
        articles = articles.filter(author_id=author_id)

    return render(
        request, "blog/article_list.html", {"articles": articles, "search": search}
    )


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
        messages.success(request, f"文章「{article.title}」已成功建立。")
        return redirect("blog:article_detail", article_id=article.id)
    # 若驗證不合法就直接render畫面
    return render(request, "blog/article_create.html", {"form": form})


def article_edit(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    # 使用者按下save時，並非建立全新的物件，而是更新instance
    form = ArticleForm(request.POST or None, instance=article)
    if form.is_valid():
        article = form.save()
        messages.debug(request, f"文章「{article.title}」已成功更新。")
        messages.info(request, f"文章「{article.title}」已成功更新。")
        messages.warning(request, f"文章「{article.title}」已成功更新。")
        messages.error(request, f"文章「{article.title}」已成功更新。")
        messages.success(request, f"文章「{article.title}」已成功更新。")
        return redirect("blog:article_detail", article_id=article.id)

    return render(request, "blog/article_edit.html", {"form": form, "article": article})


def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})


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
