from django.contrib import admin
from instamojo_wrapper import Instamojo
from firstproject.settings import PAYMENT_API_KEY,PAYMENT_API_AUTH_TOKEN
from django.contrib.auth.decorators import login_required
from django.db.models import Q
api = Instamojo(api_key=PAYMENT_API_KEY, auth_token=PAYMENT_API_AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/');


# Register your models here.
from .models import Product,ProductImages,User,Payment
from django.utils.html import format_html

class ProductImageModel(admin.StackedInline):
    model=ProductImages

class ProductModel(admin.ModelAdmin):
    list_display=['id','name','get_description','get_price','get_discount','SalePrice','file','get_thumbnail','fileSize']
    inlines=[ProductImageModel]
    def get_description(self,obj):
        return format_html(f'<span title="{obj.description}">{obj.description[0:15]}....</span>')
    def get_price(self,obj):
        return ' ₹: '+str(obj.price)
    def get_discount(self,obj):
        return str(obj.discount)+' % '

    def SalePrice(self,obj):
        return '₹: '+str(obj.price-((obj.price)*(obj.discount)/100))
    def get_thumbnail(self,obj):
        return format_html(f'''
          <img src='{obj.thumbnail.url}' style='height:40px'>
        ''')

    get_discount.short_description='Discount'
    get_price.short_description='Price'
    get_thumbnail.short_description='Thumbnail'

class UserModel(admin.ModelAdmin):
    list_display=['id','name','email','password','phone','active']
    sortable_by=['id','name']
    list_editable=['active','name']

class PaymentModel(admin.ModelAdmin):
    list_display=['id','get_user','get_product','payment_request_id','payment_id','get_status']
    sortable_by=['id']

    def get_user(self,obj):
        return format_html(f'<a target="_blank" href="/admin/Download/user/{obj.user.id}">{obj.user}</a>')

    def get_product(self,obj):
        return format_html(f'<a target="_blank" href="/admin/Download/product/{obj.product.id}">{obj.product}</a>')

    def get_status(self,obj):
       response = api.payment_request_payment_status(obj.payment_request_id,obj.payment_id)
       print(response)
       return obj.status

admin.site.register(User,UserModel)
admin.site.register(Payment,PaymentModel)
admin.site.register(Product,ProductModel)
