from django.conf.urls import patterns, url

from shoppingcart import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # user management
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    # cart
    url(r'^cart$', views.cart, name='cart'),
    url(r'^cart/(?P<pk>\d+)/$', views.cart, name='cart'),
    # order
    url(r'^checkout$', views.checkout, name='checkout'),
    #profile
    url(r'^orders$', views.orders, name='orders'),
    url(r'^order/(?P<id>\d+)/$', views.order_detail, name='order_detail'),
)