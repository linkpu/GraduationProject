import os
import time

from django import forms
from django.contrib.auth.hashers import check_password, make_password

from academy.models import Academy
from association.models import Association, AssociationStudent, Activity, UserFiles
from student.models import Student
from utils.functions import check_phone_number, check_email, validateTitle
import pinyin
import datetime


class RegisterForm(forms.Form):
    school = forms.CharField(required=True, error_messages={'required': '请选择院校'})
    association_name = forms.CharField(required=True, error_messages={'required': '社团名称必填'})
    password = forms.CharField(required=True, min_length=8, error_messages={'required': '密码必填',
                                                              'min_length': '密码长度不少于8位'})
    association_info = forms.CharField(required=False)
    confirm_pwd = forms.CharField(required=True, error_messages={'required': '确认密码必填'})
    association_tel = forms.CharField(required=True, error_messages={'required': '联系电话必填'})
    association_type = forms.CharField(required=True, error_messages={'required': '请选择社团类型'})
    association_mail = forms.CharField(required=False)
    apply_file = forms.FileField(required=False)

    def clean(self):
        if self.cleaned_data.get('school'):
            if Association.objects.filter(academy_id=self.cleaned_data.get('school')).filter(association_name=self.cleaned_data.get('association_name')).all():
                raise forms.ValidationError({'association_name': '该名称已存在'})

            if self.cleaned_data.get('confirm_pwd') != self.cleaned_data.get('password'):
                raise forms.ValidationError({'confirm_pwd': '两次密码不一致'})

            if Academy.objects.get(pk=int(self.cleaned_data.get('school'))).status != 1:
                raise forms.ValidationError({'school': '该学校暂未注册或已停用本平台'})

            if not check_phone_number(self.cleaned_data.get('association_tel')):
                raise forms.ValidationError({'association_tel': '请输入合法的手机号码'})

            if self.cleaned_data.get('association_mail'):
                if not check_email(self.cleaned_data.get('association_mail')):
                    raise forms.ValidationError({'association_mail': '请输入合法的邮箱账号'})
        return self.cleaned_data


class LoginForm(forms.Form):
    school = forms.CharField(required=True, error_messages={'required': '请选择学校'})
    association_name = forms.CharField(required=False)
    association_num = forms.CharField(required=False)
    association_pwd = forms.CharField(required=True, error_messages={'required': '请输入密码'})
    submit = forms.CharField(required=False)

    def clean(self):
        if (not self.cleaned_data.get('association_name')) and (not self.cleaned_data.get('association_num')):
            raise forms.ValidationError({'submit': '请填写登录信息'})

        if self.cleaned_data.get('association_name') and self.cleaned_data.get('association_num'):
            if not self.cleaned_data.get('school'):
                raise forms.ValidationError({'school': '请选择院校'})
            if Academy.objects.get(pk=int(self.cleaned_data.get('school'))).status != 1:
                raise forms.ValidationError({'school': '该院校已停用本平台'})
            user1 = Association.objects.filter(academy_id=int(self.cleaned_data.get('school'))).filter(
                association_name=self.cleaned_data.get('association_name')).all()[0]
            user2 = Association.objects.filter(association_num=self.cleaned_data.get('association_num')).all()
            if not user1:
                raise forms.ValidationError({'association_name': '未定位到该社团名称'})
            if not user2 or user2[0].academy.status != 1:
                raise forms.ValidationError({'association_num': '未定位到该社团编号或该院校已被停用'})
            if user1 != user2[0]:
                raise forms.ValidationError({'association_num': '该社团名称定位与编号定位定位不匹配(Tips: 可单独使用名称定位或社团编码登录)'})
            self.cleaned_data['user'] = user1

            return self.cleaned_data

        if self.cleaned_data.get('association_name'):
            if not self.cleaned_data.get('school'):
                raise forms.ValidationError({'school': '请选择院校'})

            if Academy.objects.get(pk=int(self.cleaned_data.get('school'))).status != 1:
                raise forms.ValidationError({'school': '该院校不可用'})

            user = Association.objects.filter(academy_id=int(self.cleaned_data.get('school'))).filter(
                association_name=self.cleaned_data.get('association_name')).all()
            if not user or user[0].academy.status != 1:
                raise forms.ValidationError({'association_name': '未定位到该社团名称'})
            self.cleaned_data['user'] = user[0]
            return self.cleaned_data

        if self.cleaned_data.get('association_num'):
            user = Association.objects.filter(association_num=self.cleaned_data.get('association_num')).all()
            if not user or user[0].academy.status != 1:
                raise forms.ValidationError({'association_name': '未定位到该编号或所属院校不可用'})
            self.cleaned_data['user'] = user[0]
            return self.cleaned_data


