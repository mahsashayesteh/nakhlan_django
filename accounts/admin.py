from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from jalali_date import datetime2jalali

from .models import Account, UserProfile


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 'last_name', 'username', 'shamsi_last_login', 'shamsi_date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('shamsi_last_login', 'shamsi_date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    # show date in shamsi format
    # @admin.display(description='آخرین ورود')
    def shamsi_last_login(self, obj):
        if obj.last_login is not None:

            return datetime2jalali(obj.last_login).strftime('%H:%M _ %Y/%m/%d')
        else:
            return '-'
    shamsi_last_login.admin_order_field = 'last_login'

    # show date in shamsi format
    # @admin.display(description='زمان عضویت')
    def shamsi_date_joined(self, obj):
        return datetime2jalali(obj.date_joined).strftime('%H:%M _ %Y/%m/%d')

    shamsi_date_joined.admin_order_field = 'date_joined'

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, obj):
        return format_html(
            '<img src="{}" width="30" style="border-radius=50%;">'.format(obj.profile_picture.url))

    thumbnail.short_description = 'عکس پروفایل'
    list_display = ('thumbnail', 'user', 'full_address')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Account, AccountAdmin)
