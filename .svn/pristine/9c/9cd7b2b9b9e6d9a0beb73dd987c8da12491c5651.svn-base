from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^appointments/create/$', views.CreateAppointment.as_view(), name='create'),
    url(r'^appointments/(?P<pk>[0-9]+)/delete/$', views.DeleteAppointment.as_view(), name='delete'),
    url(r'^appointments/$', views.Calendar.as_view(), name='calendar'),
    url(r'^appointments/(?P<pk>[0-9]+)/update/$', views.UpdateAppointment.as_view(), name='update'),
]
