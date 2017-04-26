from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^inbox/$', views.InboxView.as_view(), name='inbox'),
    url(r'^sentbox/$', views.SentboxView.as_view(), name='sentbox'),
    url(r'^sendmessage/$', views.SendMessageView.as_view(), name='sendmessage'),
    url(r'^(?P<pk>[0-9]+)/reply/$', views.ReplyMessageView.as_view(), name='reply'),
    url(r'^(?P<pk>[0-9]+)/delete_message/$', views.DeleteMessageView.as_view(), name='delete_m'),
    url(r'^delete_all_messages/$', views.delete_all_messages, name='delete_allm'),
    url(r'^delete_all_sent/$', views.delete_all_sent_messages, name='delete_allsm'),
]
