from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm


@method_decorator([login_required], name='dispatch')
class CreateQuestionView(CreateView):
    """创建问题的视图类
    """

    model = Question
    # CreateView 的一个父类是同模块中的 FormMixin
    # 后者有一个 get_form 方法用于创建表单类的实例,此方法的参数就是 form_class
    form_class = QuestionForm
    template_name = 'questions/ask_question.html'

    # 当客户端发送 POST 请求,服务器会调用对应的方法处理
    # 表单数据通过全部验证后,自动调用此方法进行最后的处理
    # 参数 form 是 QuestionForm 类的实例
    def form_valid(self, form):
        question = form.save(commit=False)
        # 在路由管理器中,path 方法的参数为视图类调用 as_view 方法的返回值
        # 此方法在当前类的根父类 View 中定义,其返回值为内部定义的 view 函数
        # 类中同时定义了 setup 方法,此方法将定义 self.request 属性
        # 该属性值为浏览器发送的请求对象 request
        # as_view 的返回值 view 函数中调用 setup 方法
        # self.request.user 属性值为当前登录的用户实例
        question.user = self.request.user
        question.save()
        # success 是 django.contrib.messages.api 模块下的函数
        # 此函数的作用是给请求对象添加页面消息(通常展示在页面顶部)
        # 参数分别是请求对象和消息内容
        # 除了 success 还有 info 、warning 、error 等方法分别对应不同样式的消息
        messages.success(self.request, 'The question was created with success!')
        # 浏览器使用 POST 方法提交创建问题的表单后
        # 视图类完成全部处理工作,最后重定向到问题详情页
        return redirect('questions:question_detail', question.pk)


class QuestionListView(ListView):
    """展示问题列表的视图类
    """

    model = Question
    ordering = ('update_date')
    # 下面这两个属性用于向前端模板文件中提供一组键值对
    # 前端模板文件中可以使用变量 questions 获取 Question 映射类的全部实例
    # 在父类 MultipleObjectMixin 中定义的 get_context_data 方法会处理它们
    # 将它们组合成键值对写到字典对象中传递给前端模板文件
    context_object_name = 'questions'
    template_name = 'questions/questions_list.html'
    queryset = Question.objects.all()
    # 父类 MultipleObjectMixin 中定义了 get_paginate_by 方法
    # 其返回值就是 panginate_by 的属性值
    # get_context_data 方法会对此增加一组键值对
    # key 为 'page_size' ,value 为 paginate_by ,即每页展示问题的数量
    paginate_by = 10


# 问题详情页面需要提供编写答案的表单
# 这就是使用 CreateView 作为父类的原因
class QuestionDetailView(CreateView):
    """展示问题详情的视图类
    """

    model = Answer
    form_class = AnswerForm
    template_name = 'questions/question_detail.html'

    # 视图类最终会返回响应对象给浏览器,也就是 HttpResponse 类的子类的实例
    # 用户的 GET 请求会调用视图类的 get 方法处理
    # 而 get 方法的返回值通常是 render_to_response 方法的调用
    # 后者定义在 django.views.generic.base 模块的 TemplateResponseMixin 类中
    # 调用它需要提供 get_context_data 方法的返回值
    # get_context_data 在父类中也有定义,其作用是给模板文件提供 context 属性值
    # 这个方法的返回值就是字典对象,里面的键值对可以在前端模板中使用
    def get_context_data(self, **kwargs):
        # 视图类的 as_view 方法的返回值是方法内部定义的 view 函数
        # view 函数被调用时会提供 URL 参数的键值对
        # 在 question.urls 模块中定义的路由实例 path 中
        # 第一个参数 '<int:pk>/' 提供了 pk 字段的值,即问题映射类的 id 属性
        # 所以 view 函数被调用时,是这样的:view(request, **{'pk': 2})
        # view 函数内部的变量 kwargs 的值就是字典 {'pk': 2}
        # view 函数内部调用视图类实例的 setup 方法设置当前类的实例属性
        # self.request = request ,self.kwargs = kwargs
        question_id = self.kwargs.get('pk')
        # 以下 4 行代码为前端模板文件增加了 question 和 answers 对象
        # 因为问题的详情页不仅要展示问题,还要展示问题的答案
        question = Question.objects.get(pk=question_id)
        kwargs['question'] = question
        if Answer.objects.filter(question=question):
            kwargs['answers'] = Answer.objects.filter(question=question)

        context = super().get_context_data(**kwargs)
        return context


@login_required
def create_answer(request, pk):
    if request.method == 'POST':
        # 表单类 AnswerForm 的父类的初始化方法 __init__ 中第一个参数为 data
        # 该参数的值为字典对象,用于在创建实例时为属性赋值
        # 在 django.forms.forms 模块的 BaseForm 类中
        # full_clean 方法会调用 _clean_fields 方法,后者实现属性赋值操作
        # 注意此处的属性并非指表单类中定义的属性
        # 而是 full_clean 方法创建的表单类属性 cleaned_data
        # 该属性为字典对象,用于存储提交表单中的数据
        # request.POST 为字典对象,保存提交表单中的数据
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.user = request.user  # 设定问题提出人
            answer.question = Question.objects.get(pk=pk)
            answer.description = form.cleaned_data.get('description')
            answer.save()
            # 此函数的作用是给请求对象添加页面消息(通常展示在页面顶部)
            messages.success(request, 'The answer was created with success!')
            # 创建了回答后,跳转到问题的详情页
            return redirect('questions:question_detail', answer.question.pk)
    # 通常只有 POST 请求会访问此函数对应的 URL
    # 就是用户点击 "问题详情页" 提供的 "回答表单" 下面的提交按钮
    # 如果有 get 请求的话,就跳转到对应的问题详情页面
    return redirect('questions:question_detail', pk)