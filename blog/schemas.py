from ninja import ModelSchema

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
