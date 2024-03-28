from django.db import models

# A base class to accommodate future changes or features needed
# across all models
class CustomBaseModel(models.Model):
    def save(self, *args, **kwargs):
        # Does validation
        self.full_clean()
        return super(CustomBaseModel, self).save(*args, **kwargs)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Transaction(CustomBaseModel):

    TRANSACTION_TYPE = (
        ("EXP", "Expense"),
        ("INC", "Income")
    )

    CSV_FIELDS = [
        "date", "type", "amount", "memo"
    ]

    date = models.DateField("Transaction Date")
    type = models.CharField("Type", max_length=3, choices=TRANSACTION_TYPE)
    amount = models.FloatField("Amount")
    memo = models.TextField("Memo")

    def __str__(self):
        return "Date: {}, Type: {}, Amount: {}".format(
            self.date, self.type, self.amount)
