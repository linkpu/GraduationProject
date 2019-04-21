import datetime
import os
import random
import time

from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
import pinyin

from GraduationProject.settings import PAGE_NUM_STU, PAGE_NUM_ACT, PAGE_NUM_GLR
from academy.models import Academy
from association import forms
from association.forms import NewMemberForm, CreateActivityForm
from association.models import Association, UserFiles, AssociationStudent, Activity, Gallery
from student.models import Student
from utils.functions import excel_to_stu, check_phone_number, get_rand_str, validateTitle


def index(request):
    if request.method == 'GET':
        return render(request, 'association_front/index.html')


def dynamic(request):
    if request.method == 'GET':
        return render(request, 'association_front/dynamic.html')

def about(request):
    if request.method == 'GET':
        return render(request, 'association_front/about_us.html')


def gallery(request):
    if request.method == 'GET':
        return render(request, 'association_front/gallery.html')


def contacts(request):
    if request.method == 'GET':
        return render(request, 'association_front/contacts.html')


# -------------------------社团后台模块-------------------------------
def index(request):
    if request.method == 'GET':
        return render(request, 'association/index.html')

    if request.method == 'POST':
        pass


def login(request):
    if request.method == 'GET':
        return render(request, 'association/signin.html')

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            association = data['user']
            request.session['association_id'] = association.id
            return HttpResponseRedirect(reverse('association:index'))
        else:
            return render(request, 'association/signin.html', {'form': form})


def register(request):
    if request.method == 'GET':
        return render(request, 'association/signup.html', {'type': Association.ASSOCIATION_TYPE})

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            association_num = ''
            while True:
                string = 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890'
                for i in range(6):
                    association_num += random.choice(string)
                if not Association.objects.filter(association_num=association_num):
                    break
            association_data = {
                'association_num': association_num,
                'association_pwd': make_password(data['password']),
                'association_name': data['association_name'],
                'association_info': data['association_info'],
                'association_mail': data['association_mail'],
                'association_tel': data['association_tel'],
                'association_type': int(data['association_type']),
                'academy': Academy.objects.get(pk=int(data['school']))
            }
            association = Association.objects.create(**association_data)
            apply_file = data['apply_file']
            if apply_file:
                file_data = {
                    'association': association,
                    'relative_path': Academy.objects.get(pk=int(data['school'])).school_name + '/association/' + association.association_name + '/applyFiles/'+ str(int(time.time())),
                    'filename': apply_file.name,
                    'file': apply_file
                }
                UserFiles.objects.create(**file_data)
            return HttpResponseRedirect(reverse('association:login'))
        else:
            return render(request, 'association/signup.html', {'form': form, 'type': Association.ASSOCIATION_TYPE})


def is_login(request):
    if request.method == 'GET':
        association_id = request.session.get('association_id')
        if association_id:
            association = Association.objects.get(pk=int(association_id))
            return JsonResponse({'code': 200, 'associaiton_id': association_id, 'association_name': association.association_name})
        else:
            return JsonResponse({'code': 1000})


def logout(request):
    if request.method == 'GET':
        association_id = request.session.get('association_id')
        if association_id:
            del request.session['association_id']
        return JsonResponse({'code': 200})


def member_list(request, page=1):
    if request.method == 'GET':
        association_id = request.session.get('association_id')
        if association_id:
            members = Association.objects.get(pk=int(association_id)).associationstudent_set.all()
            paginator = Paginator(members, PAGE_NUM_STU)
            page_data = paginator.page(int(page))
            if int(page) <= 3:
                previous = [i for i in range(1, int(page))]
            else:
                previous = [i for i in range(int(page)-2, int(page))]
            if paginator.num_pages - int(page) >= 2:
                tails = [i for i in range(int(page)+1, int(page)+3)]
            else:
                tails = [i for i in range(int(page)+1, paginator.num_pages+1)]
        return render(request, 'association/user-list.html', {'page_data': page_data,
                                                              'APPLY_INFO': AssociationStudent.APPLY_INFO,
                                                              'previous': previous, 'tails': tails})

    if request.method == 'POST':
        pass


