from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        # 透過login強制轉成登入狀態
        login(request, user)
        messages.success(request, f"歡迎加入, {user.username}!")
        return redirect("blog:article_list")

    return render(request, "registration/register.html", {"form": form})
