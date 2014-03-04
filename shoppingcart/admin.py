from django.contrib import admin
from shoppingcart.models import (Store, UserProfile, Product, \
    Order, OrderDetail)

class ProductAdmin(admin.ModelAdmin):
    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(ProductAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(store = user.userprofile.store)

class OrderAdmin(admin.ModelAdmin):
    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(OrderAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(user__userprofile__store = user.userprofile.store)

class OrderDetailAdmin(admin.ModelAdmin):
    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(OrderDetailAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(order__user__userprofile__store = user.userprofile.store)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)


admin.site.register(Store)
admin.site.register(UserProfile)
