from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'movies_mari.views.home', name='home'),
                       # url(r'^movies_mari/', include('movies_mari.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^movies/', include('movies.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
