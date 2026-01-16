from django.urls import path

from practices import views

app_name = "practices"

urlpatterns = [
    path("hello/", views.hello_world, name="hello_world"),
    path("greeting/", views.greeting, name="greeting"),
    path("search/", views.search, name="search"),
    path("products/", views.product_list, name="product_list"),
    path("products/filter/", views.filter_products, name="product_filter"),
    path("hello/<str:name>/", views.hello_name, name="hello_name"),
    path(
        "articles/<int:year>/<int:month>/<slug:slug>/",
        views.article_detail,
        name="article_detail",
    ),
    path(
        "users/<str:username>/articles/",
        views.user_articles,
        name="user_articles",
    ),
    path("advanced-search/", views.advanced_search, name="advanced_search"),
    path("color-filter/", views.color_filter, name="color_filter"),
    path("contact/", views.contact, name="contact"),
    path("cookie-counter/", views.cookie_counter, name="cookie_counter"),
    path("theme/", views.theme_preference, name="theme_preference"),
    path("cart/", views.shopping_cart, name="shopping_cart"),
]
