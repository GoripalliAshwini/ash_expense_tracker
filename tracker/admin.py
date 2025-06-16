from django.contrib import admin
from tracker.models import *
# Register your models here.

admin.site.site_header="Expense Tracker Admin"
admin.site.site_title="Expense Tracker Admin"
admin.site.index_title="Welcome to Expense Tracker Admin"
@admin.action(
        description='Mark selected stories as Income',
    )
def make_income(self, request, queryset):
        queryset.update(Type='Income')
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = ('Amount', 'Description', 'Type', 'Category', 'Date')
    search_fields = ('Description', 'Type', 'Category')
    list_filter = ('Type', 'Category', 'Date')
    ordering = ('-Date',)
    actions=[make_income]
admin.site.register(Transaction,TrackingHistoryAdmin)