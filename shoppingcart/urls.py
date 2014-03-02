from django.conf.urls import patterns, url

from shoppingcart import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^add_to_cart$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart$', views.cart, name='cart'),
    url(r'^remove$', views.remove, name='remove'),
    url(r'^update$', views.update, name='update'),
)