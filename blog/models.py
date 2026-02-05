from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from blog.validators import (
    validate_image_dimensions,
    validate_image_extension,
    validate_image_size,
)


class Author(models.Model):
    # _("姓名")表示欄位的顯示名稱
    name = models.CharField(_("姓名"), max_length=100)
    email = models.EmailField(_("電子郵件"), unique=True)
    bio = models.TextField(_("個人簡介"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # 代表這一個model的資訊
    class Meta:
        verbose_name = _("author")  # 單數名詞要顯示什麼
        verbose_name_plural = _("authors")  # 複數名詞要顯示什麼

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_("名稱"), max_length=50, unique=True)

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(_("標題"), max_length=200)
    content = models.TextField(_("內容"))
    # ImageField是圖片檔案的資料
    cover_image = models.ImageField(
        _("封面圖片"),
        # 檔案最後要被上傳到哪個路徑
        upload_to="articles/covers/",
        blank=True,
        null=True,
        validators=[
            # 驗證發生的點都在python裡面，沒有下makemigrations與migrate亦可正常執行
            validate_image_size,
            validate_image_extension,
            validate_image_dimensions,
        ],
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
    is_published = models.BooleanField(_("是否發布"), default=False)

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

    class Meta:
        verbose_name = _("article")
        verbose_name_plural = _("articles")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"article_id": self.pk})

    def get_cover_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        # 沒有上傳圖片時顯示設定的url路徑的圖片
        return static("blog/images/default-cover.jpg")
