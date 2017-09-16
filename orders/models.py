from django.conf import settings
from django.db import models


class Order(models.Model):
    issuer = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_issued = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=32)
    verifications_needed = models.PositiveIntegerField(default=3)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    description = models.TextField()
    currency = models.CharField(max_length=16, choices=(
        ('bitcoin', 'BITCOIN'),
        ('litecoin', 'LITECOIN'),
        ('etherum', 'ETHEREUM')
    ))
    is_done = models.BooleanField(default=False)


class Record(models.Model):
    order = models.ForeignKey('Order')
    type = models.CharField(max_length=16) # todo: enum
    asset = models.TextField()
    is_done = models.BooleanField(default=False)
    labeled_as = models.TextField()


class Label(models.Model):
    record = models.ForeignKey('Record')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    answer = models.TextField()





