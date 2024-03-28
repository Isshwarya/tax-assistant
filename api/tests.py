from deepdiff import DeepDiff
from django.test import TestCase
from django.urls import reverse

from .models import Transaction

# Create your tests here.
class TransactionStoreTestCase(TestCase):

    report_url = reverse("report")
    store_transactions_url = reverse("store_transactions_from_file")

    def setUp(self):
        Transaction.objects.all().delete()

    def test_report_view_without_any_transactions(self):
        response = (self.client.get(self.report_url))
        expected_output = {
            'gross-revenue': 0, 'expenses': 0, 'net-revenue': 0
        }
        assert DeepDiff(expected_output, response.json()) == {}
        assert response.status_code == 200
        
    def test_report_view_after_posting_transactions(self):
        with open('summer-break/data.csv') as fp:
            response = (self.client.post(self.store_transactions_url, {'data': fp}))
        assert response.status_code == 200
        assert str(response.content, 'utf-8') == ""
        response = self.client.get(self.report_url)
        expected_output = {
            "gross-revenue":225.0, "expenses":72.93, "net-revenue":152.07
        }
        assert DeepDiff(expected_output, response.json())  == {}
        assert response.status_code == 200

    def test_negative_transactions_store_view(self):
        with open('summer-break/incorrect_data.csv') as fp:
            response = (self.client.post(self.store_transactions_url, {'data': fp}))
        expected_output = \
            {"detail": "Failed while parsing csv file. Please ensure the "\
                       "format is as given in the documentation"}
        assert response.status_code == 400
        assert DeepDiff(expected_output, response.json())  == {}

    def test_delete_all_transactions(self):
        with open('summer-break/data.csv') as fp:
            response = (self.client.post(self.store_transactions_url, {'data': fp}))
        assert response.status_code == 200
        assert str(response.content, 'utf-8') == ""
        response = self.client.delete(self.store_transactions_url)
        assert response.status_code == 200
        self.test_report_view_without_any_transactions()
