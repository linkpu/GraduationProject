from django.conf.urls import url

from manager import views

urlpatterns = [
    url(r'^school_manager/$', views.school_manager, name='school_manager'),
    url(r'^update_school/(\d+)/$', views.update_school, name='update_school'),
    # url(r'^/$', views., name=''),
]