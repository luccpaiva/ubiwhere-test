# Traffic Monitoring API

Django Framework REST API for monitoring road traffic intensity based on speed readings.

## Project Structure

```
ubiwhere-test/
├── traffic_api/                    # Django project configuration
│   ├── settings.py                 # Project settings (DRF, Spectacular)
│   ├── urls.py                     # Main URL configuration
│   └── wsgi.py
├── monitoring/                     # Main application
│   ├── models.py                   # RoadSegment, SpeedReading models
│   ├── serializers.py              # API serializers
│   ├── views.py                    # ViewSets (API endpoints)
│   ├── urls.py                     # API URL routing
│   ├── permissions.py              # Custom permissions (IsAdminOrReadOnly)
│   ├── admin.py                    # Django admin configuration
│   ├── management/
│   │   └── commands/
│   │       └── import_traffic_data.py  # Data import command
│   └── migrations/                 # Database migrations
├── data/                           # Data files for import
│   ├── traffic_speed.csv
│   └── sensors.csv
├── venv/                           # Venv
├── manage.py
├── requirements.txt
└── db.sqlite3                      # SQLite
```

## Setup

### 1. Create and activate virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Create superuser

```bash
python manage.py createsuperuser
```

### 5. Import data

```bash
python manage.py import_traffic_data data/traffic_speed.csv
```

### 6. Run development server

```bash
python manage.py runserver
```

## Access Points

- Admin panel: http://127.0.0.1:8000/admin/
- API docs: http://127.0.0.1:8000/api/docs/
- API endpoints: http://127.0.0.1:8000/api/road-segments/, http://127.0.0.1:8000/api/speed-readings/