class NewMemberForm(forms.Form):
    association_id = forms.CharField(required=True, error_messages={'required': '社团登录信息错误'})
    member_name = forms.CharField(required=True, error_messages={'required': '请填写姓名'})
    member_sex = forms.CharField(required=True, error_messages={'required': '请填写性别信息'})
    member_mail = forms.CharField(required=False)
    member_sno = forms.CharField(required=True, error_messages={'required': '请填写学号'})
    member_tel = forms.CharField(required=True, error_messages={'required': '请填写手机'})
    member_pos = forms.CharField(required=False)
    member_remark = forms.CharField(required=False)
    member_submit = forms.CharField(required=False)

    def clean(self):
        stu = Student.objects.filter(stu_tel=self.cleaned_data.get('member_tel')).all()
        ass = Association.objects.get(pk=int(self.cleaned_data.get('association_id')))
        num_stu = Student.objects.filter(academy_id=ass.academy_id).filter(stu_num=self.cleaned_data.get('member_sno')).all()
        if stu:
            if AssociationStudent.objects.filter(student=stu[0]).filter(association_id=int(self.cleaned_data.get('association_id'))):
                raise forms.ValidationError({'member_tel': '该手机号已经在你的社团中'})
            else:
                if stu[0].academy_id != ass.academy_id:
                    raise forms.ValidationError({'member_tel': '该手机号用户已存在且不属于本校'})
                else:
                    if num_stu and num_stu[0].stu_tel != stu[0].stu_tel:
                        raise forms.ValidationError({'member_sno': '该学号已被本校学生注册'})
                    else:
                        if self.cleaned_data.get('member_mail'):
                            if not check_email(self.cleaned_data.get('member_mail')):
                                raise forms.ValidationError({'member_mail': '请填写正确的邮箱格式'})
                        AssociationStudent.objects.create(
                            association_id=ass.id,
                            student_id=stu[0].id,
                            student_position=1,
                            remark=self.cleaned_data.get('member_remark'),
                            apply_to_stu=1,
                            apply_to_ass=2
                        )
        else:
            if not check_phone_number(self.cleaned_data.get('member_tel')):
                raise forms.ValidationError({'member_tel': '请填写正确的手机号码'})
            if self.cleaned_data.get('member_mail'):
                if not check_email(self.cleaned_data.get('member_mail')):
                    raise forms.ValidationError({'member_mail': '请填写正确的邮箱格式'})
            else:
                if num_stu:
                    raise forms.ValidationError({'member_sno': '该学号已被本校学生注册'})
                else:
                    student = Student.objects.create(
                        stu_tel=self.cleaned_data.get('member_tel'),
                        stu_name=self.cleaned_data.get('member_name'),
                        stu_mail=self.cleaned_data.get('member_mail'),
                        stu_num=self.cleaned_data.get('member_sno'),
                        stu_sex=self.cleaned_data.get('member_sex'),
                        academy_id=ass.academy_id,
                        stu_pwd=make_password(pinyin.get(ass.association_name, format='strip')),

                    )
                    try:
                        AssociationStudent.objects.create(
                            association_id=ass.id,
                            student_id=student.id,
                            student_position=1,
                            remark=self.cleaned_data.get('member_remark'),
                            apply_to_stu=2,
                            apply_to_ass=2
                        )
                    except Exception as e:
                        student.delete()
                        raise forms.ValidationError({'member_submit': '数据存储出错, 请检查数据'})
        return self.cleaned_data


