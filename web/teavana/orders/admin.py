from django.contrib import admin

from .models import Order, OrderItem, ShippingAddress, BillingAddress

class OrderItemInline(admin.StackedInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline, ]

admin.site.register(Order, OrderAdmin)
admin.site.register(ShippingAddress)
admin.site.register(BillingAddress)
