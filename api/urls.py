from django.urls import path
from .views import TransactionStoreView, ReportView


urlpatterns = [
   path('transactions/', TransactionStoreView.as_view(),
        name="store_transactions_from_file"),
   path('report/', ReportView.as_view(), name="report"),
]
