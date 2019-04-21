from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
import re
import datetime

from rest_framework import viewsets

from station.forms import StuRegistForm, StuLoginForm
from student.models import Student
from academy.models import Area, Academy, Major

# Create your views here.
from utils.functions import get_code, send_short_message


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')


def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html')


def portfolio(request):
    if request.method == 'GET':
        return render(request, 'portfolio.html')


def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


def pricing(request):
    if request.method == 'GET':
        return render(request, 'pricing.html')


def services(request):
    if request.method == 'GET':
        return render(request, 'services.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        form = StuRegistForm(request.POST)
        code = request.session.get('vercode')
        if code:
            pass
        else:
            return render(request, 'register.html', {'code': 1000, 'code_error': '请先获取验证码'})
        if form.is_valid():
            if form.cleaned_data['vercode'] == code:
                password = make_password(form.cleaned_data['password'])
                Student.objects.create(stu_name=form.cleaned_data['stu_name'],
                                       stu_pwd=password,
                                       stu_tel=form.cleaned_data['stu_tel'])

                del request.session['vercode']
                return HttpResponseRedirect(reverse('station:login'))
            else:
                return render(request, 'register.html', {'code': 1000, 'code_error': '验证码错误'})
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = StuLoginForm(request.POST)
        if form.is_valid():
            # 获取用户对象
            stu = Student.objects.filter(stu_tel=form.cleaned_data['stu_tel']).first()
            if stu:
                if not check_password(form.cleaned_data['password'], stu.stu_pwd):
                    return HttpResponseRedirect(reverse('station:login'))
                request.session['stu_id'] = stu.id
                return HttpResponseRedirect(reverse('station:index'))
            else:
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})


def get_vercode(request):
    if request.method == 'GET':
        stu_tel = request.GET.get('stu_tel')
        restring = "^(13[0-9]|14[579]|15[0-3,5-9]|16[6]|17[0135678]|18[0-9]|19[89])\\d{8}$"
        temp = re.fullmatch(restring, stu_tel)
        if temp:
            stu_tel = temp.string
            vercode = get_code(6)
            # result = send_short_message(stu_tel, vercode)
            request.session['vercode'] = '1234'
            return JsonResponse({'code': 200})
        else:
            return JsonResponse({'code': 1001})


class StudentViewSet(viewsets.ModelViewSet):
    '''
    API端: 查看学生列表
    '''
    queryset = Student.objects.all().order_by('-id')


def login_info(request):
    if request.method == 'GET':
        stu_id = request.session.get('stu_id')
        if stu_id:
            stu = Student.objects.get(pk=stu_id)
            return JsonResponse({'code': 200, 'username': stu.stu_name})
        else:
            return JsonResponse({'code': 1002})


def logout(request):
    if request.method == 'GET':
        del request.session['stu_id']
        return HttpResponseRedirect(reverse('station:index'))


def profile(request):
    # 获取已登录id
    stu_id = request.session.get('stu_id')
    # 获取已登录用户对象
    stu = Student.objects.get(pk=stu_id)
    stu.stu_birth = stu.stu_birth.strftime('%Y-%m-%d')
    if request.method == 'GET':
        # 拿到省级数据
        provinces = list(Area.objects.filter(parent_id=0).all())
        # 将省数据进行排序
        provinces.sort(key=lambda p:p.code_id)
        # 构建返回地区数据结构
        positions = {'areas': [], 'cities': [], 'provinces': provinces}
        # 构建学生籍贯结构
        native = {'area': stu.stu_native, 'city': None, 'province': None}
        # 构建院校信息
        schools = {'schools':[], 'stu_school_majors': []}
        # 判断学生院校信息是否存在
        if stu.academy:
            # 获取同省内所有院校
            schools['schools'] = Academy.objects.filter(area_id=stu.academy.area_id).all()
            # 获取学生该学院的所有专业
            schools['stu_school_majors'] = stu.academy.major.all()
        # 判断学生对象籍贯存在
        if stu.stu_native:
            # 通过学生对象籍贯查找籍贯区级数据并添加到地区数据结构
            positions['areas'] = list(Area.objects.filter(parent_id=stu.stu_native.parent_id).all())
            positions['areas'].sort(key=lambda a:a.code_id)
            # 查询学生籍贯所属市
            city = Area.objects.get(pk=stu.stu_native.parent_id)
            # 查询学生籍贯所属市的同级数据并添加到地区数据结构
            positions['cities'] = list(Area.objects.filter(parent_id=city.parent_id).all())
            positions['cities'].sort(key=lambda c:c.code_id)
            # 查询学生籍贯所属省并添加到地区数据结构
            native['province'] = Area.objects.get(pk=city.parent_id)
            # 向学生籍贯数据结构中添加市级记录
            native['city'] = city
        return render(request, 'profile.html', {'stu': stu, 'positions': positions, 'native': native, 'schools': schools})

    if request.method == 'POST':
        stu_name = request.POST.get('stu_name')
        stu_num = request.POST.get('stu_num')
        stu_birth = request.POST.get('stu_birth')
        stu_sex = request.POST.get('stu_sex')
        stu_tel = request.POST.get('stu_tel')
        stu_mail = request.POST.get('stu_mail')
        stu_motto = request.POST.get('stu_motto')
        area_id = request.POST.get('area_id')
        academy_id = request.POST.get('academy_id')
        major_id = request.POST.get('major_id')
        stu_pwd = request.POST.get('stu_pwd')
        code = request.session.get('vercode')

        if code:
            del request.session['vercode']
        if stu_tel and code:
            stu.stu_tel = stu_tel
        if stu_name:
            stu.stu_name = stu_name
        stu.stu_num = stu_num
        if stu_birth:
            stu.stu_birth = datetime.datetime.strptime(stu_birth, '%Y-%m-%d')
        if stu_sex:
            stu.stu_sex = stu_sex
        restring = r'^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$'
        if stu_mail and re.fullmatch(restring, stu_mail):
            stu.stu_mail = stu_mail
        if stu_motto:
            stu.stu_motto = stu_motto
        if area_id:
            stu.stu_native = Area.objects.get(pk=int(area_id))
        if academy_id:
            stu.academy_id= int(academy_id)
        if major_id:
            stu.major_id = int(major_id)
        if stu_pwd and len(stu_pwd) >= 6:
            stu.stu_pwd = make_password(stu_pwd)
        stu.save()
        return JsonResponse({'code': 200})



# # api
# from django.shortcuts import render
# from django.http import JsonResponse
# from rest_framework.views import APIView
#
#
# class AuthView(APIView):
#
#     def post(self, request, *args, **kwargs):
#         ret = {'code': 1000, 'msg': "登录成功"}
#         stu_tel = request._request.POST.get('stu_tel')
#         pwd = request._request.POST.get('password')
#         stu = Student.objects.filter(stu_tel=stu_tel)
#         if not stu:
#             ret['code'] = 1001
#             ret['msg'] = "用户名不存在"
#         elif not check_password(pwd, stu.stu_pwd):
#             ret['code'] = 1002
#             ret['msg'] = '密码错误'
#
#         return JsonResponse(ret)
