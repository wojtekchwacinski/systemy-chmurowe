# systemy-chmurowe
# Gen Z Social Media Usage App

Projekt na przedmiot **Systemy chmurowe**.

Aplikacja składa się z:

- bazy danych PostgreSQL,
- backendu REST API we Flasku,
- prostego frontendu HTML/JavaScript.

## LAB 1
Dataset pochodzi z Kaggle: **Gen-Z Social Media Usage Dataset**.
Dataset należy pobrać ręcznie z Kaggle i umieścić w folderze `backend` : https://www.kaggle.com/datasets/sharmajicoder/gen-z-social-media-usage-dataset
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
│   └── genz_social_media_usage_1M.csv
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

## Lab 2 – Wirtualizacja (Vagrant + Ansible)

W ramach zadania przygotowano środowisko projektu w postaci maszyny wirtualnej z wykorzystaniem narzędzi **Vagrant** oraz **Ansible** (infrastruktura jako kod).

### Cel

Celem było stworzenie powtarzalnego środowiska uruchomieniowego zawierającego wszystkie komponenty aplikacji:
- bazę danych PostgreSQL,
- backend (Flask),
- frontend (HTML/JavaScript).

Środowisko jest konfigurowane automatycznie przy użyciu Ansible.

---

## Wymagania

Do uruchomienia wymagane są:

- VirtualBox
- Vagrant

---

## Uruchomienie projektu

### 1. Uruchomienie maszyny wirtualnej

W głównym folderze projektu:

```bash
vagrant up
```

Podczas uruchamiania:
- tworzona jest maszyna wirtualna (Ubuntu),
- instalowane są zależności (Python, PostgreSQL),
- konfigurowane jest środowisko przy użyciu Ansible.

---

### 2. Połączenie z maszyną

```bash
vagrant ssh
```

---

### 3. Import danych

```bash
cd /vagrant/backend
python3 import_csv.py
```

---

### 4. Uruchomienie backendu

```bash
python3 app.py
```

Backend dostępny pod adresem:

```txt
http://127.0.0.1:5000
```

---

### 5. Uruchomienie frontendu

W drugim terminalu:

```bash
vagrant ssh
cd /vagrant/frontend
python3 -m http.server 5500
```

Frontend dostępny pod adresem:

```txt
http://127.0.0.1:5500
```

---

## Opis działania

- Vagrant odpowiada za tworzenie maszyny wirtualnej
- Ansible automatycznie konfiguruje środowisko (instaluje pakiety, bazę danych, zależności)
- Folder projektu jest współdzielony jako `/vagrant`
- Backend komunikuje się z bazą PostgreSQL
- Frontend komunikuje się z backendem przez REST API

---

## Endpointy API

- `GET /usage` – pobranie danych
- `GET /usage?platform=TikTok` – filtrowanie
- `GET /usage/<id>` – pobranie rekordu po ID
- `POST /usage` – dodanie rekordu
- `PUT /usage/<id>` – edycja rekordu
- `GET /stats` – statystyki

---

## Uwagi

- Dataset nie jest przechowywany w repozytorium (ze względu na rozmiar)
- Należy go pobrać z Kaggle i umieścić w `backend/data.csv`
- Endpoint `/usage` zwraca ograniczoną liczbę rekordów dla wydajności

---

## Lab 3 – Konteneryzacja (Docker)

W ramach zadania przygotowano konfigurację konteneryzacji całej aplikacji przy użyciu **Dockera** i **Docker Compose**.

### Cel

Celem było umieszczenie każdego komponentu aplikacji w osobnym kontenerze aplikacyjnym:
- baza danych PostgreSQL,
- backend (Flask),
- frontend (nginx).

Całość uruchamiana jest jedną komendą przy użyciu Docker Compose.

---

## Wymagania

Do uruchomienia wymagane są:

- Docker
- Docker Compose

---

## Uruchomienie projektu

### 1. Zbuduj obrazy i uruchom kontenery

W głównym folderze projektu:

```bash
docker compose up --build
```

Podczas uruchamiania:
- budowany jest obraz backendu na podstawie `backend/Dockerfile`,
- budowany jest obraz frontendu na podstawie `frontend/Dockerfile`,
- pobierany jest oficjalny obraz PostgreSQL 16,
- tworzona jest sieć łącząca wszystkie kontenery,
- backend czeka na gotowość bazy danych przed startem.

---

### 2. Sprawdź działające kontenery

```bash
docker ps
```

Powinny być widoczne trzy kontenery:

```txt
genz_db
genz_backend
genz_frontend
```

---

### 3. Import danych

W osobnym terminalu:

```bash
cd backend
python import_csv.py
```

---

## Adresy po uruchomieniu

Frontend:

```txt
http://localhost:8080
```

Backend API:

```txt
http://localhost:5000
```

---

## Testowanie API

### Pobranie rekordów

```txt
http://localhost:5000/usage
```

### Filtrowanie po platformie

```txt
http://localhost:5000/usage?platform=TikTok
```

### Pobranie rekordu po ID

```txt
http://localhost:5000/usage/1
```

### Statystyki

```txt
http://localhost:5000/stats
```

---

## Opis działania

- `db` – kontener z PostgreSQL, dane przechowywane w wolumenie `postgres_data`
- `backend` – kontener z Flask API, łączy się z bazą przez wewnętrzną sieć Dockera
- `frontend` – kontener z nginx serwującym stronę HTML

Backend nie startuje dopóki baza danych nie jest gotowa na połączenia (healthcheck).

Kontenery komunikują się przez wewnętrzną sieć Docker – backend adresuje bazę nazwą `db`, nie `localhost`.

---

## Zatrzymanie projektu

```bash
docker compose down
```

Aby zatrzymać i usunąć dane bazy:

```bash
docker compose down -v
```

---

## Uwagi

- Dataset nie jest przechowywany w repozytorium (ze względu na rozmiar)
- Należy go pobrać z Kaggle i umieścić w `backend/genz_social_media_usage_1M.csv`
- Endpoint `/usage` zwraca ograniczoną liczbę rekordów dla wydajności
