from django import forms

from blog.models import Article


# forms.ModelForm是forms.Form的衍申型態，從Model的定義中動態產生出Form的欄位
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # model的定義由Article來
        # fields = "__all__"  # 不管model有多少欄位，全部都要，但建議還是使用白名單寫法
        fields = ["title", "content", "author", "tags", "cover_image"]  # 表單需要的欄位
        labels = {
            "title": "標題",
            "content": "內容",
            "author": "作者",
            "tags": "標籤",
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
        # widgets決定欄位渲染時會長成什麼樣子,若tags數量太多時,則不適合使用CheckboxSelectMultiple,可使用第三方元件來解決這個問題
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
            "tags": forms.CheckboxSelectMultiple(),
        }

    # 自訂驗證邏輯，可以覆寫 clean_<field_name> 方法
    def clean_title(self):
        title = self.cleaned_data["title"]
        if "測試" in title:
            error_message = "標題不能包含「測試」"
            raise forms.ValidationError(error_message)

        return title

    # 跨欄位的錯誤訊息會是全域錯誤訊息
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get("title")
        content = cleaned_data.get("content")

        if title == content:
            raise forms.ValidationError("內容不應與標題完全相等")

        return cleaned_data
