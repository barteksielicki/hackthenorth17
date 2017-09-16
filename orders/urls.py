from django.conf.urls import url

from orders.views import OrdersList, OrdersDetails

urlpatterns = [
    url(r"^$", OrdersList.as_view(), name="list"),
    url(r"^(?P<pk>[\d]+)/$", OrdersDetails.as_view(), name="details")
]