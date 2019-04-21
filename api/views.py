from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView

from academy.models import Area, Academy
from student.models import Student


# 自定义序列化器
class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = '__all__'


@api_view(['GET'])
def student(request):
    queryset = Student.objects.all()
    serializer = StudentSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def student_by_id(request, id):
    queryset = Student.objects.get(pk=id)
    serializer = StudentSerializer(queryset, many=True)
    return JsonResponse(serializer.data, safe=False)


class StudentApiView(ListCreateAPIView):
    querset = Student.objects.all()
    serializer_class = StudentSerializer


# 地区序列
class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'


@api_view(['GET'])
def get_provinces(request):
    provinces = Area.objects.filter(parent_id=0).all()
    serializer = AreaSerializer(provinces, many=True)
    return JsonResponse({'code': 200, 'provinces': serializer.data}, safe=False)


# 院校序列
class AcademySerializer(serializers.ModelSerializer):

    class Meta:
        model = Academy
        fields = '__all__'


@api_view(['GET'])
def school_by_id(request, id):
    school = Academy.objects.get(pk=id)
    serializer = AcademySerializer(school)
    return JsonResponse({'code': 200, 'school': serializer.data}, safe=False)