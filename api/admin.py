from django.contrib import admin

from api.models import Banner, Category, PathologyTest
from user.models import Pathology

# Register your models here.
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(PathologyTest)
admin.site.register(Pathology)