def new_member(request):
    if request.method == 'GET':
        return render(request, 'association/new-user.html', {
            'association_id': request.session.get('association_id'),
            'positions': AssociationStudent.POSITION})

    if request.method == 'POST':
        members_file = request.FILES.get('members_file')
        if members_file:
            association_id = request.session.get('association_id')
            if association_id:
                association = Association.objects.get(pk=int(association_id))
                file = UserFiles.objects.create(
                    association_id=int(association_id),
                    relative_path=association.academy.school_name + '/association/' + association.association_name + '/memberFiles/' + str(int(time.time())),
                    filename=members_file.name,
                    file=members_file
                )
                member_list = excel_to_stu(file.file.name)

                member_errors = []
                member_success = []
                for member in member_list:
                    member_data = {
                        'association_id': association_id,
                        'member_name': member.get('name'),
                        'member_sex': 'male' if member.get('sex') == '男' else 'female',
                        'member_sno': member.get('sno'),
                        'member_tel': member.get('tel'),
                        'member_remark': member.get('remark'),
                    }
                    form = NewMemberForm(member_data)
                    if form.is_valid():
                        member_success.append(member)
                    else:
                        member['error'] = form.errors
                        member_errors.append(member)
                return render(request, 'association/new-user.html', {
                    'association_id': association_id,
                    'positions': AssociationStudent.POSITION,
                    'member_errors': member_errors,
                    'member_success': member_success
                })
        else:
            form = NewMemberForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect(reverse('association:member_list'))
            else:
                return render(request, 'association/new-user.html', {
                    'association_id': request.session.get('association_id'),
                    'positions': AssociationStudent.POSITION,
                    'form': form
                })


def create_activity(request, act_id):
    join_conditions = Activity.CONDITIONS
    status = Activity.STATUS
    association_id = request.session.get('association_id')
    submit_code = get_rand_str(20)
    submit_unique = request.session.get('submit_unique')
    request.session['submit_unique'] = submit_code
    activities = Association.objects.get(pk=int(association_id)).activity_set.filter(
        activity_start__year=datetime.datetime.now().year).order_by('-activity_start').all()
    if request.method == 'GET':
        if act_id:
            activity = Activity.objects.get(pk=int(act_id))
            activity.activity_start = activity.activity_start.strftime('%Y-%m-%d %H:%M')
            activity.activity_end = activity.activity_end.strftime('%Y-%m-%d %H:%M')
        else:
            activity = None
        return render(request, 'association/new-activity.html', {'join_conditions': join_conditions,
                                                                 'association_id': association_id,
                                                                 'submit_code': submit_code,
                                                                 'activities': activities,
                                                                 'activity': activity
                                                                 })

    if request.method == 'POST':
        data = {
            'activity_id': request.POST.get('activity_id'),
            'association_id': request.POST.get('association_id'),
            'activity_name': request.POST.get('activity_name'),
            'activity_start': request.POST.get('activity_start'),
            'activity_end': request.POST.get('activity_end'),
            'activity_site': request.POST.get('activity_site'),
            'activity_lable': request.POST.get('activity_lable'),
            'activity_detail': request.POST.get('activity_detail'),
            'activity_remark': request.POST.get('activity_remark'),
            'activity_condition': request.POST.get('activity_condition'),
            'join_fee': request.POST.get('join_fee'),
            'submit_options': request.POST.get('submit_options'),
            'submit_code': request.POST.get('submit_code'),
            'submit_unique': submit_unique,
            'submit': request.POST.get('submit')
        }
        form = CreateActivityForm(data, request.FILES)
        if form.is_valid():
            activity = form.cleaned_data.get('activity')
            activity.activity_start = activity.activity_start.strftime('%Y-%m-%d %H:%M')
            activity.activity_end = activity.activity_end.strftime('%Y-%m-%d %H:%M')
            return render(request, 'association/new-activity.html', {'activity': activity,
                                                                     'join_conditions': join_conditions,
                                                                     'submit_code': submit_code,
                                                                     'status': status, 'association_id': association_id,
                                                                     'activities': activities
                                                                     })
        else:
            return render(request, 'association/new-activity.html', {'join_conditions': join_conditions,'form': form,
                                                                     'status': status, 'association_id': association_id,
                                                                     'submit_code': submit_code,
                                                                     'activities': activities
                                                                     })


def activity_list(request, page=1):
    if request.method == 'GET':
        association_id = request.session.get('association_id')
        join_conditions = Activity.CONDITIONS
        status = Activity.STATUS
        if association_id:
            activities = Association.objects.get(pk=int(association_id)).activity_set.all()
            paginator = Paginator(activities, PAGE_NUM_ACT)
            page_data = paginator.page(int(page))
            if int(page) <= 3:
                previous = [i for i in range(1, int(page))]
            else:
                previous = [i for i in range(int(page)-2, int(page))]
            if paginator.num_pages - int(page) >= 2:
                tails = [i for i in range(int(page)+1, int(page)+3)]
            else:
                tails = [i for i in range(int(page)+1, paginator.num_pages+1)]
        return render(request, 'association/activity-list.html', {'page_data': page_data,
                                                              'join_conditions': join_conditions,
                                                              'status': status,
                                                              'previous': previous, 'tails': tails})

    if request.method == 'POST':
        pass


