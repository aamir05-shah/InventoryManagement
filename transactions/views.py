from django.shortcuts import render 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView , View , DeleteView
from .forms import SalesTransaction, SalesItemFormSet 
from .models import TransactionHeader
from masterdata.models import Customer, Product
from django.db import transaction
# **************************************************************************
# Sales Invoice
# **************************************************************************

class SalesInvoiceView(LoginRequiredMixin, CreateView):
    
    model         = TransactionHeader    
    template_name = 'transactions/sales/salesInvoice.html'
    form_class    = SalesTransaction
    success_url   = reverse_lazy('SalesInvoiceList')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SalesItemFormSet(self.request.POST, instance=self.object)
        else:
            data['items'] = SalesItemFormSet(instance=self.object)
        return data
    
  

    def form_valid(self, form):
        
        context = self.get_context_data()
        items = context['items']
        
        self.object = form.save(commit=False)
        self.object.tranType = "S"   
                
        with transaction.atomic():
        
            self.object.tranType = "S"
            self.object.grossAmount = 0
            
            if items.is_valid():
                self.object = form.save( )
                items.instance = self.object
                items.save( )
            else:
                return self.form_invalid(form)
        return super().form_valid(form)
    
    def form_invalid(self, form, **kwargs): 
        # Ensure formset errors are displayed when the main form is invalid
        form.add_error(None, "A custom error occurred in form_invalid.")
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_object_name(self, obj):
        object = super().get_context_object_name(obj)
        object [ 'BtnText' ] = "View History"
        return super().get_context_object_name(obj)
        
   
class SalesInvoiceListView( LoginRequiredMixin ,View):

    def get(self , request):
        salesList = TransactionHeader.objects.all().order_by('id').reverse()  
        return render(request , 'transactions/sales/SalesInvoiceList.html', {'salesList': salesList })
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context [ 'BtnText' ] = "Cancel"
    #     return context



    def post(self , request):
        pass
    
    
    def get_context_object_name(self, obj):
        object = super().get_context_object_name(obj)
        object [ 'BtnText' ] = "View History"
        return super().get_context_object_name(obj)


class DeleteSalesInvoiceListItemView(LoginRequiredMixin , DeleteView ):
    model = TransactionHeader
    template_name = 'transactions/sales//DeleteSalesInvoiceListItem.html'
    success_url = reverse_lazy('SalesInvoiceList')
    context_object_name = 'sales'
   

    #    def get_context_data(self, **kwargs):
    #         context = super().get_context_data(**kwargs)
    #         context [ 'BtnText' ] = "View History"
    #         return context


        
    
   