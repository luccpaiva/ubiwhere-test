# Traffic Monitoring API

Django REST API for monitoring road traffic intensity based on speed readings.

## Project Structure

```
ubiwhere-test/
├── traffic_api/              # Django project configuration
│   ├── settings.py           # Project settings (Spectacular)
│   ├── urls.py               # Main URL configuration
│   └── wsgi.py
├── monitoring/               # Main application
│   ├── models.py             # RoadSegment, SpeedReading models
│   ├── admin.py              # Django admin config
│   ├── migrations/           # Database migrations
│   └── views.py
├── data/                     # Data files for import
│   ├── traffic_speed.csv
│   └── sensors.csv
├── venv/                     # Virtual environment
├── manage.py
├── requirements.txt
└── db.sqlite3                # SQLite database
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

### 5. Run development server

```bash
python manage.py runserver
```

- Admin panel: http://127.0.0.1:8000/admin/
- API docs: http://127.0.0.1:8000/api/docs/ (when implemented)
