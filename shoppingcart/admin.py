from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from shoppingcart.models import (Store, UserProfile, Product, \
    Order, OrderDetail)

from django.utils.translation import ugettext_lazy as _

class InventoryFilter(admin.SimpleListFilter):
    title = _('Inventory Status')
    parameter_name = 'inv'

    def lookups(self, request, model_admin):
        return (
            ('low', _('low inventory')),
            ('norm', _('normal inventory')),
            ('high', _('stock overflow')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'low':
            return queryset.filter(inventory__lte=10)
        if self.value() == 'norm':
            return queryset.filter(inventory__gt=10,
                                    inventory__lte=50)
        if self.value() == 'high':
            return queryset.filter(inventory__gt=50)

class ProductAdmin(admin.ModelAdmin):
    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(ProductAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(store = user.userprofile.store)
    search_fields = ('name', 'description')
    list_filter = ('price', InventoryFilter)
    list_display = ('name', 'price', 'inventory')

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

class ModifiedUserAdmin(UserAdmin):
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        #get all fields as readonly
        fields = [f.name for f in self.model._meta.fields]
        return fields

    def queryset(self, request):
        user = getattr(request, 'user', None)
        qs = super(ModifiedUserAdmin, self).queryset(request)
        if user.is_superuser:
            return qs
        return qs.filter(userprofile__store = user.userprofile.store,)

admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)

admin.site.unregister(User)
admin.site.register(User, ModifiedUserAdmin)


admin.site.register(Store)
admin.site.register(UserProfile)
