from django.db import models

# Create your models here.
from association.models import Association
from student.models import Student


class Stick(models.Model):
    content = models.TextField(null=True, verbose_name='评论内容')
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name='发帖学生')
    association = models.ForeignKey(Association, null=True, on_delete=models.CASCADE, verbose_name='所属社团')
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    praise = models.IntegerField(default=0, verbose_name='点赞数量')

    class Meta():
        db_table = 'stick'


class Comment(models.Model):
    """
    评论类
    """
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    comment_content = models.TextField(null=False, verbose_name='评论内容')
    comment_parent = models.IntegerField(null=True, verbose_name='评论对象')
    comment_parise = models.IntegerField(default=0, verbose_name='点赞数')
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name='学生账号评论')
    association = models.ForeignKey(Association, null=True, on_delete=models.CASCADE, verbose_name='社团账号评论')
    stick = models.ForeignKey(Stick, on_delete=models.CASCADE, verbose_name='评论帖子')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta():
        db_table = 'comment'