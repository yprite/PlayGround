from django.db import models

# Create your models here.

class category(models.Model):
   name = models.CharField(max_length=200, null=True, blank=True)  
   value = models.CharField(max_length=200, null=True, blank=True)  
   def __str__(self):
       return self.name

class product(models.Model):
   name = models.CharField(max_length=200, null=True, blank=True)  
   def __str__(self):
       return self.name

class keyword(models.Model):
   name = models.CharField(max_length=200, null=True, blank=True)  
   def __str__(self):
       return self.name

class company(models.Model):
   name = models.CharField(max_length=200, null=True, blank=True)  
   wiki = models.CharField(max_length=500, null=True, blank=True)  
   image = models.CharField(max_length=500, null=True, blank=True)  
   #category = models.ForeignKey(category, on_delete=None, null=True, blank=True)
   category = models.ManyToManyField(category)
   produce = models.ManyToManyField(product, related_name="produce", blank=True)
   replace = models.ManyToManyField(product, related_name="replace",  blank=True)

   def __str__(self):
       return self.name



