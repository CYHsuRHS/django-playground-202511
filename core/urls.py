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
from django.contrib import admin

# 把auth的views import進來並重新命名為auth_views
from django.contrib.auth import views as auth_views
from django.urls import include, path

auth_urlpatterns = [
    # as_view表示將LoginView這個class轉換成function的view,在轉成view的同時template_name要使用"registration/login.html"這個template
    # 但template_name預設值就是"registration/login.html",所以auth_views.LoginView.as_view()也是可以正常運作
    # 若auth_views.LoginView.as_view(template_name="registration/login.html",redirect_authenticated_user=True)使用者登入後,進入登入頁面就不會看到登入頁面
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("practices/", include("practices.urls")),
    path("blog/", include("blog.urls")),
    # include auth_urlpatterns list進來並且把名字取成auth,(auth_urlpatterns, "auth")是一個tuple
    # 也可以不使用tuple寫include(auth_urlpatterns)程式也可以正常執行,只是include進來的東西不具有namespace,就需要煩惱有沒有人也取名叫login
    path("auth/", include((auth_urlpatterns, "auth"))),
]

if settings.DEBUG:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [*urlpatterns, *debug_toolbar_urls()]
