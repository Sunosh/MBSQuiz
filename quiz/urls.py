from django.conf.urls import url

from . import views

app_name = 'quiz'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^user-home$', views.user_home, name='user_home'),
    url(r'^play/(?P<subject_id>\d+)/$', views.Play.as_view(), name='play'),
    url(r'^play2/(?P<subject_id>\d+)/$', views.Play2.as_view(), name='play2'),
    url(r'^playtour/(?P<subject_id>\d+)/$', views.PlayTour3.as_view(), name='playtour3'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^subjects/$', views.subjects, name='subjects'),
    url(r'^profile/$', views.profile, name='profile'),

]
