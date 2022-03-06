from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    """问题表单类
    """

    title = forms.CharField(
        max_length = 255,
        label = _('Title'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        # 指定输入内容的最大长度
        max_length = 2000,
        # 设置输入框的名称
        label = _('Description'),
        # 为输入框增加标签属性
        widget = forms.Textarea(attrs={'class': 'form-control'}),
        # 输入框下面的提示语
        help_text = _('Write the question\'s description...')
    )

    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerForm(forms.ModelForm):
    """答案表单类
    """

    description = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'})
    )

    class Meta:
        model = Answer
        fields = ['description']