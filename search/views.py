from django.shortcuts import render, redirect
from django.db.models import Q

from questions.models import Question


def search(request):
    """搜索功能视图函数
    """

    # 在 base.html 文件中有一个输入框 <input name='q'>
    # 它用来填写要搜索的问题的关键字
    # 写好关键字,点击搜索,就会将请求交给当前这个视图函数来处理
    # 请求方法是默认的 GET 方法,所以 request.GET 字典中应有 'q'
    if 'q' not in request.GET:
        return redirect('')
    # 将关键词根据空格分开成为列表
    querystring = request.GET.get('q').strip()
    # 若没有输入信息
    if len(querystring) == 0:
        return redirect('home')

    # 利用 Question 映射类查询数据库,Q 类可以实现一些高级的查询方式
    # 在 django.db.models.query_unilts 模块中定义了 Q 类
    # filter 方法中有两个 Q 类的实例作为参数,用或符号 | 连接
    # 意为查询数据库中符合任一条件的数据
    results = {'questions': Question.objects.filter(
        Q(title__icontains=querystring) |
        Q(description__icontains=querystring))}

    count = {'questions': results['questions'].count()}
    # 创建字典对象传给前端模板文件
    context = {
        'querystring': querystring,
        'count': count['questions'],
        'results': results['questions']
    }

    return render(request, 'search/results.html', context)