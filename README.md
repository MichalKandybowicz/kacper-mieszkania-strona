# Mieszkania — podstawowy projekt Django

Polskojęzyczna, responsywna strona prezentująca 8 mieszkań. Zawiera listę
ofert, strony szczegółów (metraż, pokoje, piętro, cena, opis i status)
oraz panel administracyjny do zarządzania mieszkaniami. Baza SQLite.

## Uruchomienie lokalne

Wymagany Python 3.10 lub nowszy. W katalogu projektu (Linux/macOS):

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export DJANGO_DEBUG=1
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Strona: http://127.0.0.1:8000/

Panel administracyjny: http://127.0.0.1:8000/admin/

Migracja danych automatycznie tworzy 8 **przykładowych** ofert na nowej bazie.
Kolejne uruchomienie `migrate` nie powiela danych. Opisy, parametry i ceny należy
zastąpić rzeczywistymi danymi w panelu administratora. Można dodawać kolejne
mieszkania oraz oznaczać je jako dostępne, zarezerwowane lub sprzedane.
Nie ma publicznej rejestracji ani formularza edycji ofert.

## Sprawdzenie projektu

Po aktywacji środowiska i ustawieniu `DJANGO_DEBUG=1`:

```sh
python manage.py check
python manage.py test offers
python manage.py makemigrations --check --dry-run
```

## Konfiguracja wdrożenia

Tryb debugowania jest domyślnie wyłączony. Poza środowiskiem lokalnym ustaw:

- `DJANGO_SECRET_KEY` — własny, losowy i stały sekret, przekazany przez środowisko;
  nie zapisuj go w repozytorium. Możesz wygenerować go poleceniem
  `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
- `DJANGO_ALLOWED_HOSTS` — lista nazw domen rozdzielona przecinkami.
- `DJANGO_DEBUG=0` — bez szczegółowych komunikatów błędów; ciasteczka sesji
  i CSRF wymagają wtedy HTTPS.

Plik `.env` nie jest automatycznie wczytywany. Zmienne muszą zostać ustawione
w powłoce lub konfiguracji serwera. Lokalnie można ustawić stały
`DJANGO_SECRET_KEY`; bez niego tryb debugowania generuje klucz przy starcie.

Przed publikacją uruchom `python manage.py check --deploy`, wykonaj migracje
i `python manage.py collectstatic`. Skonfiguruj serwer WSGI/ASGI, obsługę
plików z `staticfiles/`, HTTPS oraz pozostałe ustawienia zgodnie z
[listą kontrolną Django](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/).
`runserver` służy wyłącznie do pracy lokalnej.