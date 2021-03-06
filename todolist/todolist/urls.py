from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from allauth.account import views as allauth_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'todolist.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    (r'^/?$', allauth_views.login),
    (r'^tasks/?$', 'tasks.views.list_tasks'),
    (r'^tasks/create/?$', 'tasks.views.create_task'),
    (r'^tasks/(?P<task_id>[\d]+?)/edit/?$', 'tasks.views.edit_task'),
    (r'^tasks/(?P<task_id>[\d]+?)/delete/?$', 'tasks.views.delete_task'),
)

urlpatterns += patterns('',
    (r'^api/register/?$', 'rest_apis.views.register'),
    (r'^api/login/?$', 'rest_apis.views.api_login'),
    (r'^api/logout/?$', 'rest_apis.views.api_logout'),
    (r'^api/tasks/create/?$', 'rest_apis.views.create_task'),
    (r'^api/tasks/(?P<task_id>[\d]+?)/edit/?$', 'rest_apis.views.edit_task'),
    (r'^api/tasks/?$', 'rest_apis.views.list_tasks'),
    (r'^api/tasks/(?P<task_id>[\d]+?)/delete/?$', 'rest_apis.views.delete_task'),
    (r'^api/tasks/(?P<task_id>[\d]+?)/view/?$', 'rest_apis.views.view_task'),
)

urlpatterns += patterns('',
    (r'^', include('allauth.urls')),
)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'%s(?P<path>.*)' % settings.MEDIA_URL[1:],
            'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
    
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^public/static/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.BASE_DIR + '/templates/static'}),
    )
