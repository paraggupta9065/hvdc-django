import uuid
from django.db import models
from common.models import BaseModel
# Create your models here.

class Pathology(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='pathology_images/', blank=True, null=True)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    is_offline = models.BooleanField(default=False)


class Banner(BaseModel):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

# Category model 

class Category(BaseModel):
    categoryName = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.categoryName
    
class PathologyTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    test_type = models.CharField(max_length=50)
    # preparation_instructions = models.ArrayField(models.TextField(blank=True, null=True))
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    is_offline = models.BooleanField(default=True)
    
class PathologyPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # preparation_instructions = models.ArrayField(models.TextField(blank=True, null=True))
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False)
    price = models.IntegerField(null=False)


