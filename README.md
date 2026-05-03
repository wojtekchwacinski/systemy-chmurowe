# systemy-chmurowe
# Gen Z Social Media Usage App

Projekt na przedmiot **Systemy chmurowe**.

Aplikacja składa się z:

- bazy danych PostgreSQL,
- backendu REST API we Flasku,
- prostego frontendu HTML/JavaScript.

Dataset pochodzi z Kaggle: **Gen-Z Social Media Usage Dataset**.

## Funkcje aplikacji

| Metoda | Endpoint | Opis |
|---|---|---|
| GET | `/usage` | pobiera rekordy z bazy |
| GET | `/usage?platform=TikTok` | filtruje rekordy po platformie |
| GET | `/usage/<id>` | pobiera jeden rekord po ID |
| POST | `/usage` | dodaje nowy rekord |
| PUT | `/usage/<id>` | aktualizuje istniejący rekord |
| GET | `/stats` | zwraca statystyki użycia social mediów |

Endpoint `/usage` zwraca maksymalnie 100 rekordów, żeby aplikacja działała płynnie przy dużym zbiorze danych.

## Struktura projektu

```txt
systemy-chmurowe/
├── docker-compose.yml
├── backend/
│   ├── app.py
│   ├── import_csv.py
│   ├── requirements.txt
│   └── data.csv
└── frontend/
    └── index.html
```

## Wymagania

Do uruchomienia potrzebne są:

- Python 3,
- Docker,
- Docker Compose,
- przeglądarka internetowa.

## Uruchomienie projektu

### 1. Uruchom bazę danych

W głównym folderze projektu:

```bash
docker compose up -d
```

PostgreSQL działa na porcie:

```txt
5433
```

### 2. Przejdź do folderu backendu

```bash
cd backend
```

### 3. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 4. Przygotuj plik CSV

Pobierz dataset z Kaggle i zapisz plik jako:

```txt
backend/data.csv
```

Plik powinien zawierać kolumny:

```txt
age
gender
country
daily_usage_hours
primary_platform
num_platforms_used
purpose
avg_session_minutes
night_usage
mental_health_score
addiction_level
screen_time_before_sleep
```

### 5. Zaimportuj dane do bazy

```bash
python import_csv.py
```

Po poprawnym imporcie pojawi się komunikat:

```txt
Import zakończony
```

### 6. Uruchom backend

```bash
python app.py
```

Backend będzie dostępny pod adresem:

```txt
http://127.0.0.1:5000
```

### 7. Uruchom frontend

W drugim terminalu przejdź do folderu `frontend`:

```bash
cd ../frontend
```

Uruchom prosty serwer HTTP:

```bash
python -m http.server 5500
```

Frontend będzie dostępny pod adresem:

```txt
http://127.0.0.1:5500
```

## Testowanie API

### Pobranie rekordów

```txt
http://127.0.0.1:5000/usage
```

### Filtrowanie po platformie

```txt
http://127.0.0.1:5000/usage?platform=TikTok
```

### Pobranie rekordu po ID

```txt
http://127.0.0.1:5000/usage/1
```

### Statystyki

```txt
http://127.0.0.1:5000/stats
```

## Opis działania

Po uruchomieniu aplikacji frontend komunikuje się z backendem przez REST API.

Użytkownik może:

- przeglądać rekordy,
- filtrować dane po platformie społecznościowej,
- pobierać rekord po ID,
- dodawać nowe rekordy,
- edytować istniejące rekordy,
- wyświetlać statystyki.

Dodawanie rekordu odbywa się przez metodę `POST`, a edycja przez metodę `PUT`.

## Przykładowe statystyki

Endpoint:

```txt
GET /stats
```

zwraca średnie wartości dla każdej platformy:

- średni dzienny czas użycia,
- średni wynik zdrowia psychicznego,
- liczba użytkowników.

## Uwagi

Ponieważ dataset może zawierać bardzo dużo rekordów, endpoint `/usage` zwraca tylko pierwsze 100 rekordów posortowanych po `id`.

Dzięki temu frontend nie zawiesza się przy pobieraniu danych.

Dataset należy pobrać ręcznie z Kaggle i umieścić w folderze `backend` : https://www.kaggle.com/datasets/sharmajicoder/gen-z-social-media-usage-dataset