from django.conf.urls import patterns, url

from kraftprotz import views

urlpatterns = patterns('',

	url(r'^running/$', views.RunningList.as_view(),
			name='kraftprotz_running_list'),
	url(r'^running/create/$', views.RunningCreate.as_view(),
			name = 'kraftprotz_running_create'),
	url(r'^running/(?P<pk>\d+)/$', views.RunningDetail.as_view(),
			name='kraftprotz_running_detail'),
	url(r'^running/(?P<pk>\d+)/delete$', views.RunningDelete.as_view(),
			name='kraftprotz_running_delete'),

	url(r'^cycling/$', views.CyclingList.as_view(),
			name='kraftprotz_cycling_list'),
	url(r'^cycling/create/$', views.CyclingCreate.as_view(),
			name = 'kraftprotz_cycling_create'),
	url(r'^cycling/(?P<pk>\d+)/$', views.CyclingDetail.as_view(),
			name='kraftprotz_cycling_detail'),
	url(r'^cycling/(?P<pk>\d+)/delete$', views.CyclingDelete.as_view(),
			name='kraftprotz_cycling_delete'),

	url(r'^swimming/$', views.SwimmingList.as_view(),
			name='kraftprotz_swimming_list'),
	url(r'^swimming/create/$', views.SwimmingCreate.as_view(),
			name = 'kraftprotz_swimming_create'),
	url(r'^swimming/(?P<pk>\d+)/$', views.SwimmingDetail.as_view(),
			name='kraftprotz_swimming_detail'),
	url(r'^swimming/(?P<pk>\d+)/delete$', views.SwimmingDelete.as_view(),
			name='kraftprotz_swimming_delete'),

	url(r'^workout/$', views.WorkoutList.as_view(),
			name='kraftprotz_workout_list'),
	url(r'^workout/create/$', views.WorkoutCreate.as_view(),
			name = 'kraftprotz_workout_create'),
	url(r'^workout/(?P<pk>\d+)/$', views.WorkoutDetail.as_view(),
			name='kraftprotz_workout_detail'),
	url(r'^workout/(?P<pk>\d+)/delete$', views.WorkoutDelete.as_view(),
			name='kraftprotz_workout_delete'),

)
