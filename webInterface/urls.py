from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^newContact$', views.new_contact, name='new_contact'),
    url(r'^contact/(?P<pk>\d+)$', views.contact_details, name='contact_details'),
    url(r'^contact/(?P<pk>\d+)/edit$$', views.edit_contact, name='edit_contact'),
    url(r'^contact/(?P<pk>\d+)/public$', views.contact_public, name='contact_public'),
    url(r'^contact/(?P<pk>\d+)/request$', views.contact_request, name='contact_request'),
    url(r'^contact/(?P<pk>\d+)/download$', views.download_contact, name='download_contact'),
    url(r'^share/(?P<pk>\d+)/approve$', views.approve_share, name='approve_share'),
    url(r'^share/(?P<pk>\d+)/remove$', views.remove_share, name='remove_share'),
    url(r'^sharing$', views.sharing, name='sharing'),
    url(r'^newGroup$', views.new_group, name='new_group'),
    url(r'^group/(?P<pk>\d+$)$', views.group_details, name='group_details'),
]
