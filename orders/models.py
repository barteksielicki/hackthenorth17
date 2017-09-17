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

    class Meta:
        ordering = ['is_done']


class Record(models.Model):
    RECORD_CHOICES = (
        ('image', 'Image'),
        ('text', 'Text'),
    )
    order = models.ForeignKey('Order')
    type = models.CharField(max_length=16, choices=RECORD_CHOICES)
    asset = models.TextField()
    is_done = models.BooleanField(default=False)
    labeled_as = models.TextField()

    class Meta:
        ordering = ['is_done']

    def check_if_done(self, answer):
        if self.label_set.filter(answer__iexact=answer).count() >= self.order.verifications_needed:
            self.labeled_as = answer
            self.is_done = True
            self.save()


class Label(models.Model):
    record = models.ForeignKey('Record')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    answer = models.TextField()
