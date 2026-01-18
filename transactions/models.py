from django.db import models
from masterdata.models import Product, Customer, Supplier

# ********************** Transaction - Header ********************

class TransactionHeader(models.Model):
    
    transactionTypes  = { "S" : "Sales",
                          "P" : "Purchase" }

    modesOfPayment    = { "C" : "Cash",
                          "A" : "Card",
                          "T" : "Bank Transfer",
                          "U" : "UPI" }

    tranType          = models.CharField(max_length=1, choices=transactionTypes )
    tranDate          = models.DateField( )
    paymentMode       = models.CharField( max_length=1, choices=modesOfPayment, default="C" )
    customer          = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    supplier          = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    one_time_name     = models.CharField(max_length=250, blank=True, null=True )
    one_time_number   = models.DecimalField(max_digits=10, decimal_places=0 , blank=True, null=True )
    grossAmount       = models.DecimalField(max_digits=7,decimal_places=2)
    discount          = models.DecimalField(max_digits=7,decimal_places=2)

    class Meta:
        verbose_name_plural = 'Transactions'

    def update_total(self):
        # Calculate total from related items
        result = self.items.aggregate(
            total=models.Sum(models.F('quantity') * models.F('price'))
        )
        self.grossAmount = result['total'] or 0
        self.save(update_fields=['grossAmount'])
        
class TransactionItems(models.Model):
    
    transaction        = models.ForeignKey(TransactionHeader, on_delete=models.CASCADE, related_name='items' )
    product            = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity           = models.DecimalField(max_digits=7, decimal_places=2)
    price              = models.DecimalField(max_digits=7,decimal_places=2)

    class Meta:
        verbose_name_plural = 'TransactionItems'


    def save(self, *args, **kwargs):
        # 1. Update the product stock using F() to prevent race conditions
        # this executes the subtraction directly in the database
        Product.objects.filter(barCode=self.product.barCode).update(
            currentStock=models.F('currentStock') - self.quantity
        )
        # 2. Call the actual save method of the TransactionItem
        super().save(*args, **kwargs)
        
        # Update parent invoice total after saving item
        self.transaction.update_total()

    def delete(self, *args, **kwargs):
        # Update parent invoice total before deleting item
        self.transaction.update_total()
        super().delete(*args, **kwargs)