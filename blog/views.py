from django.contrib import messages

# from django.contrib.auth.decorators import login_required
# 沒登入不可能有權限，所以可使用permission_required替換login_required
from django.contrib.auth.decorators import permission_required

# from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from blog.filters import ArticleFilter
from blog.forms import ArticleForm
from blog.models import Article, Author, Tag


# article_list(request)表示是一個function view
def article_list(request):
    # 在python的世界裡filter這個名稱已經被內建的函式使用了，若命名為filter將會把其函式覆蓋
    filter_ = ArticleFilter(
        request.GET or None,  # 像初始化form的方式一樣初始化它
        queryset=Article.objects.select_related("author").prefetch_related("tags"),
    )
    # filter轉換到前端沒有使用底線
    return render(request, "blog/article_list.html", {"filter": filter_})


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


# @login_required
@permission_required("blog.add_article", raise_exception=True)
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


# @login_required
@permission_required("blog.change_article", raise_exception=True)
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


# @login_required
@permission_required("blog.delete_article", raise_exception=True)
def article_delete(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        article.delete()
        messages.success(request, f"文章「{article.title}」已成功刪除。")
        return redirect("blog:article_list")

    return render(request, "blog/article_delete.html", {"article": article})


# def article_bulk_delete(request):
#     if request.method == "POST":
#         article_ids = request.POST.getlist("article_ids")
#         if article_ids:
#             # 如果article_ids有東西做的動作
#             # in表示只要在丟給你的article_ids列表裡面都要找到
#             # a = Article.objects.filter(id__in=article_ids)
#             # print(a)
#             # .delete()會回傳兩個東西給你
#             # a, b = Article.objects.filter(id__in=article_ids).delete()
#             # print(a) 會得到總共刪除幾篇文章
#             # print(b) ['blog:Article':1]在各個model各刪多少,告知連帶刪除的東西
#             # 知道有回傳值，但沒有要使用的參數，使用底線_接，這是python約定成俗的慣例
#             deleted_count, _ = Article.objects.filter(id__in=article_ids).delete()
#             messages.success(request, f"已成功刪除 {deleted_count} 篇文章")
#         else:
#             messages.warning(request, "請先選取至少一個要刪除的文章")
#     return redirect("blog:article_list")


# @login_required
@permission_required("blog.delete_article", raise_exception=True)
def article_bulk_delete(request):
    # 第一步：從列表頁送來 → 顯示確認頁
    if request.method == "POST" and "confirm" not in request.POST:
        article_ids = request.POST.getlist("article_ids")

        if not article_ids:
            messages.warning(request, "請先選取至少一個要刪除的文章")
            return redirect("blog:article_list")

        articles = Article.objects.filter(id__in=article_ids)

        return render(
            request,
            "blog/article_bulk_delete.html",
            {
                "articles": articles,
            },
        )

    # 第二步：確認頁送來 → 真正刪除
    if request.method == "POST" and "confirm" in request.POST:
        article_ids = request.POST.getlist("article_ids")

        deleted_count, _ = Article.objects.filter(id__in=article_ids).delete()
        messages.success(request, f"已成功刪除 {deleted_count} 篇文章")

        return redirect("blog:article_list")

    # 其他情況（例如直接 GET）
    return redirect("blog:article_list")


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
