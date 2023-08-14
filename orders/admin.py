from django.contrib import admin
from jalali_date import datetime2jalali

from .models import Payment, Order, OrderProduct


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'status', 'order_total',
                    'created_shamsi_date', 'updated_shamsi_date']
    list_filter = ['is_ordered', 'status',]
    search_fields = ['order_number', 'first_name', 'last_name', 'email', 'phone', 'created_shamsi_date', 'updated_shamsi_date']
    list_per_page = 20
    readonly_fields = ['created_shamsi_date', 'updated_shamsi_date']

    # @admin.display(description='تاریخ ایجاد')
    def created_shamsi_date(self, obj):
        return datetime2jalali(obj.created_at).strftime('%H:%M:%S _ %Y/%m/%d')

    created_shamsi_date.admin_order_field = 'created_at'

    # @admin.display(description='تاریخ به روزرسانی')
    def updated_shamsi_date(self, obj):
        return datetime2jalali(obj.updated_at).strftime('%H:%M:%S _ %Y/%m/%d')

    updated_shamsi_date.admin_order_field = 'updated_at'


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