class CreateActivityForm(forms.Form):
    activity_id = forms.CharField(required=False)
    association_id = forms.CharField(required=True)
    activity_name = forms.CharField(required=True, error_messages={'required': '请填写活动名称'})
    activity_start = forms.CharField(required=True, error_messages={'required': '请选择开始时间'})
    activity_end = forms.CharField(required=True, error_messages={'required': '请选择结束时间'})
    activity_site = forms.CharField(required=True, error_messages={'required': '请输入活动地点'})
    activity_lable = forms.CharField(required=False)
    activity_detail = forms.CharField(required=False)
    activity_remark = forms.CharField(required=False)
    activity_condition = forms.CharField(required=True, error_messages={'required': '请选择参与条件'})
    activity_file = forms.FileField(required=False)
    join_fee = forms.CharField(required=False)
    submit_options = forms.CharField(required=False)
    submit_code = forms.CharField(required=True)
    submit_unique = forms.CharField(required=True)
    submit = forms.CharField(required=False)

    def clean(self):
        data = self.cleaned_data
        if data.get('submit_unique') == data.get('submit_code'):
            if int(data.get('activity_condition')) == 2:
                if not data.get('join_fee'):
                    raise forms.ValidationError({'join_fee': '请填写参与金额'})
                else:
                    data['join_fee'] = int(data['join_fee'])
            else:
                data['join_fee'] = 0

            if not data.get('activity_site'):
                raise forms.ValidationError({'activity_site': '活动地点不能为空'})

            if int(data.get('submit_options')) == 1:
                activity_status = 2
            elif int(data.get('submit_options')) == 3:
                activity_status = 7
            else:
                activity_status = 1
            activity_start = datetime.datetime.strptime(data.get('activity_start'), '%Y-%m-%d %H:%M')
            activity_end = datetime.datetime.strptime(data.get('activity_end'), '%Y-%m-%d %H:%M')
            if (activity_start - datetime.datetime.now()).days < 0:
                raise forms.ValidationError({'activity_start': '开始时间不能在当前时间之前'})
            if (activity_end - activity_start).days < 0:
                raise forms.ValidationError({'activity_end': '结束时间不能在开始时间之前'})

            if data.get('activity_id'):
                activity = Activity.objects.get(pk=int(data.get('activity_id')))
                if activity.activity_status == 4:
                    activity.activity_status = 6
                elif activity.activity_status == 6:
                    activity.activity_status = 7
                elif activity.activity_status == 7:
                    activity.activity_status = 8
                else:
                    activity.activity_name = data.get('activity_name')
                    activity.activity_site = data.get('activity_site')
                    activity.activity_start = activity_start
                    activity.activity_end = activity_end
                    activity.activity_conndition = int(data.get('activity_condition'))
                    activity.join_fee = data.get('join_fee'),
                    activity.activity_label = data.get('activity_label')
                    activity.activity_detail = data.get('activity_detail')
                    activity.activity_status = activity_status
                    activity.activity_remark = data.get('activity_remark')
                activity.save()
            else:
                activity = Activity.objects.create(
                    activity_name=data.get('activity_name'),
                    activity_site=data.get('activity_site'),
                    activity_start=activity_start,
                    activity_end=activity_end,
                    activity_conndition=int(data.get('activity_condition')),
                    join_fee=data.get('join_fee'),
                    activity_label=data.get('activity_label'),
                    activity_detail=data.get('activity_detail'),
                    activity_status=activity_status,
                    activity_remark=data['activity_remark'],
                    association_id=int(data['association_id'])
                )
                activity_file = activity.userfiles_set.all()
                if data.get('activity_file') and activity_file:
                    os.removedirs(activity_file[0].relative_path)
                    activity_file[0].relative_path = activity.association.academy.school_name + '/association/' + activity.association.association_name + '/activity_apply_files/' + str(int(time.time()))
                    activity_file[0].filename = data['activity_file'].name
                    activity_file[0].file = data['activity_file']
                    activity_file[0].save()

            if data.get('activity_file'):
                data['activity_file'].name = validateTitle(data['activity_file'].name)
                UserFiles.objects.create(
                    activity_id=activity.id,
                    relative_path=activity.association.academy.school_name + '/association/' + activity.association.association_name + '/activity_apply_files/' + str(int(time.time())),
                    filename=data['activity_file'].name,
                    file=data['activity_file']
                )
            self.cleaned_data['activity'] = activity
            return self.cleaned_data
        else:
            raise forms.ValidationError({'submit': '此表单已经提交过'})

