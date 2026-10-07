from django.db import migrations


def create_sample_apartments(apps, schema_editor):
    Apartment = apps.get_model('offers', 'Apartment')
    samples = [
        (1, 'Przytulne dwa pokoje', '38.50', 2, 0, '385000.00'),
        (2, 'Przestrzeń na dobry początek', '42.00', 2, 0, '420000.00'),
        (3, 'Komfort dla rodziny', '56.30', 3, 1, '563000.00'),
        (4, 'Jasne mieszkanie trzypokojowe', '61.20', 3, 1, '612000.00'),
        (5, 'Kompaktowe i funkcjonalne', '35.80', 2, 2, '358000.00'),
        (6, 'Miejsce na Twój dom', '58.40', 3, 2, '584000.00'),
        (7, 'Cztery pokoje, wiele możliwości', '74.60', 4, 3, '746000.00'),
        (8, 'Przestronny apartament', '82.10', 4, 3, '821000.00'),
    ]
    for number, title, area, rooms, floor, price in samples:
        Apartment.objects.using(schema_editor.connection.alias).create(
            number=number,
            title=title,
            area=area,
            rooms=rooms,
            floor=floor,
            price=price,
            status='available',
            description=(
                f'Przykładowe mieszkanie M{number} o powierzchni {area} m², '
                f'z liczbą pokoi: {rooms}. Funkcjonalna przestrzeń do '
                'zaaranżowania według własnych potrzeb.\n\n'
                'Dane demonstracyjne — uzupełnij opis, cenę i parametry '
                'rzeczywistego mieszkania w panelu administracyjnym.'
            ),
        )


class Migration(migrations.Migration):
    dependencies = [('offers', '0001_initial')]

    operations = [
        migrations.RunPython(create_sample_apartments, migrations.RunPython.noop),
    ]
