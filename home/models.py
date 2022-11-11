from django.db import models

# Create your models here.

class Software(models.Model):
    name                = models.CharField(max_length=50)
    version             = models.CharField(max_length = 40)
    icon                = models.ImageField(upload_to= 'icons')
    file                = models.FileField(upload_to = 'exefile')
    screenshots1        = models.ImageField(upload_to = 'scre' , default= '')
    screenshots2        = models.ImageField(upload_to = 'scre' , default= '')
    screenshots3        = models.ImageField(upload_to = 'scre' , default= '')
    screenshots4        = models.ImageField(upload_to = 'scre' , default= '')
    screenshots5        = models.ImageField(upload_to = 'scre' , default= '')
    descriptions        = models.TextField()
    rating              = models.CharField(max_length= 30)
    type                = models.CharField(max_length= 15)
    count               = models.IntegerField()

    # additional Informations
    publisher           = models.CharField(max_length=50)
    category            = models.CharField(max_length=50)
    # reldate      = models.CharField(max_length=50)
    reldate             = models.DateTimeField(auto_now_add=True)
    updatedate          = models.DateTimeField(blank=True,null=True)
    size                = models.CharField(max_length=50)
    installation        = models.CharField(max_length = 100) 
    info                = models.CharField(max_length = 120)
    language            = models.CharField(max_length = 20)
    pubinfo             = models.CharField(max_length = 150)
    term                = models.CharField(max_length = 180,default='')
    average             = models.CharField(max_length = 40,default='')
    position            = models.CharField(max_length = 50,default='')
    update              = models.BooleanField(max_length = 50,default=False,blank = True)
    instapos            = models.BooleanField(default = False,blank=True)
    
    def __str__(self):
        return self.name + " "+ self.version


