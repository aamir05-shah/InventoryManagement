from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View , CreateView , UpdateView , DeleteView
from .models import Supplier, Customer , Product , ProductCategory
from .forms import ModifyCustomer , ModifySupplier, ModifyProduct

# **************************************************************************
# Supplier
# **************************************************************************

class SupplierListView( LoginRequiredMixin ,View):
    def get(self , request):
        suppList = Supplier.objects.all().order_by('id')
        return render(request , 'masterdata/Supplier/SupplierList.html', {'suppList': suppList })

    def post(self , request):
        pass

class CreateSupplierView(LoginRequiredMixin , CreateView):
    model = Supplier
    form_class = ModifySupplier
    template_name = 'masterdata/Supplier/ModifySupplier.html'
    success_url = reverse_lazy('SupplierList')

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Create"
        return context

class EditSupplierView(LoginRequiredMixin ,UpdateView):
    model = Supplier
    form_class = ModifySupplier
    template_name = 'masterdata/Supplier/ModifySupplier.html'
    success_url = reverse_lazy('SupplierList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Update"
        return context

class DeleteSupplierView(LoginRequiredMixin , DeleteView ):
    model = Supplier
    template_name = 'masterdata/Supplier/DeleteSupplier.html'
    success_url = reverse_lazy('SupplierList')
    context_object_name = 'supp'


# **************************************************************************
# Customer
# **************************************************************************

class CustomerListView( LoginRequiredMixin ,View):
    def get(self , request):
        custList = Customer.objects.all().order_by('id')
        return render(request , 'masterdata/Customer/CustomerList.html', {'custList': custList })

    def post(self , request):
        pass

class CreateCustomerView(LoginRequiredMixin , CreateView):
    model = Customer
    form_class = ModifyCustomer
    template_name = 'masterdata/Customer/ModifyCustomer.html'
    success_url = reverse_lazy('CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Create"
        return context

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)
    
class EditCustomerView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = ModifyCustomer
    template_name = 'masterdata/Customer/ModifyCustomer.html'
    success_url = reverse_lazy('CustomerList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Update"
        return context

class DeleteCustomerView(LoginRequiredMixin , DeleteView ):
    model = Customer
    template_name = 'masterdata/Customer/DeleteCustomer.html'
    success_url = reverse_lazy('CustomerList')
    context_object_name = 'cust' 


def GetCustomerDetails(request, pk):
    
    """
    Retrieves the details of a customer
    """
    try:

        customer = get_object_or_404(Customer, pk=pk)

        # Return as a JSON response
        return JsonResponse({'id'   : customer.pk,
                             'name' : customer.name,
                             'mobileNo': str(customer.mobileNo)})
    
    except Exception as e:
        # Handle cases where the product is not found or other errors
        return JsonResponse({'error': 'Customer not found or invalid request'}, status=404)

# **************************************************************************
# Product
# **************************************************************************

class ProductListView( LoginRequiredMixin ,View):
    def get(self , request):
        prodList = Product.objects.all().order_by('id')
        return render(request , 'masterdata/Product/ProductList.html', {'prodList': prodList })

    def post(self , request):
        pass

class CreateProductView(LoginRequiredMixin , CreateView):
    model = Product
    form_class = ModifyProduct
    template_name = 'masterdata/Product/ModifyProduct.html'
    success_url = reverse_lazy('ProductList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'productCategory' ] = ProductCategory.objects.all()
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Create"
        return context  

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        return super().form_valid(form)
    

class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ModifyProduct
    template_name = 'masterdata/Product/ModifyProduct.html'
    success_url = reverse_lazy('ProductList')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context [ 'BtnText' ] = "Update"
        return context

class DeleteProductView(LoginRequiredMixin , DeleteView ):
    model = Product
    template_name = 'masterdata/Product/DeleteProduct.html'
    success_url = reverse_lazy('ProductList')
    context_object_name = 'prod'

def GetProductDetails(request, barCode):
    """
    Retrieves the details of a product using its barcode string.
    """
    try:
        cleaned_parameter = barCode.strip('"\'')
        product = get_object_or_404(Product, barCode=cleaned_parameter)

        # Return the price as a JSON response
        return JsonResponse({'barcode': product.barCode, 
                             'name' : product.name,
                             'price': str(product.salesPrice)})
    except Exception as e:
        # Handle cases where the product is not found or other errors
        return JsonResponse({'error': 'Product not found or invalid request'}, status=404)