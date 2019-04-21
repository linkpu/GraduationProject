from django.http import JsonResponse
from django.shortcuts import render
import random

# Create your views here.
from academy.models import Academy
from utils.functions import check_phone_number


def school_manager(request):
    if request.method == 'GET':
        return render(request, 'admin/school_manager.html')


def update_school(request, id):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        school = Academy.objects.get(pk=id)
        school_pwd = request.POST.get('school_pwd')
        school_tel = request.POST.get('school_tel')
        if check_phone_number(school_tel):
            school.school_tel = school_tel
        else:
            return JsonResponse({'code': 1000, 'msg': '非法的手机号!'})
        if len(school_tel) >= 8:
            school.school_pwd = school_pwd
        else:
            return JsonResponse({'code': 1000, 'msg': '密码长度应不少于8位!'})
        if not school.school_num:
            while True:
                school.school_num = ''
                string = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
                for i in range(8):
                    school.school_num += random.choice(string)
                if not Academy.objects.filter(school_num=school.school_num):
                    break
        school.status = 1
        school.save()
        return JsonResponse({'code': 200})
