from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #url(r'^', core_urls),
    url(r'^stats/', views.AdminPageView.as_view(), name='adminstats'),
    url(r'^$', views.AdminPageView.as_view(), name='adminpage'),
]
