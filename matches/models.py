from django.db import models

# Create your models here.
class matches(models.Model):
    object1 = models.CharField(max_length=100)
    object2 = models.CharField(max_length=100)
    ans_yes = models.PositiveIntegerField(null=True,blank=False)
    ans_no = models.PositiveIntegerField(null=True,blank=False)
    def __str__(self):
        return self.object1+ ', ' +self.object2
class Object(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
class Rate(models.Model):
    object1 = models.ForeignKey(Object, on_delete=models.CASCADE,related_name="a")
    object2 = models.ForeignKey(Object, on_delete=models.CASCADE,related_name="b")
    ans_yes = models.PositiveIntegerField(default=0, null=True,blank=False)
    ans_no = models.PositiveIntegerField(default=0,null=True,blank=False)
    class Meta:
        unique_together = ('object1', 'object2')
    def __str__(self):
        return "#"+str(self.id)+ ": " + self.object1.__str__() + ", " + self.object2.__str__()
class AddressRate(models.Model):
    ipAddress = models.CharField(max_length=100)
    rates = models.ManyToManyField(Rate)