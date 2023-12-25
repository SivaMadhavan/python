from django.urls import path
from . import views


urlpatterns = [
    path(r'^list', views.patient_list, name='patient_list'),
    path(r'^$', views.patient_create, name='patient_insert'),
    path(r'^(?P<uuid>[A-Za-z0-9-]+)$', views.patient_create, name='patient_update'),
    path(r'^delete/(?P<id>[A-Za-z0-9-]+)$', views.patient_delete, name='patient_delete'),
    path(r'^module3/list/$', views.module_list, name='module_list'),
    path(r'^module3/$', views.module_create, name='module_insert'),
    path(r'^module3/(?P<uuid>[A-Za-z0-9-]+)$', views.module_create, name='module_update'),
    path(r'^module3/delete/(?P<uuid>[A-Za-z0-9-]+)$', views.module_delete, name='module_delete'),
    path(r'^module2/list/$', views.module2_list, name='module2_list'),
    path(r'^module2/$', views.module2_create, name='module2_insert'),
    path(r'^module2/(?P<uuid>[A-Za-z0-9-]+)$', views.module2_create, name='module2_update'),
    path(r'^module2/delete/(?P<uuid>[A-Za-z0-9-]+)$', views.module2_delete, name='module2_delete'),
    path(r'^medical-problems/list/$', views.mp_list, name='mp_list'),
    path(r'^medical-problems/$', views.mp_create, name='mp_insert'),
    path(r'^medical-problems/(?P<uuid>[A-Za-z0-9-]+)$', views.mp_create, name='mp_update'),
    path(r'^medical-problems/delete/(?P<uuid>[A-Za-z0-9-]+)$', views.mp_delete, name='mp_delete'),
    path(r'^result/$', views.result, name='result'),
    # path(r'^download_excel/$', views.download_excel, name='download_excel'),
    # path(r'^download_csv/$', views.download_csv, name='download_csv'),
    # path(r'^download_pdf/$', views.download_pdf, name='download_pdf'),
]