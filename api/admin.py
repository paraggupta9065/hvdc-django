from django.contrib import admin

from api.models import Banner, Category, Order, PathologyTest, Prescription, Slot
from user.models import Pathology

# Register your models here.
admin.site.register(Banner)
admin.site.register(Category)
class PathologyTestAdmin(admin.ModelAdmin):
    list_filter = ["test_type"]
    list_display = ['name',"test_type",'price']
    search_fields = ["name",'description','test_type']
    
admin.site.register(PathologyTest,PathologyTestAdmin)
admin.site.register(Pathology)
admin.site.register(Slot)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ["date_added"]
    search_fields = ["user__name"]
    filter_horizontal = ["tests"]
    fields = ["patient", "user","address",'status','slot','tests']
admin.site.register(Order,OrderAdmin)
admin.site.register(Prescription)

