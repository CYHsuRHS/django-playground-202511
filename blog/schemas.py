from typing import Annotated

from ninja import FilterLookup, FilterSchema, ModelSchema

from blog.models import Article


class ArticleIn(ModelSchema):
    class Meta:
        model = Article
        fields = ["title", "content", "is_published"]


class ArticleOut(ModelSchema):
    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "content",
            "is_published",
            "created_by",
            "author",
            "created_at",
            "updated_at",
        ]


class ArticleFilterSchema(FilterSchema):
    # None的意思是這欄位不參與Filter
    is_published: bool | None = None
    # __是ORM的lookup
    title__icontains: str | None = None
    search: Annotated[
        # 第一個參數是用來表達search的型態，第二個參數表示要到什麼欄位找
        str | None, FilterLookup(["title__icontains", "content__icontains"])
    ] = None
