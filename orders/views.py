import zipfile
from uuid import uuid4

import os
from django.conf import settings
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, FormView

from orders.forms import OrderForm
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


class OrderUpload(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/upload.html"

    def get_success_url(self):
        return reverse("orders:list")

    def form_valid(self, form):
        order = form.save(commit=False)
        order.issuer = self.request.user
        order.save()
        self.extract_zipfile(form.cleaned_data["zip_file"], order, form.cleaned_data["type"])
        return HttpResponseRedirect(self.get_success_url())

    def extract_zipfile(self, archive, order, type):
        unzipped = zipfile.ZipFile(archive)
        for old_filename in unzipped.namelist():
            _, ext = os.path.splitext(old_filename)
            new_filename = f"{uuid4().hex}{ext}"
            path = os.path.join(settings.MEDIA_ROOT, "storage", new_filename)
            asset_path = os.path.join(settings.MEDIA_URL, "storage", new_filename)

            with open(path, "wb") as f:
                f.write(unzipped.read(old_filename))

            order.record_set.create(asset=asset_path, type=type)
