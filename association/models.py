import os

from django.db import models

# Create your models here.
from GraduationProject.settings import MEDIA_ROOT
from academy.models import Major, Academy
from student.models import Student


# class ImageFile(models):
#     """
#     图片类
#     """
#     image_name = models.CharField(max_length=200, verbose_name='图片名称')
#     image_file = models.ImageField(upload_to='gallery/', verbose_name='相册图集路径')
#
#
# class Gallery(models.Model):
#     """
#     相册类
#     """
#     gallery_name = models.CharField(max_length=200, verbose_name='相册名称')
#     imagefile = models.ManyToManyField(ImageFile, verbose_name='相册照片')


class Association(models.Model):
    """
    社团类
    """
    ASSOCIATION_TYPE=(
        (1, '艺术'),
        (2, '文学'),
        (3, '运动'),
        (3, '学术'),
    )
    APPLY_STATUS=(
        (1, '待审核'),
        (2, '通过'),
        (3, '驳回'),
        (4, '待完善'),
    )
    association_num = models.CharField(max_length=20, unique=True, verbose_name='社团编号')
    association_pwd = models.CharField(max_length=500, verbose_name='社团密码')
    association_name = models.CharField(max_length=100, verbose_name='协会名称')
    association_info = models.TextField(null=True, verbose_name='协会信息')
    association_mail = models.CharField(max_length=100, null=True, verbose_name='社团邮箱')
    association_tel = models.CharField(max_length=100, null=True, verbose_name='社团手机')
    association_start = models.DateField(null=True, verbose_name='创建时间')
    association_join = models.DateField(auto_now_add=True, verbose_name='加入时间')
    association_praise = models.IntegerField(default=0, verbose_name='社团点赞')
    association_type = models.IntegerField(choices=ASSOCIATION_TYPE, verbose_name='社团类别')
    association_growth = models.IntegerField(default=0, verbose_name='成长值')
    # association_head = models.ImageField(upload_to=MEDIA_ROOT + '/association/'+ association_num + '/images', null=True, verbose_name='头像')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    apply_status = models.IntegerField(choices=APPLY_STATUS, default=1, verbose_name='审核状态')
    students = models.ManyToManyField(Student, verbose_name='协会成员')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE)

    class Meta():
        db_table = 'association'

    def to_dict(self):
        return {
            'association_num': self.association_num,
            'association_name': self.association_name,
            'association_info': self.association_info,
            'association_mail': self.association_mail,
            'association_tel': self.association_tel,
            'association_start': self.association_start,
            'association_join': self.association_join,
            'associaiton_praise': self.association_praise,
            'association_type': self.association_type,
            'association_growth': self.association_growth,
            'academy_id': self.academy_id,
            'apply_status': self.apply_status,
            'TYPE': self.ASSOCIATION_TYPE,
            'STATUS': self.APPLY_STATUS,
        }


# class Department(models.Model):
#     """
#     部门
#     """
#     pass


