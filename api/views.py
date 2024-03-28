import warnings
warnings.filterwarnings("ignore", message= "Falling back to the 'python' engine because")
import pandas as pd
from io import StringIO
from django.db.utils import IntegrityError
from django.db.models import Sum
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from .models import Transaction


class TransactionStoreView(APIView):
    """
    This view helps to store multiple transanctions in database or
    delete all transactions from the database.
    """

    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.data['data']
        string_data = str(file_obj.read(), 'utf-8')
        try:
            df = pd.read_csv(StringIO(string_data), sep='\s*,\s*', comment='#',
                            names=Transaction.CSV_FIELDS)
            transaction_records = []
            for _, row in df.iterrows():
                transaction_records.append(
                    Transaction(**row)
                )
            Transaction.objects.bulk_create(transaction_records)
        except (IntegrityError, Exception) as ex:
            return Response(
                data={"detail": "Failed while parsing csv file. "\
                                "Please ensure the format is as given in the documentation."
                                " Additional error info: %s" % str(ex)},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(status=200)

    def delete(self, request):
        Transaction.objects.all().delete()
        return Response(status=200)

class ReportView(APIView):
    """
    This view returns a json response with the tally of gross revenue,
    expenses, and net revenue (gross - expenses)
    """

    def get(self, request):
        result_queryset = \
            Transaction.objects.values('type').annotate(sum=Sum('amount'))
        # To handle the case where no transactions are stored yet
        result = {
            "gross-revenue": 0,
            "expenses": 0,
            "net-revenue": 0
        }
        for entry in result_queryset:
            if entry["type"] == "Expense":
                result["expenses"] = entry["sum"]
            else:
                result["gross-revenue"] = entry["sum"]

        result["net-revenue"] = result["gross-revenue"] - result["expenses"]
        return Response(result)


