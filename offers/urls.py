from django.urls import path

from .views import ApartmentDetailView, ApartmentListView

app_name = 'offers'

urlpatterns = [
    path('', ApartmentListView.as_view(), name='list'),
    path('mieszkania/<int:pk>/', ApartmentDetailView.as_view(), name='detail'),
]
