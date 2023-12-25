from django.urls import path, include
from django.contrib import admin
from . import views
urlpatterns = [
    path(r'^$', views.index_redirect, name='index_redirect'),
    path(r'^patient/', include('app.urls')),
    path(r'^admin/', admin.site.urls),
]
