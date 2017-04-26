from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^register/$', views.SignUpView.as_view(), name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(), name='dashboard'),
    url(r'^medical/$', views.MedicalInfoView.as_view(), name='medical'),
    url(r'^export_medical/$', views.download, name='download'),
    url(r'^(?P<pk>[0-9]+)/profile/$', views.UpdateProfile.as_view(), name='profile'),
    url(r'^(?P<pk>[0-9]+)/medical_info/$', views.UpdateMedicalInfo.as_view(), name='updatemedical'),
    url(r'^(?P<pk>[0-9]+)/admit/$', views.AdmitView.as_view(), name='admit'),
    url(r'^(?P<pk>[0-9]+)/discharge/$', views.DischargeView.as_view(), name='discharge'),
    url(r'^(?P<pk>[0-9]+)/transfer/$', views.TransferView.as_view(), name='transfer'),
]
