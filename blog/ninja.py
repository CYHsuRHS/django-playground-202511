# Router需與API搭配才可使用
from ninja import Router

from blog.models import Article

router = Router()


# 這個router有一個get方法的API view路徑為/articles
@router.get("/articles")
def list_articles(request):
    # 所有Article的queryset
    articles = Article.objects.all()
    # 用for迴圈變成一個list，裡面有很多dictionary
    return [
        {
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "is_published": article.is_published,
            "created_at": article.created_at,
        }
        for article in articles
    ]


# 因已指定article_id: int，故{article_id}只能出現數字
@router.get("/articles/{article_id}")
def get_article(request, article_id: int):
    # 直接以id取得一篇文章
    article = Article.objects.get(id=article_id)
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "is_published": article.is_published,
        "created_at": article.created_at,
    }
