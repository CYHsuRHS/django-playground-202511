from django.shortcuts import get_object_or_404

# Router需與API搭配才可使用
from ninja import PatchDict, Query, Router
from ninja.errors import HttpError

from blog.models import Article
from blog.schemas import ArticleFilterSchema, ArticleIn, ArticleOut

# Router(auth=django_auth)表示這個Router所有的路徑都要靠django_auth驗證
# router = Router(auth=django_auth)
router = Router()


# /articles的response格式會是list包著ArticleOut，可透過auth=None來覆蓋Router的驗證設定
@router.get("/articles", response=list[ArticleOut], auth=None)
# Query[ArticleFilterSchema]有加上Query才知道是GET的參數，沒加Query預設是POST的參數
def list_articles(request, filters: Query[ArticleFilterSchema]):
    return filters.filter(Article.objects.all())


# response=ArticleOut表示只有一筆資料
@router.get(
    "/articles/{article_id}",
    response=ArticleOut,
    auth=None,
    # 有客製化需求，文件需要寫很清楚，需要額外補充，可以使用openapi_extra格式撰寫，風格要遵守openapi的格式
    openapi_extra={
        "responses": {
            404: {
                "description": "文章不存在",
            }
        }
    },
)
def get_article(request, article_id: int):
    return get_object_or_404(Article, id=article_id)


@router.post("/articles", response={201: ArticleOut})
# payload參數型態若為ArticleIn，就會當作POST參數的一部份
def create_article(request, payload: ArticleIn):
    if not request.auth.has_perm("blog.add_article"):
        # 狀態碼403表我知道你是誰，但你沒有權限做這件事
        raise HttpError(403, "你沒有權限新增文章")

    print("===")
    print(payload)
    print("===")
    # 使用.dict()轉換為python的dictionary，透過**語法把所有dictionary的值丟到create裡面，因為有做序列化，所以可以放心地做這件事
    article = Article.objects.create(
        **payload.dict(),
        created_by=request.auth,
    )
    return 201, article


@router.put("/articles/{article_id}", response=ArticleOut)
# 依照ArticleIn型態的請求做資料驗證
def update_article(request, article_id: int, payload: ArticleIn):
    if not request.auth.has_perm("blog.change_article"):
        raise HttpError(403, "你沒有權限編輯文章")

    # 文章透過article_id做取得
    article = get_object_or_404(Article, id=article_id)
    for attr, value in payload.dict().items():
        # 透過python內建setattr，將屬性attr的名字加上value做設定
        setattr(article, attr, value)

    article.save()
    return article


# patch的概念是只傳入需要被更新的欄位，patch與put程式一模一樣，只差在payload的參數，實作時可只做patch不做put亦可達到同樣的效果
@router.patch("/articles/{article_id}", response=ArticleOut)
def partial_update_article(
    request,
    article_id: int,
    # 只要用PatchDict包起來，所有欄位都會變成選填
    payload: PatchDict[ArticleIn],
):
    if not request.auth.has_perm("blog.change_article"):
        raise HttpError(403, "你沒有權限編輯文章")

    article = get_object_or_404(Article, id=article_id)
    for attr, value in payload.items():
        setattr(article, attr, value)

    article.save()
    return article


@router.delete("/articles/{article_id}", response={204: None})
def delete_article(request, article_id: int):
    if not request.auth.has_perm("blog.delete_article"):
        raise HttpError(403, "你沒有權限刪除文章")

    article = get_object_or_404(Article, id=article_id)
    article.delete()
    # 回應204狀態碼，None表沒有任何東西要回應
    return 204, None
