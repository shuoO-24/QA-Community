from django.urls import include, path
# auth_views 是 django.contrib.auth.views 模块
from django.contrib.auth import views as auth_views

from .views import UserSignupView


# 这个变量用于增加路由的命名空间，当前端使用 {% url %} 设置路由时
# 可以写成这样：{% url 'authentication:signup' %}
# 意为 authentication 命名空间下 name 为 signup 的 path 来处理
app_name = 'authentication'


urlpatterns = [
    # 函数 path 须提供两个位置参数：route 和 view
    # 所有视图类均继承自 django.views.generic.base.View 类
    # 后者提供了一个 as_view 方法，此方法内部定义并返回了一个嵌套 view 方法
    # 该 view 方法就是视图函数
    path('signup/', UserSignupView.as_view(), name='signup'),
    # 这里使用了 django.contrib.auth.views 模块中定义的
    # 视图类提供的登录、登出功能
    # 该视图类的 as_view 定义在父类 django.views.generic.base.View 中
    path('login/', auth_views.LoginView.as_view(
        template_name='authentication/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
