from django import forms

from blog.models import Article


# forms.ModelForm是forms.Form的衍申型態，從Model的定義中動態產生出Form的欄位
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # model的定義由Article來
        # fields = "__all__"  # 不管model有多少欄位，全部都要，但建議還是使用白名單寫法
        fields = ["title", "content", "author"]  # 表單需要的欄位
        labels = {
            "title": "標題",
            "content": "內容",
            "author": "作者",
        }
        error_messages = {
            "title": {
                "required": "標題不能空白",
                "max_length": "標題最多 %(limit_value)d 字元",
            },
            "content": {
                "required": "內容不能空白",
            },
        }
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
        }
