from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import User


def forbidden_username_validator(value):
    """判断用户名是否属于禁用词
    """

    forbidden_usernames = {
        'admin', 'settings', 'news', 'about', 'help', 'signin', 'signup',
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout',
        'administrator', 'join', 'account', 'username', 'root', 'blog',
        'authentication', 'users', 'billing', 'subscribe', 'reviews', 'review',
        'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs',
        'newsletter', 'shop', 'profile', 'register', 'authentication',
        'campaign', '.env', 'delete', 'remove', 'forum', 'forums',
        'download', 'downloads', 'contact', 'blogs', 'feed', 'feeds', 'faq',
        'intranet', 'log', 'registration', 'search', 'explore', 'rss',
        'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'questions', 'articles', 'network',
        'contribute', 'authentication',
    }

    if value.lower() in forbidden_usernames:
        msg = _('This is a reserved username.')
        raise ValidationError(msg)


def invalid_username_validator(value):
    """检查用户名是否包含非法字符
    """

    if '@' in value or '+' in value or '-' in value:
        msg = _('Enter a valid username.')
        raise ValidationError(msg)


def unique_email_validator(value):
    """验证邮箱唯一性
    """

    if User.objects.filter(email__iexact=value).exists():
        msg = _('User with this email already exists.')
        raise ValidationError(msg)


def unique_username_validator(value):
    """验证用户名唯一性
    """

    if User.objects.filter(username__iexact=value).exists():
        msg = _('User with this username already exists.')
        raise ValidationError(msg)


# ModelForm 来自 django.forms.models 模块，是创建表单类的专用父类
class SignUpForm(forms.ModelForm):
    """创建新用户使用的注册表单类
    """

    # 各个字段中的 TextInput 、EmailInput 等都是 Widget 类的子类
    # Widget 定义在 django.forms.widgets 模块中
    # 每个 Widget 类的子类对应一种前端 <input type=''> 标签的 type 属性
    # 例如 TextInput 对应的是 <input type='text'>

    username = forms.CharField(
        # 文本输入框
        widget = forms.TextInput(attrs={'class': 'form-control'}),  
        max_length = 32,        # 输入内容的长度
        required = True,        # 必填项
        label = _('Username'),  # 输入框前面的提示信息
        # 输入框下面的提示信息
        help_text = _("Username may contain alphanumeric, "
                      "'_' and '.' characters.")
    )

    password = forms.CharField(
        # 密码输入框
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        label = _('Password'),  # 输入框前面的提示信息
        required = True         # 必填项
    )

    confirm_password = forms.CharField(
        # 密码输入框
        widget = forms.PasswordInput(attrs={'class': 'form-control'}),
        label = _('Confirm your password'),
        required = True,
    )

    email = forms.EmailField(
        # 邮箱输入框
        widget = forms.EmailInput(attrs={'class': 'form-control'}),
        required = True, 
        max_length = 75,
        label = _('Email')
    )

    class Meta:
        model = User
        exclude = ['last_login', 'date_joined']
        fields = ['username', 'email', 'password', 'confirm_password',]

    def __init__(self, *args, **kwargs):
        """验证表单数据合法性
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].validators += [
            forbidden_username_validator, 
            invalid_username_validator,
            unique_username_validator,
        ]
        self.fields['email'].validators += [
            unique_email_validator,
        ]

    def clean_password(self):
        """验证两次输入密码是否一致
        """
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            msg = _('Passwords don\'t match.')
            raise ValidationError(msg)
        return password

    def save(self, commit=True):
        """保存前的操作
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
