from django import forms


# ArticleForm這個class繼承Django定義的forms class
class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,  # 表必填
        error_messages={
            "required": "標題不能空白",
            "max_length": "標題最多 %(limit_value)d 字元",  # Django提供%(limit_value)d會根據上方max_length的值顯示
        },  # 顯示的錯誤訊息
    )
    content = forms.CharField(
        widget=forms.Textarea,  # Textarea多行的文字方塊
        required=True,
        error_messages={
            "required": "內容不能空白",
        },
    )
    author = forms.IntegerField(
        required=False,
    )  # 直接填入作者id
