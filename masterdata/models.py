from django.db import models
from django.contrib.auth.models import User

# ********************** Supplier ********************

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contactPerson = models.CharField(max_length=200)
    mobileNo = models.IntegerField()
    officeNo =  models.IntegerField(blank=True , null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True , null=True)

    class Meta:
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.name

# ********************** Customer ********************

class Customer(models.Model):

    name        = models.CharField(max_length=200)
    mobileNo    = models.IntegerField()
    companyName = models.CharField(max_length=200, blank=True , null=True)
    officeNo    =  models.IntegerField(blank=True , null=True)
    createdOn   = models.DateTimeField(auto_now_add=True)
    createdBy   = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True , null=True)

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name


# ********************** Product ********************

class ProductCategory(models.Model):
    productCategory = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        return self.productCategory

class Product(models.Model):
    
    unitOfMeasureChoices = { "PCS" : "Pieces",
                             "MTR" : "Meter" }
    
    name               = models.CharField(max_length=250)
    barCode            = models.CharField(unique=True,max_length=16,blank = False,null=False)
    productCategory    = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL , blank=True , null=True)
    currentStock       = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    reOrderlLevel      = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    unitOfMeasure      = models.CharField(max_length=5, choices=unitOfMeasureChoices, default="MTR")
    salesPrice         = models.DecimalField(max_digits=7,decimal_places=2,null=False,blank = False)
    purchasePrice      = models.DecimalField(max_digits=7,decimal_places=2,default=0,null=False)
    
    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return str(self.barCode) 
