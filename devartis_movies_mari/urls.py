from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^', include('movies.urls', namespace="movies")),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       #override the default urls
                       url(r'^accounts/password/change/$',
                           auth_views.password_change,
                           name='password_change'),
                       url(r'^accounts/password/change/done/$',
                           auth_views.password_change_done,
                           name='password_change_done'),
                       url(r'^accounts/password/reset/$',
                           auth_views.password_reset,
                           name='password_reset'),
                       url(r'^accounts/password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^accounts/password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='password_reset_complete'),
                       url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           name='password_reset_confirm'),
                       # url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                       #     'django.contrib.auth.views.password_reset_confirm',
                       #     {'template_name': 'registration/password_reset_confirm.html'}),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)