from django.shortcuts import redirect


def home(request):
    """网站首页
    """

    return redirect('questions:questions_list')