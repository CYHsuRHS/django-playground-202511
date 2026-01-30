from django.shortcuts import get_object_or_404

# Router需與API搭配才可使用
from ninja import Router

from blog.models import Article
from blog.schemas import ArticleOut

router = Router()


# /articles的response格式會是list包著ArticleOut
@router.get("/articles", response=list[ArticleOut])
def list_articles(request):
    # 已經知道回應格式是list包著ArticleOut就不需自己做處理了，直接把queryset給它，它知道schemas是什麼自己會想辦法處理
    return Article.objects.all()


# response=ArticleOut表示只有一筆資料
@router.get("/articles/{article_id}", response=ArticleOut)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)
