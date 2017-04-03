from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup1/$', views.signup1, name='signup1'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^story1/$', views.story1contrib, name='story1'),
    url(r'^story1read/$', views.story1read, name='story1read'),
    url(r'^story1submit/$', views.story1submit, name='story1submit'),
    url(r'^already/$', views.already, name='already'),
]
