from django.conf.urls import url

from orders.views import OrdersList, OrdersDetails, OrderUpload, OrderLabel

urlpatterns = [
    url(r"^$", OrdersList.as_view(), name="list"),
    url(r"^(?P<pk>[\d]+)/$", OrdersDetails.as_view(), name="details"),
    url(r"^new/$", OrderUpload.as_view(), name="new"),
    url(r"^label/$", OrderLabel.as_view(), name="label")
]