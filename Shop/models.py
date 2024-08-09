from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class LowercaseEmailField(models.EmailField):
    
    def to_python(self, value):
        
        value = super(LowercaseEmailField, self).to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = LowercaseEmailField(_('email address'), unique=True)
    name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # if you require phone number field in your project
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone = models.CharField(max_length=255, validators=[phone_regex], blank = True, null=True) 

    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"
    
    # Types = (
    #     (1, 'SELLER'),
    #     (2, 'CUSTOMER')
    # )
    # type = models.IntegerField(choices=Types, default=2)

    default_type = Types.CUSTOMER

    #type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    type = MultiSelectField(choices=Types.choices, default=[], null=True, blank=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
    def save(self, *args, **kwargs):
        if not self.id:
            #self.type = self.default_type
            self.type.append(self.default_type)
        return super().save(*args, **kwargs)

class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.CharField(max_length=1000)

class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.SELLER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.SELLER))

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        #return super().get_queryset(*args, **kwargs).filter(type = CustomUser.Types.CUSTOMER)
        return super().get_queryset(*args, **kwargs).filter(Q(type__contains = CustomUser.Types.CUSTOMER))

class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")

    @property
    def showAdditional(self):
        return self.selleradditional

class Customer(CustomUser):
    default_type = CustomUser.Types.CUSTOMER
    objects = CustomerManager()
    class Meta:
        proxy = True 

    def buy(self):
        print("I can buy")

    @property
    def showAdditional(self):
        return self.customeradditional


class SellerAdditional(models.Model):
    user = models.OneToOneField(Seller, on_delete = models.CASCADE,unique=True)
    store_Name = models.CharField(max_length=10)
    store_Logo = models.ImageField(upload_to='ArtImages/storesLogo',default=None)
    Verification_Image = models.ImageField(upload_to='ArtImages/Seller_Verification',default=None)
    Verification_status = models.BooleanField(default=False)
    

    def __str__(self):
        return self.store_Name

class Art(models.Model):


    Art_id = models.AutoField(primary_key=True)
    Art_Name = models.CharField(max_length=15)
    image = models.ImageField(upload_to = "ArtImages/productimages", default = None, null = True, blank = True)
    price = models.FloatField()
    Type = models.CharField(max_length=1000)
    upload_by = models.ForeignKey(SellerAdditional,on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Art_id


    @classmethod
    def updateprice(cls,product_id, price):
        product = cls.objects.filter(product_id = product_id)
        product = product.first()
        product.price = price
        product.save()
        return product

    def __str__(self):
        return (f'{self.Art_id}')
        


class Order(models.Model):

    Order_id = models.AutoField(primary_key=True)
    item_json = models.CharField(max_length=10000)
    User = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    Address = models.CharField(max_length=100)
    Zip_Code = models.CharField(max_length=100)
    order_Method = models.BooleanField(default=False)

class order_update(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_updates')
    order_Status = models.CharField(max_length=1000)
    order_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_Status[0:8]+" ...")



class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Art, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Review(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    post = models.ForeignKey(Art, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timez = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment[0:13] + "... by " + self.user.name

class Contact(models.Model):

    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=70,default="")
    c_email = models.CharField(max_length=75,default="")
    c_phone = models.CharField(max_length=50,default="")
    c_subject = models.CharField(max_length=100,default="")
    c_message = models.CharField(max_length=1500,default="")

    def __str__(self):
        return self.c_email

