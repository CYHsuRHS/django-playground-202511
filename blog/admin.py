from django.contrib import admin

from blog.models import Article, Author, Tag


# 在作者畫面可以同時編輯文章
# class ArticleInline(admin.TabularInline): # 橫放欄位
class ArticleInline(admin.StackedInline):  # 直放欄位
    model = Article  # 要改的model
    extra = 1  # 每次預先留一筆空白
    fields = ["title", "content", "is_published"]  # 可編輯的欄位


# admin.site.register(Article)
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_published", "created_at", "tag_count"]
    list_filter = ["is_published", "created_at", "author"]
    search_fields = [
        "title",
        "content",
        "author__name",
    ]  # 到"title"與"content"欄位尋找,作者的名稱也搜尋->跨關聯
    ordering = ["-created_at"]  # 預設排序
    list_per_page = 20  # 每20筆分頁
    actions = ["publish_articles", "unpublish_articles"]  # 註冊給admin自訂批次操作功能
    filter_horizontal = ["tags"]  # 變成左選到右或右選到左,預設要按住Ctrl選擇
    # filter_vertical = ["tags"]  # 變成上選到下或下選到上,預設要按住Ctrl選擇
    # exclude = ["is_published"]  # exclude：排除不想顯示的欄位
    # fields = ["title", "content"]  # fields：只顯示指定的欄位 正面表列 沒寫就是所有欄位顯示
    fieldsets = [  # fields 和 fieldsets，兩者擇一使用
        (
            "基本資訊",
            {
                "fields": ["title", "content"],
                "classes": ["wide"],  # 會變寬一點
            },
        ),
        (
            "進階選項",
            {
                "fields": ["author", "tags", "is_published"],
                "classes": ["collapse"],  # 預設收摺
            },
        ),
        (
            "時間資訊",
            {
                "fields": ["created_at", "updated_at"],
            },
        ),
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]  # "created_at"預設不顯示,加上這個強迫顯示並且唯讀

    @admin.display(description="標籤數量")  # tag_count顯示在列表的中文
    def tag_count(self, obj):  # obj表示當前的物件
        return obj.tags.count()

    @admin.action(description="發布選中的文章")
    def publish_articles(self, request, queryset):
        count = queryset.update(is_published=True)  # queryset就是使用者選中的那一批資料
        self.message_user(
            request, f"成功發布 {count} 篇文章"
        )  # message_user跳一個通知給使用者,在頁面的訊息列

    @admin.action(description="取消發布選中的文章")
    def unpublish_articles(self, request, queryset):
        count = queryset.update(is_published=False)
        self.message_user(request, f"成功取消發布 {count} 篇文章")


# admin.site.register(Author) # 只做註冊
# @是特殊語法 做註冊還綁定
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "created_at", "has_published_articles"]
    inlines = [ArticleInline]  # 連帶編輯關聯到的資料

    @admin.display(
        description="有已發布的文章", boolean=True
    )  # boolean=True 顯示勾或叉圖示
    def has_published_articles(self, obj):
        return obj.articles.filter(
            is_published=True
        ).exists()  # 有發布的文章數量大於等於1


admin.site.register(Tag)
