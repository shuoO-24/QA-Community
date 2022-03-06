from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView

from authentication.models import User
from .models import Profile


# 我们知道装饰器就是一种高阶函数（类装饰器除外），通常作用于函数上为其增加功能
# method_decorator 亦如此，不同之处在于它是作用于类的装饰器
# 该装饰器的第 1 个参数为列表，里面是真正用于增加功能的装饰器
# 第 2 个参数为类内部被装饰的函数的名字
# 也就是说 method_decorator 这个装饰器的作用就是
# 把参数列表中的装饰器传给类内部被装饰的函数上
# login_required 的作用是登录保护
# dispatch 是根父类 View 中定义的方法，其作用是调用与请求对应的方法来处理请求
# 例如客户端发来了 GET 请求，dispatch 就调用类的 get 方法处理请求
# 所以 method_decorator 装饰器的 name 参数值通常为 'dispatch'
@method_decorator([login_required], name='dispatch')
# TemplateView 为模板视图类，只有 get 方法，只接受 GET 请求
# 也就是说这个视图类及其子类仅用于显示页面，不支持 POST 请求
class ProfileDetailView(TemplateView):
    """展示用户详情页面的视图类
    """

    model = Profile
    template_name = 'user_profile/profile.html'

    # 这个函数在父类中已有定义，这里重写了一下，首先调用父类的同名方法
    # 然后在 context 这个字典里增加用户类和用户详情类的实例
    # 最后这个 context 会传给模板文件，具体是怎么传的呢？
    # 首先这个方法的返回值会作为父类中 render_to_response 方法的参数
    # render_to_response 的返回值是 TemplateRespose 类的实例
    # TemplateResponse 是 HttpResponse 类的子类，所以一切就通了
    # 这个方法写在这里等待被调用，以提供前端模板所需数据
    def get_context_data(self, **kwargs):
        """给模板文件传递键值对
        """
        # 此时 context 字典中有俩数据：{'user_id': 用户ID, 'view': 视图类实例}
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        # 这个 self.kwargs 是解析请求路径时得到的
        user_id = self.kwargs.get('user_id')
        context['user_'] = User.objects.get(id=user_id)
        context['profile'] = Profile.objects.get(user_id=user_id)
        return context


@method_decorator([login_required], name='dispatch')
# UpdateView 作为视图类用于处理映射类实例的属性的修改
# 比 TemplateView 类支持的请求方式要多，包括 GET 、POST 和 PUT 请求
class UpdateProfileView(UpdateView):
    """更新用户详情的视图类
    """

    model = Profile
    # UpdateView 的父类 ModelFormMixin 的 get_form_class 方法用到了 fields 属性
    # 此方法的返回值是 django.forms.models 模块中 modelform_factory 函数的调用
    # modelform_factory 的返回值是一个根据 fields 属性创建的表单类
    # 也就是说 get_form_class 方法的返回值是利用 fields 创建的表单类
    fields = ['avatar', 'url', 'location', 'job']
    template_name = 'user_profile/profile_update.html'

    def dispatch(self, request, *args, **kwargs):
        # 这里加个判断
        # 如果当前登录的用户不是超级用户且与被编辑的用户不是同一个
        # 则重定向到被编辑的用户的详情页
        if (not request.user.is_admin and 
                request.user.id != kwargs.get('user_id')):
            return redirect('user_profile:profile', self.kwargs.get('user_id'))
        return super().dispatch(request, *args, **kwargs)

    # 父类中用于处理请求的 get 、post 方法里用到了 get_object 方法
    # 在 django.views.generic.detail 模块的 SingleObjectMixin 类中
    # 定义了 get_object 方法，其返回值是映射类实例
    # 通过其它方法，该映射类实例被赋值给当前类的 object 属性
    # 此处重写了该方法，功能不变
    # 参数 queryset 的作用是提供一个查询对象，就是查询数据库得到的那个
    # 如果该参数值为 None ，会调用某个父类提供的 get_queryset 方法获取查询对象
    # 这里并未用到该参数，可以省略不写
    def get_object(self, queryset=None):
        # 视图类在使用时，首先要调用其父类中的 as_view 方法生成视图函数
        # 生成的视图函数内部会调用根父类 View 的 setup 方法
        # 将键值对参数赋值给 self.kwargs 属性
        return Profile.objects.get(user_id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        kw = super().get_context_data(**kwargs)
        kw['user_'] = User.objects.get(id=self.kwargs.get('user_id'))
        return kw

    # 如果客户端发来的是 post 请求，视图类会调用从父类继承的 post 方法处理
    # 表单数据通过了全部验证后，会自动调用 form_valid 方法进行最后的处理
    # 参数 form 是由 Django 框架自动生成的表单类的实例
    def form_valid(self, form):
        # 表单类实例的 save 方法的作用是创建 Profile 映射类的实例
        # 然后调用该实例的 save 方法保存实例数据到数据库并返回该实例
        # commit=False 会略过映射类实例调用自身的 save 方法这一步
        profile = form.save(commit=False)
        profile.save()
        form.save_m2m()
        # 重定向到路由的命名空间 user 下面的 profile 路径
        # 即 user/urls.py 的 urlpatterns 列表里 name 参数值为 profile 的 path
        # 第二个参数为 Pattern 映射类实例的 user_id 属性值
        # 它将被赋值给 path 方法的第一个参数的 <int:user_id>
        return redirect('user_profile:profile', self.kwargs.get('user_id'))
