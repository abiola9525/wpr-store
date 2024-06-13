from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.files import File

from io import BytesIO
from PIL import Image

# Create your models here.
class Category(models.Model):
	title = models.CharField(max_length=25)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to='media/', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.title


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField()
    description = RichTextUploadingField()
    price = models.IntegerField()
    # thumbnail = models.ImageField(upload_to='product_images/thumbnail/', blank=True, null=True)
    image = models.ImageField(upload_to='product-media/')
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
class Order(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    paid_amount = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    payment_intent = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (self.last_name + ' ' + self.first_name)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return str(self.product)
    
    
    # def get_thumbnail(self):
    #     if self.thumbnail:
    #         return self.thumbnail.url
    #     else:
    #         if self.image:
    #             self.thumbnail = self.make_thumbnail(self.image)
    #             self.save()
                
    #             return self.thumbnail.url
    #         else:
    #             return 'https://via.placeholder.com/240x240x.jpg'
    
    # def make_thumbnail(self, image, size=(300, 300)):
    #     img = Image.open(image)
    #     img.convert('RGB')
    #     img.thumbnail(size)
        
    #     thumb_io = BytesIO()
    #     img.save(thumb_io, name=image.name)
    #     thumbnail = File(thumb_io, name=image.name)
        
    #     return thumbnail
		
  
	
        
    
 
	
