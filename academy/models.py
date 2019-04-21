from django.db import models


# Create your models here.
class Area(models.Model):
    """
    地区表
    """
    code_id = models.IntegerField(primary_key=True, verbose_name='编号')
    parent_id = models.IntegerField(verbose_name='父级编号')
    area_name = models.CharField(max_length=180, verbose_name='区域名称')

    class Meta():
        db_table = 'area'

    def to_dict(self):
        return {'code_id':      self.code_id, 'parent_id': self.parent_id, 'area_name': self.area_name}


class Major(models.Model):
    """
    专业
    """
    major_name = models.CharField(max_length=100, verbose_name='专业名称')

    class Meta():
        db_table = 'major'

    def to_dict(self):
        return {'id': self.id, 'major_name': self.major_name}


class Academy(models.Model):
    """
    院校表
    """
    STATUS = (
        (1, '使用中'),
        (2, '停用'),
        (3, '未开通'),
    )
    school_name = models.CharField(max_length=60, verbose_name='名称')
    major = models.ManyToManyField(Major, verbose_name='院校专业')
    area = models.ForeignKey(Area, verbose_name='城市id')
    school_num = models.CharField(max_length=20, null=True, verbose_name='院校账号')
    school_pwd = models.CharField(max_length=200, null=True, verbose_name='院校密码')
    school_tel = models.CharField(max_length=15, null=True, verbose_name='院校电话')
    status = models.IntegerField(choices=STATUS, default=3, verbose_name='院校状态')

    class Meta():
        db_table = 'academy'

    def to_dict(self):
        return {'id': self.id, 'school_name': self.school_name, 'area_id': self.area_id, 'school_num': self.school_name,
                'school_tel': self.school_tel}

    def __str__(self):
        return self.school_name



