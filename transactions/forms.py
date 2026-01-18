from django import forms
import datetime
from .models import TransactionHeader , TransactionItems, Product, Customer

# *************************************************************
# # Sales Invoice Transaction 
# *************************************************************

class SalesTransaction(forms.ModelForm):
  
    customer          = forms.IntegerField(label = "Customer", required=False)
    tranDate          = forms.DateField(label= "Invoice Date" , 
                                        initial=datetime.date.today,
                                        widget=forms.DateInput(attrs={'type': 'date'}),
                                        required= True)
    one_time_name     = forms.CharField(label="Customer Name", required= False)
    one_time_number   = forms.IntegerField(label="Mobile Number", required= False)
    grossAmount       = forms.DecimalField(label="Total Amount", initial=0)
    discount          = forms.DecimalField(label="Discount Amount", initial=0, required= False)
    paymentMode       = forms.ChoiceField(label= 'Payment Mode',
                                          choices=TransactionHeader.modesOfPayment,
                                          widget=forms.RadioSelect(),
                                          initial="C" )

    class Meta: 
        model   = TransactionHeader
        fields  = ['customer', 'tranDate', 'one_time_name',
                  'one_time_number', 'grossAmount' ,'discount', 'paymentMode']
   
    def clean(self):
        
        data = self.cleaned_data
                
        if(not data['customer']):
            if(not data['one_time_name'] or not data['one_time_number']):
                self.add_error("customer", "Customer is mandatory")
                raise forms.ValidationError("Customer is empty") 
        if(not data['grossAmount']):
            self.add_error("grossAmount", "Cannot post a zero value invoice")
            raise forms.ValidationError("No Items") 
        return super().clean()
    
    def clean_customer(self):
        customer_id = self.cleaned_data['customer']
        if customer_id:
            try:
                return Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                raise forms.ValidationError("Customer does not exist.")


class SalesItem(forms.ModelForm):
    product            = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'product-input'}))
    productName        = forms.CharField(max_length=255, label="Product Name")
    quantity           = forms.DecimalField(label="Quantity")
    price              = forms.DecimalField(label="Unit Price")

    class Meta:
        model   = TransactionItems
        fields  = [ 'product', 'quantity','price']

    def clean(self):

        # Check product
        try:
            product_id   = self.cleaned_data['product']
            oProduct = Product.objects.get(barCode=product_id)
        except Product.DoesNotExist:
            raise forms.ValidationError("Product ID does not exist.")
        
        # Check stock
        try:
            quantity     = self.cleaned_data['quantity']
            if quantity > oProduct.currentStock:
                self.add_error('quantity', f"Product has only {oProduct.currentStock} available.")
                raise forms.ValidationError("Stock issue")
        except (KeyError, TypeError) as e:
                self.add_error('quantity', "Quantity cannot be empty")
                raise forms.ValidationError("Zero qunatity issue")
        
        return super().clean()
    
    def clean_product(self):

        product_id = self.cleaned_data['product']
        try:
            oProduct = Product.objects.get(barCode=product_id)
            return oProduct
        except Product.DoesNotExist:
            raise forms.ValidationError("Product ID does not exist.")

SalesItemFormSet = forms.inlineformset_factory(
    
    parent_model = TransactionHeader,
    model        = TransactionItems,
    form         = SalesItem,
    extra        = 1,
    can_delete   = True
)

# *************************************************************
# # Purchase Invoice Transaction 
# *************************************************************