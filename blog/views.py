from django.shortcuts import render

from blog.models import Article


# article_list(request)表示是一個function view
def article_list(request):
    articles = Article.objects.all()  # 把Article這張表的所有物件撈出來放在articles變數
    return render(
        request, "blog/article_list.html", {"articles": articles}
    )  # 透過render function將articles變數丟到"articles" template裡面，要渲染的畫面是"blog/article_list.html"，並且挾帶articles變數到"articles" template裡
