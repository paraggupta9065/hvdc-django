import uuid
from django.db import models
from common.models import BaseModel
from user.models import Address, Pathology, Patient, User
from django.utils.html import mark_safe
from django.utils import timezone

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
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False,default = 0)
    price = models.IntegerField(null=False)
    is_offline = models.BooleanField(default=False)
    pathology_list = models.ManyToManyField(Pathology,blank=True,related_name="test_pathology_list")
    fasting = models.CharField(max_length=50,default="No fasting required")
    gender = models.CharField(max_length=50,default="For Male, Female")
    age = models.CharField(max_length=50,default="Age: 5-99 yrs")
    report_time = models.CharField(max_length=50,default="Reports with in 24 hrs")
    
    def __str__(self):
        return self.name

class PathologyPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)
    tests = models.ManyToManyField(PathologyTest,blank=False,related_name="packages_tests_list")
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    regular_price = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    fasting = models.CharField(max_length=50,default="No fasting required")
    gender = models.CharField(max_length=50,default="For Male, Female")
    age = models.CharField(max_length=50,default="Age: 5-99 yrs")
    report_time = models.CharField(max_length=50,default="Reports with in 24 hrs")
    
        
class Slot(models.Model):
    day = models.IntegerField(choices=[(i, i) for i in range(1,32)])
    month = models.IntegerField(choices=[(i, i) for i in range(1,13)])
    year = models.IntegerField()
    hour = models.IntegerField(choices=[(i, i) for i in range(1,25)])
    minute = models.IntegerField(choices=[(i, i) for i in range(0,60)])
    pathology = models.ForeignKey(Pathology,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.day} - {self.hour:02}:{self.minute:02}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    promocode = models.ForeignKey("PromoCode", on_delete=models.CASCADE, blank=True, null=True)
    tests = models.ManyToManyField('PathologyTest')
    packages = models.ManyToManyField('PathologyPackage', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        total = 0
        for package in self.packages.all():
            total += package.price
        for test in self.tests.all():
            total += test.price
        if(self.promocode):
            discount = ((total / 100) * int(self.promocode.discount_percentage))
            total = (total - discount)            
        return total
    
    def discount(self):     
        total = 0
        discount = 0
        for package in self.packages.all():
            total += package.price
        for test in self.tests.all():
            total += test.price
        if(self.promocode):
            discount = ((total / 100) * int(self.promocode.discount_percentage))
            total = (total - discount)   
        return discount
    
    def normal_price(self):     
        total = 0
        for package in self.packages.all():
            total += package.price
        for test in self.tests.all():
            total += test.price
        return total

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tests = models.ManyToManyField('PathologyTest')
    packages = models.ManyToManyField('PathologyPackage', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,null=True,blank=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE,null=True)
    is_offline = models.BooleanField(default=False)
    report = models.FileField(upload_to ='reports/',null=True,blank=True)
    promocode = models.ForeignKey("PromoCode", on_delete=models.CASCADE, blank=True, null=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('uploaded', 'uploaded'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        if(self.promocode):
            total = (total - ((total / 100)* self.promocode.discount_percentage))
        return total
    def __str__(self) -> str:
        return f'{self.user.name}'
    
class Prescription(models.Model):
    prescription = models.ImageField(upload_to ='prescription/') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tests = models.ManyToManyField('PathologyTest',blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    promo_code = models.CharField(max_length=50, blank=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def total_price(self):
        total = 0
        for test in self.tests.all():
            total += test.price
        return total

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to