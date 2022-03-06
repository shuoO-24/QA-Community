import markdown
from django.db import models

from authentication.models import User


class Question(models.Model):
    """问题映射类
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    # 参数 auto_now_add 作用是自动添加该字段的值为当前时间
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'
        # 按照 update_date 字段的值降序排列
        ordering = ('-update_date',)

    def __str__(self):
        return self.title

    # 前端模板文件中会用到此方法获取问题的回答集合
    # 类似这样:{% for answer in question.get_answers %}
    def get_answers(self):
        """获取问题相关的所有答案
        """
        return Answer.objects.filter(question=self)

    def get_answers_count(self):
        """获取问题的答案总数
        """
        return Answer.objects.filter(question=self).count()

    def get_description_as_markdown(self):
        """将问题文本渲染为 Markdown 格式
        """
        return markdown.markdown(self.description, safe_mode='escape')
    
    
class Answer(models.Model):
    """答案映射类
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField(max_length=2000)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'
        ordering = ('create_date',)

    def __str__(self):
        return self.description

    def get_description_as_markdown(self):
        """将问题文本渲染为 Markdown 格式
        """
        return markdown.markdown(self.description, safe_mode='escape')