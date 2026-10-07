from django.views.generic import DetailView, ListView

from .models import Apartment


class ApartmentListView(ListView):
    model = Apartment
    context_object_name = 'apartments'
    template_name = 'offers/list.html'


class ApartmentDetailView(DetailView):
    model = Apartment
    context_object_name = 'apartment'
    template_name = 'offers/detail.html'
