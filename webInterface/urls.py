from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.landing_page, name='landing_page'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^newContact', views.new_contact, name='new_contact'),
    url(r'^contact/(?P<pk>\d+)$', views.contact_details, name='contact_details'),
    url(r'^contact/(?P<pk>\d+)/edit$', views.edit_contact, name='edit_contact'),
    url(r'^contact/(?P<pk>\d+)/public', views.contact_public, name='contact_public'),
    url(r'^contact/(?P<pk>\d+)/request', views.contact_request, name='contact_request'),
]
