from django.contrib import admin
from .models import *


admin.site.register(Address)
admin.site.register(PaymentMethods)
admin.site.register(AdditionalInfo)
admin.site.register(PreOrderingCalender)

