from django.urls import path
from .views import SalesInvoiceView , SalesInvoiceListView , DeleteSalesInvoiceListItemView

urlpatterns = [

    path('sales/', SalesInvoiceView.as_view(), name="sales"),
    path('SalesInvoiceList/', SalesInvoiceListView.as_view(), name="SalesInvoiceList"),
    path('DeleteSalesInvoiceListItem/<int:pk>', DeleteSalesInvoiceListItemView.as_view(), name='DeleteSalesInvoiceListItem'),

]