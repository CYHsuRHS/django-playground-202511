from django.conf import settings
from django.db import models
from django.templatetags.static import static


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # ImageField是圖片檔案的資料
    cover_image = models.ImageField(
        # 檔案最後要被上傳到哪個路徑
        upload_to="articles/covers/",
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        # 關聯到它設定的User
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # null=True,
        # blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    author = models.ForeignKey(  # ForeignKey外鍵會關聯到Author這張表
        Author,
        on_delete=models.CASCADE,  # 假設作者這筆資料被刪掉,文章就一起被刪掉
        related_name="articles",  # 反向的名字如何查詢,不寫也可以,Django 會自動命名為Default article
        null=True,
        blank=True,
    )

    tags = models.ManyToManyField(  # 多對多的關聯
        Tag,
        related_name="articles",  # 反向的名字如何查詢
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        # 沒有上傳圖片時顯示設定的url路徑的圖片
        return static("blog/images/default-cover.jpg")
