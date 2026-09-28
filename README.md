# NaijaHomes - Nigerian Property & Rental Management Platform

A full-stack web application that connects landlords and tenants across Nigeria.
Built with Django (Python) backend and a plain HTML/CSS/JavaScript frontend.

---

## Project Overview

NaijaHomes solves the problem of finding and managing rental properties in Nigeria.
Landlords can list properties, tenants can search and apply, and both can track
everything through their dashboards.

---

## Technologies Used

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3, Django, Django REST Framework |
| Database    | SQLite                            |
| Frontend    | HTML5, CSS3, JavaScript (Vanilla) |
| Charts      | Matplotlib                        |
| API Format  | JSON (REST API)                   |
| CLI Tool    | Python argparse                   |

---

## Python Concepts Used

- Variables and Operators
- Conditional Statements (if/else)
- Loops (for loops in seed.py and cli.py)
- Functions (views, helper functions)
- Strings and String Formatting
- Lists and Dictionaries
- File Handling (CSV export, JSON import)
- Exception Handling (try/except in all views)
- JSON (API communication)
- REST API (Django REST Framework)
- Database Connectivity (Django ORM + SQLite)
- Data Visualization (Matplotlib charts)
- Automation (cli.py)
- Command Line Arguments (argparse)

---

## Project Structure

nigerian-property-project/
├── core/ → Django project settings and main URLs
├── accounts/ → User registration, login, profile
├── properties/ → Property listings, search, filter
├── applications/ → Rental applications management
├── templates/pages/ → 12 HTML frontend pages
├── static/css/ → Global stylesheet
├── static/js/ → Shared JavaScript functions
├── data/ → Sample JSON data and CSV exports
├── charts/ → Generated Matplotlib chart images
├── logs/ → Application activity logs
├── database/ → SQLite database file
├── cli.py → Command line tool
├── seed.py → Sample data loader
└── manage.py → Django management tool


---

## Setup Instructions

### 1. Install Python dependencies
```bash
pip install django djangorestframework django-cors-headers bcrypt pillow matplotlib
```

### 2. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Load sample data
```bash
python seed.py
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser

http://127.0.0.1:8000/


---

## Demo Accounts

| Role     | Email                | Password    |
|----------|----------------------|-------------|
| Landlord | landlord@demo.com    | password123 |
| Tenant   | tenant@demo.com      | password123 |

---

## Frontend Pages (12 Pages)

| Page                  | URL                      | Description                        |
|-----------------------|--------------------------|------------------------------------|
| Landing Page          | /                        | Homepage with featured properties  |
| Register              | /register/               | Create a new account               |
| Login                 | /login/                  | Login to existing account          |
| Dashboard             | /dashboard/              | Role-based user dashboard          |
| Property Listings     | /properties/             | Browse, search and filter          |
| Property Detail       | /property-detail/?id=1   | Full property info + apply         |
| Add Property          | /add-property/           | Landlord lists a new property      |
| Edit Property         | /edit-property/?id=1     | Landlord edits a listing           |
| My Applications       | /applications/           | Tenant tracks their applications   |
| Manage Applications   | /manage-applications/    | Landlord approves/rejects          |
| Profile               | /profile/                | View and edit user profile         |
| Statistics            | /stats/                  | Charts and platform analytics      |

---

## REST API Endpoints

### Accounts
| Method | Endpoint                        | Description          |
|--------|---------------------------------|----------------------|
| POST   | /api/accounts/register/         | Register new user    |
| POST   | /api/accounts/login/            | Login user           |
| GET    | /api/accounts/profile/<id>/     | Get user profile     |
| PUT    | /api/accounts/profile/<id>/     | Update user profile  |

### Properties
| Method | Endpoint                              | Description              |
|--------|---------------------------------------|--------------------------|
| GET    | /api/properties/                      | List all properties      |
| POST   | /api/properties/                      | Add new property         |
| GET    | /api/properties/<id>/                 | Get single property      |
| PUT    | /api/properties/<id>/                 | Update property          |
| DELETE | /api/properties/<id>/                 | Delete property          |
| GET    | /api/properties/landlord/<id>/        | Get landlord properties  |
| GET    | /api/properties/stats/summary/        | Get statistics           |
| GET    | /api/properties/export/csv/           | Export to CSV            |

### Applications
| Method | Endpoint                              | Description              |
|--------|---------------------------------------|--------------------------|
| POST   | /api/applications/                    | Submit application       |
| GET    | /api/applications/tenant/<id>/        | Tenant's applications    |
| GET    | /api/applications/landlord/<id>/      | Landlord's applications  |
| PUT    | /api/applications/<id>/update/        | Approve or reject        |

---

## CLI Tool Commands

```bash
python cli.py --report    # Print statistics report in terminal
python cli.py --charts    # Generate 3 Matplotlib chart images
python cli.py --export    # Export all properties to CSV file
python cli.py --backup    # Backup the SQLite database
python cli.py --seed      # Load sample data into database
python cli.py --all       # Run report, charts, export and backup
```

---

## Features Implemented

### Core Features
- User registration and login with encrypted passwords
- Role-based access (Tenant vs Landlord)
- Property listing with full CRUD (Create, Read, Update, Delete)
- Property search by keyword
- Filter by state, type, price range, and status
- Rental application submission and tracking
- Application approval and rejection by landlord
- User profile management
- Property availability status management

### Data Features
- SQLite database with 4 tables
- Sample dataset of 15 Nigerian properties
- JSON data import via seed.py
- CSV export via browser and CLI
- Activity logging to logs/app.log

### Visualization
- Bar chart: Properties by state
- Pie chart: Property type distribution
- Bar chart: Average rent by state
- Live statistics dashboard on /stats/ page

### Bonus Features
- Duplicate property detection
- Property recommendation (similar properties)
- Role-based dashboard
- Command line interface with argparse

---

## Sample Data

15 properties across 6 Nigerian states:
- **Lagos**: Lekki, Ajao Estate, Ikeja GRA, Ojota, Surulere, Banana Island, Yaba
- **Abuja**: Maitama, Wuse Zone 4, Garki
- **Rivers**: Port Harcourt GRA, Trans Amadi
- **Enugu**: GRA
- **Oyo**: Bodija, Ibadan
- **Edo**: Benin City GRA

Price range: ₦250,000 - ₦25,000,000 per year

---

## Author

**Victor Tamunotonye Bobmanuel**
400-Level Software Engineering Student
Augustine University, Ilara-Epe, Lagos

---

*Built as a final year project demonstrating full-stack web development
with Python, Django, REST API, SQLite, and data visualization.*