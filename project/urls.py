from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^signup1/$', views.signup1, name='signup1'),
    url(r'^signup2/$', views.signup2, name='signup2'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^already/$', views.already, name='already'),
    url(r'^already3/$', views.already3, name='already3'),
    url(r'^alreadyvoted/$', views.alreadyvoted, name='alreadyvoted'),
    url(r'^nicetry/$', views.nicetry, name='nicetry'),
    url(r'^newstory/$', views.newstory, name='newstory'),
    url(r'^newstory1/$', views.newstory1, name='newstory1'),
    url(r'^register_activate/activation/',views.activate, name='activation'),
    url(r'^vote/(?P<Submission_id>[0-9]+)/$', views.vote, name='vote'),
    url(r'^(?P<slug>.+)/$', views.story, name='story'),

]
