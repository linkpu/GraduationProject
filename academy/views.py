from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from academy.models import Area, Academy


def province_change(request, province_id):
    if request.method == 'GET':
        # 查找该省内的所有城市
        cities = list(Area.objects.filter(parent_id=province_id).all())
        # 获取到第一个城市对应的区
        areas_ = list(Area.objects.filter(parent_id=cities[0].code_id).all())
        # 将对象转换为json数据
        for index in range(len(cities)):
            cities[index] = cities[index].to_dict()
        for index in range(len(areas_)):
            areas_[index] = areas_[index].to_dict()
        # 对结果进行排序
        cities.sort(key=lambda c:c['code_id'])
        areas_.sort(key=lambda a:a['code_id'])
        data = {'code': 200, 'cities': cities, 'areas_': areas_}
        return JsonResponse(data)


def city_change(request, city_id):
    if request.method == 'GET':
        # 查找该市内的所有区
        areas_ = list(Area.objects.filter(parent_id=city_id).all())
        for index in range(len(areas_)):
            areas_[index] = areas_[index].to_dict()
        areas_.sort(key=lambda a:a['code_id'])
        data = {'code': 200, 'areas_': areas_}
        return JsonResponse(data)


def school_area_change(request, province_id):
    if request.method == 'GET':
        # 查找该省内的所有学校
        schools = list(Academy.objects.filter(area_id=province_id))
        # 将学校序列中的学校对象转换为dict
        for index in range(len(schools)):
            schools[index] = schools[index].to_dict()
        return JsonResponse({'code': 200, 'schools': schools})


def school_change(request, school_id):
    if request.method == 'GET':
        # 查找该学校
        academy = Academy.objects.get(pk=school_id)
        # 获取到该学校所有专业
        majors = list(academy.major.all())
        # 将专业序列中的专业对象转换为dict
        for index in range(len(majors)):
            majors[index] = majors[index].to_dict()
        return JsonResponse({'code': 200, 'majors': majors})




# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
# def index(request):
#     if request.method == 'GET':
#         pass
#
#     if request.method == 'POST':
#         pass
#
#
#