from django.db import models

# Create your models here.
from academy.models import Academy, Major, Area


class Student(models.Model):
    """
    学生表
    """
    GENDER = (
        ("male", "男"),
        ("female", "女")
    )
    stu_name = models.CharField(max_length=20, null=True, verbose_name='姓名')
    # stu_nick = models.CharField(max_length=100, null=True, verbose_name='昵称')
    stu_num = models.CharField(max_length=20, null=True, verbose_name='学号')
    stu_pwd = models.CharField(max_length=200, verbose_name='学生密码')
    stu_birth = models.DateField(max_length=20, null=True, verbose_name="出生年月")
    stu_sex = models.CharField(max_length=6, choices=GENDER, default='male', verbose_name='性别')
    stu_tel = models.CharField(max_length=11, verbose_name='手机')
    stu_mail = models.EmailField(max_length=100, null=True, verbose_name='邮箱')
    stu_native = models.ForeignKey(Area, null=True, verbose_name='籍贯', on_delete=models.CASCADE)
    stu_motto = models.CharField(max_length=200, null=True, verbose_name='签名')
    stu_head = models.ImageField(upload_to='student/images/', null=True, verbose_name='头像')
    stu_growth = models.IntegerField(default=0, verbose_name='成长值')
    join_time = models.DateField(auto_now_add=True, verbose_name='注册时间')
    academy = models.ForeignKey(Academy, null=True, verbose_name='学校', on_delete=models.CASCADE)
    major = models.ForeignKey(Major, null=True, verbose_name='系别', on_delete=models.CASCADE)
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'student'