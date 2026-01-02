from django import forms
from .models import Customer , Supplier, Product , ProductCategory

class ModifySupplier(forms.ModelForm):
    
    contactPerson = forms.CharField(label="Contact Person")
    mobileNo = forms.IntegerField(label="Mobile Number")
    officeNo = forms.IntegerField(label="Office Number" , required=False)
    
    class Meta:
        model = Supplier
        fields = ['name', 'mobileNo','contactPerson','officeNo']
        

class ModifyCustomer(forms.ModelForm):
    companyName = forms.CharField(label="Company Name", required=False)
    mobileNo = forms.IntegerField(label="Mobile Number")
    officeNo = forms.IntegerField(label="Office Number" , required=False)
    
    class Meta:
        model = Customer
        fields = ['name', 'mobileNo','companyName','officeNo']

class ModifyProduct(forms.ModelForm):
   
    class Meta:
        model = Product
        fields = ['name', 'barCode' , 'productCategory','currentStock','reOrderlLevel', 'unitOfMeasure',
                  'salesPrice', 'purchasePrice']
