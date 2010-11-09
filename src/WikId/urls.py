from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



  
urlpatterns = patterns('',    
	(r'^wiki/$', 'wiki.views.index'),
	(r'^wiki/search/$', 'wiki.views.search'),
	(r'^wiki/article/(?P<article_title>.*?)/$', 'wiki.views.view_article'),
    (r'^wiki/insert_test_data/$', 'wiki.views.insert_test_data'),
    (r'^wiki/register_user/$', 'wiki.views.register_user'),
    (r'^admin/', include(admin.site.urls)),
)

