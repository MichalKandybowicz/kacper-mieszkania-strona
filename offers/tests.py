from decimal import Decimal
from importlib import import_module
from types import SimpleNamespace

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from .models import Apartment


class ApartmentTests(TestCase):
    def test_initial_migration_provides_eight_apartments(self):
        self.assertEqual(
            list(Apartment.objects.values_list('number', flat=True)),
            list(range(1, 9)),
        )

    def test_list_contains_all_apartments(self):
        response = self.client.get(reverse('offers:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['apartments']), 8)
        for apartment in Apartment.objects.all():
            self.assertContains(response, apartment.title)
            self.assertContains(response, apartment.get_absolute_url())

    def test_reapplying_sample_data_preserves_existing_offers(self):
        apartment = Apartment.objects.first()
        apartment.title = 'Zaktualizowana oferta'
        apartment.save()
        migration = import_module('offers.migrations.0002_sample_apartments')
        migration.create_sample_apartments(
            apps, SimpleNamespace(connection=connection)
        )
        apartment.refresh_from_db()
        self.assertEqual(Apartment.objects.count(), 8)
        self.assertEqual(apartment.title, 'Zaktualizowana oferta')

    def test_detail_displays_parameters_and_status(self):
        apartment = Apartment.objects.first()
        apartment.status = Apartment.Status.RESERVED
        apartment.save()
        response = self.client.get(apartment.get_absolute_url())
        self.assertContains(response, apartment.title)
        self.assertContains(response, '38,50 m²')
        self.assertContains(response, '385000,00 zł')
        self.assertContains(response, 'Parter')
        self.assertContains(response, 'Zarezerwowane')
        self.assertContains(response, 'Dane demonstracyjne')

    def test_unknown_apartment_returns_404(self):
        response = self.client.get(reverse('offers:detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)

    def test_empty_list(self):
        Apartment.objects.all().delete()
        response = self.client.get(reverse('offers:list'))
        self.assertContains(response, 'Obecnie nie ma ofert mieszkań.')

    def test_description_is_escaped(self):
        apartment = Apartment.objects.first()
        apartment.description = '<script>alert("test")</script>'
        apartment.save()
        response = self.client.get(apartment.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;')
        self.assertNotContains(response, '<script>')

    def test_nonpositive_parameters_are_invalid(self):
        for field in ('number', 'area', 'rooms', 'price'):
            with self.subTest(field=field):
                apartment = Apartment.objects.first()
                setattr(apartment, field, Decimal('0'))
                with self.assertRaises(ValidationError):
                    apartment.full_clean()

    def test_admin_requires_login(self):
        response = self.client.get(reverse('admin:offers_apartment_changelist'))
        self.assertRedirects(
            response, '/admin/login/?next=/admin/offers/apartment/',
            fetch_redirect_response=False,
        )
