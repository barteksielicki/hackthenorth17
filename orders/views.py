import os
import zipfile
import functools

from uuid import uuid4

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import (
    Count,
    Sum,
)
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
)
from django.utils.functional import cached_property

from orders.forms import (
    LabelForm,
    OrderForm,
)
from orders.models import (
    Label,
    Order,
    Record,
)


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
        if form.cleaned_data["type"] == 'image':
            func = functools.partial(
                self.process_image,
                order=order,
                type_=form.cleaned_data["type"],
            )
        elif form.cleaned_data["type"] == 'text':
            func = functools.partial(
                self.process_text,
                order=order,
                type_=form.cleaned_data["type"],
            )
        for fname_data in self.extract_zipfile(form.cleaned_data['zip_file']):
            func(fname_data)
        return HttpResponseRedirect(self.get_success_url())

    def extract_zipfile(self, archive):
        unzipped = zipfile.ZipFile(archive)
        for old_filename in unzipped.namelist():
            print(old_filename, unzipped.read(old_filename))
            yield old_filename, unzipped.read(old_filename)

    def process_image(self, file_data, order, type_):
        old_filename, image_text = file_data
        _, ext = os.path.splitext(old_filename)
        new_filename = f"{uuid4().hex}{ext}"
        path = os.path.join(settings.MEDIA_ROOT, "storage", new_filename)
        asset_path = os.path.join(settings.MEDIA_URL, "storage", new_filename)

        with open(path, "wb") as f:
            f.write(image_text)

        order.record_set.create(asset=asset_path, type=type_)

    def process_text(self, file_data, order, type_):
        fname, text = file_data
        order.record_set.create(asset=text, type=type_)


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
