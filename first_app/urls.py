from django.conf.urls import url
from first_app import views

#template tagging
app_name = 'first_app'

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^relative/$', views.related, name='relative'),
    url(r'^other/$', views.other, name='other'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/', views.user_login, name='user_login'),
]
