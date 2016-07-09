from django.conf.urls import include, url
from monkey_hd import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^agile/$', views.agile, name='agile'),
    url(r'^ticket/(?P<pk>[0-9]+)/$', views.ticket, name='ticket'),
    url(r'^ticket/new/$', views.ticket_new, name='ticket_new'),
    url(r'^ticket/edit/(?P<pk>[0-9]+)/$', views.ticket_edit, name='ticket_edit'),
    url(r'^ticket/delete/(?P<pk>[0-9]+)/$', views.ticket_delete, name='ticket_delete'),
    url(r'^ticket/escalate/(?P<pk>[0-9]+)/$', views.ticket_escalate, name='ticket_escalate'),
]
