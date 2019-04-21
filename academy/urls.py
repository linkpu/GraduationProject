from django.conf.urls import url

from academy import views

urlpatterns = [
    url(r'^province_change/(\d+)/$', views.province_change, name='province_change'),
    url(r'^city_change/(\d+)/$', views.city_change, name='city_change'),
    url(r'^school_area_change/(\d+)/$', views.school_area_change, name='school_area_change'),
    url(r'^school_change/(\d+)/$', views.school_change, name='school_change'),
    # url(r'^/$', views., name=''),

]