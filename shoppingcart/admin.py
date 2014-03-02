from django.contrib import admin
from shoppingcart.models import (Store, UserProfile, Product, \
    Order, OrderDetail)

admin.site.register(Store)
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetail)