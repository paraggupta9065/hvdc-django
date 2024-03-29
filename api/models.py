import uuid
from django.db import models
from common.models import BaseModel
from user.models import Pathology, User
# Create your models here.

class Banner(BaseModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# Category model 

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    image = models.ImageField(upload_to='categories/',null=False,default="r")
    

    def __str__(self):
        return self.category_name
    
class PathologyTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    test_type = models.CharField(max_length=50)
    # preparation_instructions = models.ArrayField(models.TextField(blank=True, null=True))
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False,default = 0)
    price = models.IntegerField(null=False)
    is_offline = models.BooleanField(default=False)
    
class PathologyPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # preparation_instructions = models.ArrayField(models.TextField(blank=True, null=True))
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    tests = models.ManyToManyField('PathologyTest')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False)
    price = models.IntegerField(null=False)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField('PathologyTest')
    date_added = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        return total

