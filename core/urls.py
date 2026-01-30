"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# 把auth的views import進來並重新命名為auth_views
from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from core import views
from core.ninja import api as ninja_api

auth_urlpatterns = [
    # as_view表示將LoginView這個class轉換成function的view,在轉成view的同時template_name要使用"registration/login.html"這個template
    # 但template_name預設值就是"registration/login.html",所以auth_views.LoginView.as_view()也是可以正常運作
    # 若auth_views.LoginView.as_view(template_name="registration/login.html",redirect_authenticated_user=True)使用者登入後,進入登入頁面就不會看到登入頁面
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    # auth_views.LogoutView是Class-based views所以要用as_view轉成function view
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    # views.register是function view直接放入即可
    path("register/", views.register, name="register"),
    # 使用PasswordChangeView使用as_view轉成function view
    # success_url表示成功之後要被跳往的頁面
    # 程式執行到success_url=reverse_lazy("auth:password_change_done"),時程式還沒載入完成，所以不能用reverse要使用reverse_lazy
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html",
            success_url=reverse_lazy("auth:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # 現在要要求一個密碼重設的信，所以會是一個輸入email的畫面
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            success_url=reverse_lazy("auth:password_reset_done"),
        ),
        name="password_reset",
    ),
    # reset請求已經被完成了，也就是提示使用者信件已經寄出
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # password reset的路徑，<uidb64>表示userid經過base64的計算，表示密碼重設的url是屬於哪個user的
    # <token>表示重設密碼的token
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("auth:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # 重設密碼動作已完成
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]

urlpatterns = [
    # 使用者打http://127.0.0.1:8000/系統會自動導向至http://127.0.0.1:8000/blog/articles/
    path("", RedirectView.as_view(pattern_name="blog:article_list"), name="root"),
    path("admin/", admin.site.urls),
    path("practices/", include("practices.urls")),
    path("blog/", include("blog.urls")),
    # include auth_urlpatterns list進來並且把名字取成auth,(auth_urlpatterns, "auth")是一個tuple
    # 也可以不使用tuple寫include(auth_urlpatterns)程式也可以正常執行,只是include進來的東西不具有namespace,就需要煩惱有沒有人也取名叫login
    path("auth/", include((auth_urlpatterns, "auth"))),
    path("api-drf/blog/", include("blog.drf_urls")),
    path("api-drf/token", obtain_auth_token, name="api-token"),
    # API 文件
    # 產生json檔或yaml檔
    path("api-drf/schema", SpectacularAPIView.as_view(), name="schema"),
    # 文件美觀的UI畫面
    path(
        "api-drf/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Django Ninja API
    path("api-ninja/", ninja_api.urls),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        *urlpatterns,
        *debug_toolbar_urls(),
        # 單純存取檔案，所以使用*static
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
