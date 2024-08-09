from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import Customer,Seller,Art,Order,order_update,Contact,Cart,CartItem,Review

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser,SellerAdditional


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'name','type', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'name', 'type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = ['Art_id','Art_Name','price','upload_by','Type','date_added']

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','date_joined']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','email','phone','date_joined']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['User','Address','Zip_Code','order_Method']

@admin.register(order_update)
class order_updateAdmin(admin.ModelAdmin):
    list_display = ['order_Status','order_id','order_time']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['c_name','c_email','c_phone']

@admin.register(SellerAdditional)
class SellerAdditionalAdmin(admin.ModelAdmin):
    list_display = ['store_Name','user','Verification_status']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart','product','quantity']

admin.site.register([Cart,Review])