class AssociationStudent(models.Model):
    """
    社团成员类
    """
    POSITION = (
        (1, '成员'),
        (2, '干事'),
        (3, '副部长'),
        (4, '部长'),
        (5, '副社长'),
        (6, '社长'),
    )
    APPLY_INFO = (
        (1, '待回复'),
        (2, '已加入'),
        (3, '已拒绝'),
    )

    PAY_OPTION = (
        (1, '未缴费'),
        (2, '已缴费'),
        (3, ''),
    )
    association = models.ForeignKey(Association, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    join_time = models.DateField(auto_now_add=True, verbose_name='加入时间')
    student_position = models.IntegerField(choices=POSITION, default=1, verbose_name='职务')
    is_paid = models.IntegerField(choices=PAY_OPTION, default=1, verbose_name='是否缴纳会费')
    apply_to_stu = models.IntegerField(choices=APPLY_INFO, default=1, verbose_name='邀请请求状态')
    apply_to_ass = models.IntegerField(choices=APPLY_INFO, default=1, verbose_name='入团请求状态')
    remark = models.CharField(max_length=500, null=True, verbose_name='成员备注')

    class Meta():
        db_table = 'association_student'


class Activity(models.Model):
    """
    活动类
    """
    STATUS = (
        (1, '已保存但未提交'),
        (2, '待审批'),
        (3, '待补充'),
        (4, '已通过审批'),
        (5, '未通过审批'),
        (6, '预热中'),
        (7, '进行中'),
        (8, '已结束'),
    )
    CONDITIONS = (
        (1, '直接加入'),
        (2, '缴费参与'),
        (3, '校内人员'),
        (4, '团内会员'),
    )
    activity_name = models.CharField(max_length=100, verbose_name='活动名称')
    activity_site = models.CharField(max_length=200, null=True, verbose_name='活动地点')
    activity_start = models.DateTimeField(null=True, verbose_name='开始时间')
    activity_end = models.DateTimeField(null=True, verbose_name='结束时间')
    activity_condition = models.IntegerField(choices=CONDITIONS, default=1, verbose_name='参与条件')
    activity_add = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    join_fee = models.IntegerField(default=0, verbose_name='参与费用')
    activity_praise = models.IntegerField(default=0, verbose_name='活动点赞')
    activity_label = models.IntegerField(default=0, null=True, verbose_name='活动标签')
    activity_remark = models.TextField(null=True, verbose_name='活动备注')
    activity_status = models.IntegerField(choices=STATUS, default=1, verbose_name='活动状态')
    activity_detail = models.TextField(null=True, verbose_name='活动详情')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    students = models.ManyToManyField(Student, verbose_name='参与人员')
    association = models.ForeignKey(Association, on_delete=models.CASCADE)

    class Meta():
        db_table = 'activity'


class ActivityStudent(models.Model):
    """
    社团成员类
    """
    PART = (
        (1, '参与者'),
        (1, '主要参与者'),
        (1, '组织者'),
    )
    SIGN_STATUS = (
        (1, '已报名'),
        (2, '通过报名'),
        (3, '报名被拒绝'),
    )

    AWARDS = (
        (0, '未获奖'),
        (1, '一级奖项'),
        (2, '二级奖项'),
        (3, '三级奖项'),
        (4, '四级奖项'),
    )
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    create_time = models.DateField(auto_now_add=True, verbose_name='创建时间')
    part = models.IntegerField(choices=PART, default=1, verbose_name='角色')
    join_status = models.IntegerField(choices=SIGN_STATUS, default=1, verbose_name='报名状态')
    awards = models.IntegerField(choices=AWARDS, default=0, verbose_name='获奖情况')
    remark = models.CharField(max_length=500, null=True, verbose_name='成员备注')

    class Meta():
        db_table = 'activity_student'


class Gallery(models.Model):
    """
    相册类
    """
    PERMISSION = {
        (1, '所有人可见'),
        (2, '社团内部可见'),
        (3, '仅自己可见'),
    }
    gallery_name = models.CharField(max_length=100, null=False, verbose_name='相册名称')
    create_time = models.DateField(auto_now_add=True, null=True, verbose_name='创建时间')
    describe = models.TextField(null=True, verbose_name='相册描述')
    association = models.ForeignKey(Association, null=True, on_delete=models.CASCADE, verbose_name="社团")
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE, verbose_name="学生")
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE, verbose_name="活动")
    permission = models.IntegerField(choices=PERMISSION, verbose_name="权限")

    class Meta():
        db_table = "gallery"

    def to_dict(self):
        return {
            'permission': self.permission,
            'gallery_name': self.gallery_name,
            'create_time': self.create_time,
            'association_id': self.association_id,
            'activity_id': self.activity_id,
            'student_id': self.student_id,
            'describe': self.describe,
            'head_photo':self.userfiles_set.filter(file_type=1).all()[0].file.name if self.userfiles_set.filter(file_type=1).all() else ''
        }


def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, instance.relative_path, filename])


class UserFiles(models.Model):
    """
    文件类
    """
    FILE_TYPE = (
        (1, '头像'),
        (2, '审批文件'),
        (3, '相册'),
        (4, '图片'),
        (5, '普通'),
    )
    student = models.ForeignKey(Student, null=True, verbose_name='学生', on_delete=models.CASCADE)
    association = models.ForeignKey(Association, null=True, verbose_name='社团', on_delete=models.CASCADE)
    gallery = models.ForeignKey(Gallery, null=True, verbose_name='相册', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True, verbose_name='活动', on_delete=models.CASCADE)
    file_type = models.IntegerField(choices=FILE_TYPE, default=5, verbose_name='文件说明')
    relative_path = models.CharField(max_length=2000, default='', verbose_name='相对路径')
    filename = models.CharField(max_length=500, null=True, verbose_name='文件名字')
    file = models.FileField(upload_to=upload_to, max_length=1000, null=True, verbose_name='文件')
    imagefile = models.ImageField(upload_to=upload_to, max_length=1000, null=True, verbose_name='图片文件')
    file_date = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta():
        db_table = 'userfiles'

    def to_dict(self):
        return {
            'student_id': self.student_id,
            'association_id': self.association_id,
            'gallery_id': self.gallery_id,
            'activity_id': self.activity_id,
            'file_type': self.file_type,
            'filename': self.filename,
            'path': self.relative_path + '/' + self.filename if self.imagefile else '',
            'file_date': self.file_date.strftime('%Y-%m-%d %H:%M:%S'),
            'file_id': self.id
        }

    def modify_file(self, relativity_path, file=None, imagefile=None):
        os.removedirs(MEDIA_ROOT + '/' + self.relative_path)
        self.relative_path = relativity_path
        if file:
            self.filename = file.name
            self.file = file
        elif imagefile:
            self.filename = imagefile.name
            self.imagefile = imagefile
