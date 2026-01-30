from datetime import datetime

from ninja import Schema


class ArticleIn(Schema):
    title: str
    content: str
    is_published: bool = False


class ArticleOut(Schema):
    id: int
    title: str
    content: str
    is_published: bool
    created_by_id: int
    author_id: int | None
    created_at: datetime
    updated_at: datetime
