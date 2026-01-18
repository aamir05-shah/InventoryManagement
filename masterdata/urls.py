from django.urls import path

from .views import SupplierListView, CustomerListView , CreateSupplierView , CreateCustomerView ,ProductListView , CreateProductView
from .views import EditSupplierView , EditCustomerView , DeleteSupplierView ,DeleteCustomerView , EditProductView , DeleteProductView

from .views import GetProductDetails, GetCustomerDetails

urlpatterns = [
# List 
    path('SupplierList/', SupplierListView.as_view(), name="SupplierList"),
    path('CustomerList/', CustomerListView.as_view(), name="CustomerList"),
    path('ProductList/', ProductListView.as_view(), name="ProductList"),
#Create
    path('CreateSupplier', CreateSupplierView.as_view(), name='CreateSupplier'),
    path('CreateCustomer', CreateCustomerView.as_view(), name='CreateCustomer'),
    path('CreateProduct', CreateProductView.as_view(), name='CreateProduct'),
#Edit
    path('UpdateSupplier/<int:pk>', EditSupplierView.as_view(), name='UpdateSupplier'),
    path('UpdateCustomer/<int:pk>', EditCustomerView.as_view(), name='UpdateCustomer'),
     path('UpdateProduct/<int:pk>', EditProductView.as_view(), name='UpdateProduct'),
#Delete 
    path('DeleteSupplier/<int:pk>', DeleteSupplierView.as_view(), name='DeleteSupplier'),
    path('DeleteCustomer/<int:pk>', DeleteCustomerView.as_view(), name='DeleteCustomer'),
    path('DeleteProduct/<int:pk>', DeleteProductView.as_view(), name='DeleteProduct'),
    
#Data Path URLs
    path('GetProduct/<str:barCode>', GetProductDetails , name='GetProduct'),
    path('GetCustomer/<int:pk>', GetCustomerDetails , name='GetCustomer'),
]