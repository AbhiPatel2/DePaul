from django.contrib import admin
from .models import *


admin.site.register(Quality)
admin.site.register(QualityType)

admin.site.register(Customer)
admin.site.register(QualityCustomerJoin)
admin.site.register(ShippingAddress)

admin.site.register(Brand)

admin.site.register(ItemCategory)
admin.site.register(Item)
admin.site.register(ItemType)
admin.site.register(QualityItemTypeJoin)

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(BestSellers)
admin.site.register(NewArrivals)
