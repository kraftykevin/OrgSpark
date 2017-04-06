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
    url(r'^register_activate/activation/',views.activate, name='activation'),
    # above are ones that don't need to be copied.
    url(r'^story1/$', views.story1contrib, name='story1'),
    url(r'^story1read/$', views.story1read, name='story1read'),
    url(r'^story1submit/$', views.story1submit, name='story1submit'),
    url(r'^prompt1/$', views.prompt1, name='prompt1'),
    url(r'^story1/vote1/(?P<suba_id>[0-9]+)/$', views.vote1, name='vote1'),
    #here are the bad urls that need DRY
    url(r'^story2/$', views.story2contrib, name='story2'),
    url(r'^story2read/$', views.story2read, name='story2read'),
    url(r'^story2submit/$', views.story2submit, name='story2submit'),
    url(r'^prompt2/$', views.prompt2, name='prompt2'),
    url(r'^story2/vote2/(?P<subb_id>[0-9]+)/$', views.vote2, name='vote2'),
    # next
    url(r'^story3/$', views.story3contrib, name='story3'),
    url(r'^story3read/$', views.story3read, name='story3read'),
    url(r'^story3submit/$', views.story3submit, name='story3submit'),
    url(r'^prompt3/$', views.prompt3, name='prompt3'),
    url(r'^story3/vote3/(?P<subc_id>[0-9]+)/$', views.vote3, name='vote3'),
    # next
    url(r'^story4/$', views.story4contrib, name='story4'),
    url(r'^story4read/$', views.story4read, name='story4read'),
    url(r'^story4submit/$', views.story4submit, name='story4submit'),
    url(r'^prompt4/$', views.prompt4, name='prompt4'),
    url(r'^story4/vote4/(?P<subd_id>[0-9]+)/$', views.vote4, name='vote4'),    
]
