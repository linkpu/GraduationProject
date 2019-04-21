from django import forms
from student.models import Student


class StuRegistForm(forms.Form):
    '''
    用户注册验证表单
    '''
    stu_name = forms.CharField(required=True, max_length=20,
                                error_messages={'required': '用户名必填',
                                                'max_length': '用户名长度不能超过20个字符'})

    password = forms.CharField(required=True, min_length=8, max_length=20,
                               error_messages={'required': '密码必填',
                                               'min_length': '密码长度不少于8位',
                                               'max_length': '密码长度不超过20位'})

    repassword = forms.CharField(required=True, min_length=8, max_length=20,
                               error_messages={'required': '确认密码必填'})

    stu_tel = forms.CharField(required=True, min_length=11, max_length=11,
                          error_messages={'required': '手机必填',
                                          'max_length': '手机账号为11位数字',
                                          'min_length': '手机账号为11位数字'})

    vercode = forms.CharField(required=True, min_length=4, max_length=4,
                              error_messages={
                                  'required': '请输入验证码',
                                  'max_length': '验证码为四位字符',
                                  'min_length': '验证码为四位字符'
                              })

    # code = forms.CharField()

    def clean(self):
        stu_tel = self.cleaned_data.get('stu_tel')
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')

        # 校验用户名是否已经注册过
        student = Student.objects.filter(stu_tel=stu_tel)
        if student:
            raise forms.ValidationError({'stu_tel': '手机号已被注册'})
        # 校验两次密码是否一致
        if repassword != password:
            raise forms.ValidationError({'repassword': '两次输入密码不一致'})
        # 校验验证码是否正确
        # vercode = self.cleaned_data.get('vercode')
        # code = self.code
        # if vercode != code:
        #     raise forms.ValidationError({'vercode': '验证码错误'})
        return self.cleaned_data


class StuLoginForm(forms.Form):
    stu_tel = forms.CharField(required=True, min_length=11, max_length=11,
                              error_messages={'required': '手机必填',
                                              'max_length': '手机账号为11位数字',
                                              'min_length': '手机账号为11位数字'})

    password = forms.CharField(required=True, min_length=8, max_length=20,
                          error_messages={'required': '密码必填',
                                          'max_length': '密码长度不能超过20字符',
                                          'min_length': '密码长度不能少于8个字符'})

    def clean(self):
        # 验证用户名是否注册
        user = Student.objects.filter(stu_tel=self.cleaned_data.get('stu_tel')).first()
        if not user:
             raise forms.ValidationError({'stu_tel': '该用户没有注册, 请先注册'})
        return self.cleaned_data