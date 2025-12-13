from django.http import HttpResponse
from django.shortcuts import render


def hello_world(request):
    return render(request, "practices/hello.html")


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
