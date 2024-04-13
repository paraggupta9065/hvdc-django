import uuid
from django.db import models
from common.models import BaseModel
from user.models import Address, Pathology, Patient, User
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

class InCartField(models.BooleanField):
    description = "Indicates whether the test is in the cart for a specific user"

    def contribute_to_class(self, cls, name, private_only=False):
        super().contribute_to_class(cls, name, private_only=private_only)
        models.signals.post_save.connect(self.update_in_cart, sender=cls)

    def update_in_cart(self, sender, instance, **kwargs):
        
        if hasattr(instance, 'cart'):
            instance.in_cart = instance.cart.tests.filter(pk=instance.pk).exists()
        else:
            instance.in_cart = True
    
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
    pathology_list = models.ManyToManyField(Pathology,null=True,blank=True,related_name="test_pathology_list")
    
    
    def __str__(self):
        return self.name
    
class PathologyPackageTest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class PathologyPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # preparation_instructions = models.ArrayField(models.TextField(blank=True, null=True))
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    tests = models.ManyToManyField(PathologyPackageTest)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
        
class Slot(models.Model):
    day = models.IntegerField(choices=[(i, i) for i in range(1,32)])
    month = models.IntegerField(choices=[(i, i) for i in range(1,13)])
    year = models.IntegerField()
    hour = models.IntegerField(choices=[(i, i) for i in range(1,25)])
    minute = models.IntegerField(choices=[(i, i) for i in range(1,61)])
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day} - {self.hour:02}:{self.minute:02}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField('PathologyTest')
    date_added = models.DateTimeField(auto_now_add=True)
    promo_code = models.CharField(max_length=50, blank=True)

    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        return total

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField('PathologyTest')
    date_added = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE,null=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        return total

