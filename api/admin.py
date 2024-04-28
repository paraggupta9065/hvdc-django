from django.contrib import admin
from api.models import Banner, Category, Order, PathologyPackage, PathologyTest, Prescription, Slot
from user.models import Pathology
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)

# Register your models here.

@admin.register(PathologyTest)
class PathologyTestAdmin(admin.ModelAdmin):
    list_filter = ["test_type","is_offline","category","gender","age","report_time"]
    list_display = ['name',"test_type",'price']
    search_fields = ["name",'description','test_type']
    
    
@admin.register(Pathology)
class PathologyAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(PathologyPackage)
class PathologyPackageAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    filter_horizontal = ["tests"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ["date_added"]
    search_fields = ["user__name"]
    filter_horizontal = ["tests"]
    fields = ["patient", "user","address",'status','slot','tests','report']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_filter = ["date_added"]
    list_display = ['user',"promo_code"]
    search_fields = ["user__name"]
    filter_horizontal = ["tests"]
    readonly_fields = ['user']
    
admin.site.register(Banner)
admin.site.register(Category)

admin.site.site_header = 'HVDC Admin'
admin.site.site_title = 'HVDC Admin'
admin.site.index_title = 'Dashboard'