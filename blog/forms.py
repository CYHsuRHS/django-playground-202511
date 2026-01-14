from django import forms

from blog.models import Author


# ArticleForm這個class繼承Django定義的forms class
class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,  # 表必填
        label="標題",
        error_messages={
            "required": "標題不能空白",
            "max_length": "標題最多 %(limit_value)d 字元",  # Django提供%(limit_value)d會根據上方max_length的值顯示
        },  # 顯示的錯誤訊息
    )
    content = forms.CharField(
        widget=forms.Textarea,  # Textarea多行的文字方塊
        required=True,
        label="內容",
        error_messages={
            "required": "內容不能空白",
        },
    )
    # ChoiceField是選單型的欄位
    author = forms.ChoiceField(
        choices=[],  # 空的選項
        required=False,
        label="作者",
    )

    # __init__ 是python class的建構子，在這個類別被變成物件的時候，表單被建立要執行的動作
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 表執行繼承的forms原本的__init__

        # 多做的動作
        self.fields["author"].choices = [("", "未指定")] + [
            (author.id, author.name) for author in Author.objects.all()
        ]
