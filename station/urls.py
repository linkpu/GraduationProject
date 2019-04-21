from django.conf.urls import url

from station import views

urlpatterns = [
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^index/$', views.index, name='index'),
    url(r'^portfolio/$', views.portfolio, name='portfolio'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^services/$', views.services, name='services'),
    url(r'^pricing/$', views.pricing, name='pricing'),
    url(r'^get_vercode/$', views.get_vercode, name='get_vercode'),
    url(r'^login_info/$', views.login_info, name='login_info'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    # url(r'^/$', views., name=''),
]