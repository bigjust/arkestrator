from django.conf.urls.defaults import *


import views
import models

urlpatterns = patterns('',
    url(r"^$",views.list_threads, name='list-threads'),
    url(r"^threads/(?P<id>\d+)/$",views.view_thread,name='view-thread'),
    url(r"^threads/(?P<id>\d+)/full/$",views.view_thread,{
        'expand' : True,
    }, name='view-thread-full'),
    url(r"^threads/sticky/(?P<id>\d+)/$",views.sticky,
        name='sticky'),
    url(r"^threads/unsticky/(?P<id>\d+)/$",views.unsticky,
        name='unsticky'),
    url(r"^threads/lock/(?P<id>\d+)/$",views.lock_thread,
        name='lock-thread'),
    url(r"^threads/unlock/(?P<id>\d+)/$",views.unlock_thread,
        name='unlock-thread'),
    url(r"^threads/(?P<id>\d+)/history/$",views.thread_history,
        name='thread-history'),
    url(r"^threads/new/$",views.new_thread,name='new-thread'),
    url(r"^threads/mark_read/$",views.mark_read,name='mark-threads-read'),
    url(r"^threads/threads_by/(?P<id>\d+)/$", views.threads_by,
            name='threads-by'),
    url(r"^threads/posts_by/(?P<id>\d+)/$", views.posts_by,
            name='posts-by'),
    url(r"^quote/(?P<id>\d+)/$", views.get_quote, name='get-quote'),
    url(r"^pms/$", views.list_pms, name='list-pms'),
    url(r"^pms/new/$", views.new_pm, name='new-pm'),
    url(r"^pms/new/(?P<rec_id>\d+)/$", views.new_pm, name='new-pm'),
)
