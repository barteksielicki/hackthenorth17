import os
import zipfile
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.generic import ListView, DetailView, CreateView

from orders.forms import OrderForm, LabelForm
from orders.models import Order, Label, Record


@method_decorator(login_required, name="dispatch")
class OrdersList(ListView):
    template_name = "orders/list.html"

    def get_queryset(self):
        qs = self.request.user.order_set.all().prefetch_related('record_set')
        qs = qs.annotate(records_total=Count('record'))
        qs = qs.annotate(records_done=Sum('record__is_done'))
        return qs


@method_decorator(login_required, name="dispatch")
class OrdersDetails(DetailView):
    template_name = "orders/details.html"

    def get_queryset(self):
        # noinspection PyCallByClass
        return OrdersList.get_queryset(self)


@method_decorator(login_required, name="dispatch")
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


@method_decorator(login_required, name="dispatch")
class OrderLabel(CreateView):
    model = Label
    form_class = LabelForm
    template_name = "orders/label.html"

    @cached_property
    def record(self):
        qs = Record.objects.filter(is_done=False).exclude(label__user=self.request.user)
        if "record" in self.request.POST:
            return qs.filter(pk=self.request.POST.get("record"))
        else:
            return qs.order_by('?').first()

    def get_initial(self):
        return {
            "record": self.record
        }

    def get_context_data(self, **kwargs):
        kwargs['record'] = self.record
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse("orders:label")

    def form_valid(self, form):
        label = form.save(commit=False)
        label.user = self.request.user
        label.save()
        label.record.check_if_done(label.answer)
        return HttpResponseRedirect(self.get_success_url())
