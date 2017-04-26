from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^(?P<pk>[0-9]+)/tests/$', views.TestView.as_view(), name='tests'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultView.as_view(), name='results'),
    url(r'^(?P<pk>[0-9]+)/prescriptions/$', views.PrescriptionView.as_view(), name='prescriptions'),
    url(r'^(?P<pk>[0-9]+)/prescriptions/create/$', views.CreatePrescriptionView.as_view(), name='create_p'),
    url(r'^(?P<pk>[0-9]+)/prescriptions/(?P<pres_pk>[0-9]+)/delete/$',
        views.DeletePrescriptionView.as_view(), name='delete_p'),
    url(r'^(?P<pk>[0-9]+)/tests/$', views.TestView.as_view(), name='tests'),
    url(r'^(?P<pk>[0-9]+)/tests/create$', views.CreateTestView.as_view(), name='create_t'),
    url(r'^(?P<pk>[0-9]+)/tests/(?P<test_pk>[0-9]+)/image$', views.ImageTestView.as_view(), name='image_t'),
    url(r'^(?P<pk>[0-9]+)/tests/(?P<test_pk>[0-9]+)/update$', views.UpdateTestView.as_view(), name='update_t'),
    url(r'^(?P<pk>[0-9]+)/tests/(?P<test_pk>[0-9]+)/delete$', views.DeleteTestView.as_view(), name='delete_t'),
    url(r'^stats/$', views.StatisticsJson.as_view(), name='stats'),
]
