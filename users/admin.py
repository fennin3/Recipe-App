from django.contrib import admin
from .models import *

class AddressAdmin(admin.ModelAdmin):
    list_display= ('user', 'address', 'name')

class PaymentMethodsAdmin(admin.ModelAdmin):
    list_display=('user','type','momo_name','holder_name')
    search_fields = ['momo_name','holder_name']

admin.site.register(Address, AddressAdmin)
admin.site.register(PaymentMethods, PaymentMethodsAdmin)
admin.site.register(AdditionalInfo)
admin.site.register(PreOrderingCalender)
admin.site.register(CustomUser)
admin.site.register(Language)
admin.site.register(OTPCode)

