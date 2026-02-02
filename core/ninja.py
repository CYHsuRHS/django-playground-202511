from ninja import NinjaAPI  # , Redoc
from ninja.security import HttpBearer
from rest_framework.authtoken.models import Token

from blog.ninja import router as blog_router


# HttpBearer是一個傳遞token的方法
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # 以使用者傳進來的token到DRF的token裡面找，有沒有這個token，有找到它就是那個使用者的token
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return None  # 回傳None表認證失敗

        return token_obj.user


# 實例化為api的變數，auth=AuthBearer()表示所有API都要經過驗證
api = NinjaAPI(
    title="Blog API",
    version="1.0.0",
    description="Django 大冒險的部落格 API (Django Ninja 版本)",
    auth=AuthBearer(),
    # docs=Redoc(),
)
api.add_router("/blog", blog_router, tags=["文章"])


# 這個api允許使用get方法訪問/hello
@api.get("/hello")
def hello(request):
    return {"message": "Hello, Django Ninja!"}
