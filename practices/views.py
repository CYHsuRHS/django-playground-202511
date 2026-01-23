from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# def hello_world(request):
#     return render(request, "practices/hello.html")


class HelloWorldView(TemplateView):
    template_name = "practices/hello.html"


def greeting(request):
    name = "Django"
    return render(request, "practices/greeting.html", {"name": name})


def search(request):
    keyword = request.GET.get("q", "")
    # GET 參數
    # return HttpResponse(f"Keyword: {keyword}")
    # 使用表單傳遞 GET 參數
    return render(request, "practices/search.html", {"keyword": keyword})


def product_list(request):
    category = request.GET.get("category", "all")
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    return HttpResponse(f"分類: {category}, 排序: {sort}, 頁數: {page}")


def filter_products(request):
    c = request.GET.get("color")
    colors = request.GET.getlist("color")
    print(c)  # 要到終端機介面看
    print(colors)
    return HttpResponse(f"選擇的顏色: {', '.join(colors)}")


def hello_name(request, name):
    print(name, type(name))
    return HttpResponse(f"Hello, {name}!")


def article_detail(request, year, month, slug):
    return HttpResponse(f"文章: {year} 年 {month} 月 - {slug}")


def user_articles(request, username):
    sort = request.GET.get("sort", "newest")
    page = request.GET.get("page", "1")

    return HttpResponse(f"{username} 的文章, 排序: {sort}, 頁數: {page}")


def advanced_search(request):
    keyword = request.GET.get("q", "")
    category = request.GET.get("category", "all")
    sort = request.GET.get("sort", "newest")

    return render(
        request,
        "practices/advanced_search.html",
        {
            "keyword": keyword,
            "category": category,
            "sort": sort,
        },
    )


def color_filter(request):
    colors = request.GET.getlist("color")
    return render(
        request,
        "practices/color_filter.html",
        {"colors": colors},
    )


def contact(request):
    context = {}

    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        context = {
            "success": True,
            "name": name,
            "email": email,
            "message": message,
        }

    return render(request, "practices/contact.html", context)


from django.views import View


class ContactView(View):
    def get(self, request):
        context = {}
        return render(request, "practices/contact.html", context)

    def post(self, request):
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")

        context = {
            "success": True,
            "name": name,
            "email": email,
            "message": message,
        }

        return render(request, "practices/contact.html", context)


def cookie_counter(request):
    # 從 Cookie 讀取訪問次數
    visit_count = request.COOKIES.get("visit_count", "0")
    visit_count = int(visit_count) + 1

    # 建立回應
    response = HttpResponse(f"你已經訪問了 {visit_count} 次")

    # 設定 Cookie
    response.set_cookie("visit_count", str(visit_count))

    return response


def theme_preference(request):
    # 從 GET 參數讀取主題設定
    theme = request.GET.get("theme")

    # 從 Cookie 讀取目前的主題
    current_theme = request.COOKIES.get("theme", "light")

    # 如果有新的主題設定就更新
    if theme:
        current_theme = theme

    # 建立回應
    response = render(request, "practices/theme.html", {"theme": current_theme})

    # 儲存主題設定到 Cookie
    if theme:
        response.set_cookie("theme", current_theme, max_age=365 * 24 * 60 * 60)

    return response


def shopping_cart(request):
    # 取得操作類型
    action = request.GET.get("action")
    product = request.GET.get("product")

    # 從 Session 取得購物車, 如果沒有就建立空字典
    cart = request.session.get("cart", {})

    # 處理加入購物車
    if action == "add" and product:
        cart[product] = cart.get(product, 0) + 1
        request.session["cart"] = cart

    # 處理移除商品
    elif action == "remove" and product:
        if product in cart:
            del cart[product]
            request.session["cart"] = cart

    # 處理清空購物車
    elif action == "clear":
        request.session["cart"] = {}

    # 重新取得購物車, 可能已更新
    cart = request.session.get("cart", {})

    return render(request, "practices/cart.html", {"cart": cart})
