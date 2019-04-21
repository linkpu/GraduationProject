from django.conf.urls import url

from association import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^dynamic/$', views.dynamic, name='dynamic'),
    url(r'^about/$', views.about, name='about'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    # url(r'^/$', views., name=''),
    # ------------------社团后台模块--------------------
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^is_login/$', views.is_login, name='is_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^member_list/(\d+)?/?$', views.member_list, name='member_list'),
    url(r'^new_member/$', views.new_member, name='new_member'),
    url(r'^create_activity/(\d+)?/?$', views.create_activity, name='create_activity'),
    url(r'^activity_list/(\d+)?/?$', views.activity_list, name='activity_list'),
    url(r'^gallery_list/(\d+)?/?$', views.gallery_list, name='gallery_list'),
    url(r'^gallery/(\d+)?/?$', views.gallery, name='gallery'),
    # url(r'^make_gallery/$', views.make_gallery, name='make_gallery'),
    # url(r'^/$', views., name=''),
]