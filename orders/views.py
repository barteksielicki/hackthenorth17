from django.db.models import Count, Sum
from django.views.generic import ListView, DetailView

from orders.models import Order


class OrdersList(ListView):
    template_name = "orders/list.html"

    def get_queryset(self):
        qs = self.request.user.order_set.all().prefetch_related('record_set')
        qs = qs.annotate(records_total=Count('record'))
        qs = qs.annotate(records_done=Sum('record__is_done'))
        return qs


class OrdersDetails(DetailView):
    template_name = "orders/details.html"

    def get_queryset(self):
        # noinspection PyCallByClass
        return OrdersList.get_queryset(self)