def gallery_list(request, page):
    if not page:
        page = 1
    association_id = request.session.get('association_id')
    association = Association.objects.get(pk=int(association_id))
    if request.method == 'GET':
        permissions = Gallery.PERMISSION
        galleries = association.gallery_set.all()
        for g in galleries:
            f = g.userfiles_set.filter(file_type=1).all()
            g.head_photo = f[0].relative_path + '/' + f[0].filename if f else None
        paginator = Paginator(galleries, 50)
        page_data = paginator.page(int(page))
        if int(page) <= 3:
            previous = [i for i in range(1, int(page))]
        else:
            previous = [i for i in range(int(page) - 2, int(page))]
        if paginator.num_pages - int(page) >= 2:
            tails = [i for i in range(int(page) + 1, int(page) + 3)]
        else:
            tails = [i for i in range(int(page) + 1, paginator.num_pages + 1)]
        return render(request, 'association/gallery.html', {'permissions': permissions,
                                                            'page_data': page_data,
                                                            'previous': previous, 'tails': tails
                                                            })

    if request.method == 'POST':
        activity_id = request.POST.get('activity_id')
        gallery_id = request.POST.get('gallery_id')
        gallery_name = request.POST.get('gallery_name')
        gallery_permission = request.POST.get('gallery_permission')
        gallery_describe = request.POST.get('gallery_describe')
        gallery_header = request.FILES.get('head_photo')
        if activity_id == 'none':
            activity_id = None
        if not gallery_name:
            return JsonResponse({'code': 1000, 'msg': '相册名称不能为空'})
        if Gallery.objects.filter(association_id=int(association_id)).filter(gallery_name=gallery_name):
            return JsonResponse({'code': 1000, 'msg': '该相册名称已存在'})
        if gallery_id:
            gallery = Gallery.objects.get(pk=int(gallery_id))
            gallery.gallery_name = gallery_name
            gallery.describe = gallery_describe
            gallery.permission = int(gallery_permission)
        else:
            gallery = Gallery.objects.create(
                gallery_name=gallery_name,
                association_id=int(association_id),
                describe=gallery_describe,
                permission=int(gallery_permission),
            )
        if activity_id:
            gallery.activity_id = int(activity_id)
        gallery.save()
        if gallery_header:
            gallery_header.name = validateTitle(gallery_header.name)
            relative_path = association.academy.school_name + '/association/' + association.association_name + '/gallery/' + gallery_name + '/headPhoto/' + str(int(time.time()))
            gallery_head_file = gallery.userfiles_set.filter(file_type=1).all()
            if gallery_head_file:
                os.removedirs(gallery_head_file[0].relative_path)
                gallery_head_file[0].relative_path = relative_path
                gallery_head_file[0].filename = gallery_header.name
                gallery_head_file[0].file = gallery_header
                gallery_head_file[0].save()
            else:
                UserFiles.objects.create(
                    gallery_id=gallery.id,
                    relative_path=relative_path,
                    filename=gallery_header.name,
                    imagefile=gallery_header,
                    file_type=1
                )
        gallery = gallery.to_dict()
        return HttpResponseRedirect(reverse('association:gallery'))


def gallery(request, g_id):
    gallery = Gallery.objects.get(pk=int(g_id))
    if request.method == 'GET':
        images = list(gallery.userfiles_set.filter(file_type=3))
        for i in range(len(images)):
            images[i] = images[i].to_dict()
        return JsonResponse({'code': 200, 'images': images, 'gallery_name': gallery.gallery_name})

    if request.method == 'POST':
        photo = request.FILES.get('photo')
        photo.name = validateTitle(photo.name)
        img = UserFiles.objects.create(
            gallery_id=int(g_id),
            file_type=3,
            relative_path=gallery.association.academy.school_name + '/association/' + gallery.association.association_name + '/gallery/' + gallery.gallery_name + '/photos/' + str(int(time.time())),
            filename=photo.name,
            imagefile=photo
        )
        return JsonResponse({'code': 200, 'photo': img.to_dict()})

#
# def register(request):
#     if request.method == 'GET':
#         return render(request, 'association/signup.html')
#
#     if request.method == 'POST':
#         pass
#
#
# def register(request):
#     if request.method == 'GET':
#         return render(request, 'association/signup.html')
#
#     if request.method == 'POST':
#         pass
#