from django.conf.urls import patterns, url

from kraftprotz.urls import urlpatterns as kraftprotz_urls

from core import views

urlpatterns = patterns('',

	url(r'^$', 'core.views.login',
			kwargs={'template_name': 'index.html'}, name='core_login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout',
			kwargs={'next_page': 'core_login'}, name='core_logout'),

	url(r'^dashboard/$', views.CoreDashboard.as_view(), name='core_dashboard'),
)

urlpatterns += kraftprotz_urls
