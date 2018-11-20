from django.db import models
from datetime import datetime, timezone
import matches
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    class Meta:
        verbose_name_plural="Categories"
    def __str__(self):
        return self.name
class Object(models.Model):
    name = models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=None)
    image = models.CharField(max_length=1000)
    plural = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Rate(models.Model):
    object1 = models.ForeignKey(Object, on_delete=models.CASCADE,related_name="a")
    object2 = models.ForeignKey(Object, on_delete=models.CASCADE,related_name="b")
    ans_yes = models.PositiveIntegerField(default=0, null=True,blank=False)
    ans_no = models.PositiveIntegerField(default=0,null=True,blank=False)
    ans_irrelevant=models.PositiveIntegerField(default=0,null=True,blank=False)
    approved = models.BooleanField(default=False)
    created     = models.DateTimeField(blank=True)
    modified    = models.DateTimeField(blank=True)
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.now()
        self.modified = datetime.now()
        return super(Rate, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('object1', 'object2')
    def __str__(self):
        return "#"+str(self.id)+ ": " + self.object1.__str__() + ", " + self.object2.__str__() + ". Last Modified: " + str(self.modified.strftime('%Y-%m-%d %H:%M')) + " Approved: " + str(self.approved)
class ClientRate(models.Model):
    rates = models.ManyToManyField(Rate)
    def __str__(self):
        return "CookieID: " + str(self.id)
# class Category(models.Model):
#     name = models.CharField(max_length=100)

# class DateAnswer(models.Model):
#     date = models.DateField(blank=True)
#     rate= models.ForeignKey(Rate,on_delete=models.CASCADE)
#     ans_yes = models.PositiveIntegerField(default=0,null=True,blank=False)
#     ans_no = models.PositiveIntegerField(default=0,null=True,blank=False)
#     ans_irrelevant = models.PositiveIntegerField(default=0,null=True,blank=False)
#     class Meta:
#         unique_together = ('date', 'rate')