from django.db import models
from django.db.models.signals import post_save

from authentication.models import User


# 父类是 django.db.models.base.Model 类
class Profile(models.Model):
    """用户个人简介映射类
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    job = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(upload_to='pic_folder', default='img/user.png')
    class Meta:
        db_table = 'user_profile'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 使用信号，在创建 user 时同时创建 profile
# Django 自带一套信号系统帮助我们在框架中传递信息
# 当某种条件出现时，信号发送者利用信号系统将信号发送给信号接收者
# 信号系统中有很多对象用于实现信息传递功能
# 这些对象都是 db.models.signals 模块下 ModelSignal 类的实例
# 其中包括 post_save 对象，当某映射类的实例执行 save 方法保存数据后
# 该映射类会自动发送信号给信号接收者
# ModelSignal 类有一个 connect 方法，第一个位置参数就是接收信号的对象
# 第二个参数 sender 就是发送信号的那个映射类
# 如下所示差不多是固定写法
# 当 User 类的实例被存储到数据库，自动执行第一个参数那个函数
# 此处 sender 参数的值可以是引入的映射类，也可以用字符串表示
post_save.connect(create_user_profile, sender=User)
