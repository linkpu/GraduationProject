from django.conf.urls import url

from api import views
from api.views import StudentApiView

urlpatterns = [
    # url(r'^student/$', views.student, name='student'),
    url(r'^student/$', views.student, name='student'),
    url(r'^student_by_name/<int:id>/$', StudentApiView.as_view(), name='student_by_name'),
    url(r'^get_provinces/$', views.get_provinces, name='get_provinces'),
    url(r'^school_by_id/(\d+)/$', views.school_by_id, name='school_by_id'),
    # url(r'^/$', views., name=''),
]