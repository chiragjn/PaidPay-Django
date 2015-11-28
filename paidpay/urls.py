from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'paidpay.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', views.home, name='Home'),
    url(r'^generate_prototype/',views.gen_prop, name='Generate Transaction Prototype'),
    url(r'^generate_transfer/',views.gen_trans, name='Generate Transfer Prototype'),
    url(r'^bill/',views.citrus_bill_generator, name='Generate'),
    url(r'^returnbill/',views.citrus_return_url, name='Generate'),
    url(r'^test/',views.test_ret, name='Generate')
    # url(r'^generate_prototype/',views.gen_prop, name='Generate Transaction Prototype')
)
