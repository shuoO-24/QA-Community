from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import ProfileDetailView, UpdateProfileView


# 设置命名空间，便于前端构造路由
app_name = 'user_profile'


urlpatterns = [
    # 此 path 函数的返回值是「路由处理对象」，即 URLResolver 类的实例
    path('user/', 
        # 此 include 函数的返回值是一个三元元组，第一个元素是列表
        # 列表里面是两个「路由模式对象」，即 URLPattern 类的实例
        include(([
            path('<int:user_id>/', ProfileDetailView.as_view(), name='profile'),
            path('<int:user_id>/edit', UpdateProfileView.as_view(), 
                name='update_profile'),
        ]))
    ),
]


# 这个 static 函数返回的是列表，列表里面是「路由模式对象」
# 第一个参数是字符串 '/media/' ，该对象匹配的就是以第一个参数开头的请求路径
# 注意只有在 DEBUG 模式下这个才有用
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
