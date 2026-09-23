# 🎬 Movie Streaming Platform

A modern **full-stack movie streaming platform** built with a responsive **HTML, CSS, Bootstrap, and JavaScript frontend** and a powerful **Python Django + Django REST Framework backend**, using **MySQL** as the primary database.

The platform is designed to provide a complete movie browsing and streaming experience with user authentication, movie management, REST APIs, database integration, and an administrative dashboard.

---

## 📌 Project Overview

This project is a full-stack movie streaming web application developed with a clear separation between the frontend and backend.

Users can browse movies, view movie details, access streaming content, and interact with the platform through a responsive web interface.

The backend provides RESTful APIs for handling authentication, movie data, users, streaming metadata, and other application functionality.

### Architecture

```text
┌─────────────────────────────┐
│        Frontend             │
│ HTML5 + CSS3 + Bootstrap    │
│ JavaScript                  │
└──────────────┬──────────────┘
               │
               │ REST API
               ▼
┌─────────────────────────────┐
│        Django Backend       │
│ Python + Django             │
│ Django REST Framework       │
└──────────────┬──────────────┘
               │
               │ Django ORM
               ▼
┌─────────────────────────────┐
│          MySQL              │
│       Relational DB         │
└─────────────────────────────┘
```

---

## ✨ Features

### 🎥 Movie Features

* Browse available movies
* Movie cards with posters
* Movie details page
* Movie descriptions
* Genre and category information
* Release information
* Movie metadata
* Streaming interface
* Video/streaming metadata
* Responsive movie browsing experience

### 👤 User Features

* User registration
* User login
* Authentication
* User account management
* Protected backend functionality
* User-specific data handling

### 🔐 Backend Features

* Django-powered backend
* Django REST Framework APIs
* MySQL database integration
* Django ORM
* Authentication system
* Movie management
* User management
* Admin dashboard
* REST API architecture
* API documentation
* Business logic separation

### 📚 API Documentation

Interactive API documentation is available through:

* Swagger UI
* ReDoc
* Django Admin

---

# 🛠️ Technologies Used

| Technology            | Purpose                |
| --------------------- | ---------------------- |
| HTML5                 | Frontend structure     |
| CSS3                  | Styling                |
| Bootstrap             | Responsive UI          |
| JavaScript            | Frontend functionality |
| Python                | Backend programming    |
| Django                | Backend framework      |
| Django REST Framework | REST APIs              |
| MySQL                 | Primary database       |
| Django ORM            | Database interaction   |
| Swagger / OpenAPI     | API documentation      |
| ReDoc                 | API documentation      |
| Django Admin          | Administration         |
| Git                   | Version control        |
| GitHub                | Source code hosting    |

---

# 🗂️ Project Structure

A typical project structure is organized as follows:

```text
movie-streaming-platform/
│
├── movie_backend/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   │
│   ├── movie_backend/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── apps/
│   │   ├── users/
│   │   ├── movies/
│   │   └── ...
│   │
│   └── ...
│
├── frontend/
│   │
│   ├── index.html
│   ├── movies.html
│   ├── movie-details.html
│   ├── login.html
│   ├── signup.html
│   ├── watch.html
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── assets/
│
├── README.md
└── .gitignore
```

> The exact folder structure may vary depending on the final Django application configuration.

---

# 🗄️ Database

This project uses **MySQL** as the primary relational database.

Django communicates with MySQL through the Django ORM, allowing the application to work with users, movies, categories, metadata, and other application records.

### Database Technology

```text
Database: MySQL
Engine: django.db.backends.mysql
Port: 3306
Character Set: utf8mb4
```

---

# 💾 MySQL Setup

## 1. Install MySQL

Install MySQL Server on your system.

You can use any of the following environments:

* MySQL Server
* MySQL Workbench
* XAMPP
* WAMP
* MariaDB-compatible development environment

Verify that MySQL is installed:

```bash
mysql --version
```

---

## 2. Create the Database

Open MySQL and create the project database:

```sql
CREATE DATABASE movie_streaming_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Verify the database:

```sql
SHOW DATABASES;
```

You should see:

```text
movie_streaming_db
```

---

# ⚙️ Django MySQL Configuration

Inside:

```text
movie_backend/movie_backend/settings.py
```

configure the database:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "movie_streaming_db",
        "USER": "root",
        "PASSWORD": "your_mysql_password",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}
```

Replace:

```text
your_mysql_password
```

with your actual MySQL password.

### Recommended Configuration

For production or shared repositories, database credentials should be stored in environment variables rather than directly inside `settings.py`.

Example:

```env
DB_NAME=movie_streaming_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Never commit real database passwords to GitHub. Humans have invented `.env` files specifically because apparently putting passwords in public repositories wasn't a sustainable security strategy.

---

# 📦 Backend Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

A typical `requirements.txt` may contain:

```text
Django
djangorestframework
mysqlclient
```

If additional packages are used by the project, they should also be included in `requirements.txt`.

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/movie-streaming-platform.git
```

Navigate into the project:

```bash
cd movie-streaming-platform
```

---

# 🐍 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

# 📥 3. Install Dependencies

Navigate to the backend:

```bash
cd movie_backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🗄️ 4. Configure MySQL

Make sure your MySQL server is running.

Create the database:

```sql
CREATE DATABASE movie_streaming_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Then configure the MySQL credentials inside Django's settings or your environment configuration.

---

# 🔄 5. Run Django Migrations

Create migrations:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

This creates the required Django tables inside MySQL.

---

# 👨‍💼 6. Create Django Superuser

Create an administrator account:

```bash
python manage.py createsuperuser
```

Follow the terminal instructions to enter:

```text
Username
Email
Password
```

The superuser can access Django Admin.

---

# ▶️ 7. Start the Backend Server

The current development server can be started with:

```bash
python manage.py runserver 127.0.0.1:8000
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

# 📚 API Documentation

The project provides interactive API documentation.

## Swagger UI

```text
http://127.0.0.1:8000/api/docs/
```

Swagger provides an interactive interface for exploring and testing available REST API endpoints.

## ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

ReDoc provides a clean documentation interface for the API.

---

# 🔧 Django Admin

The Django administration panel is available at:

```text
http://127.0.0.1:8000/admin/
```

The admin panel can be used to manage backend data such as:

* Users
* Movies
* Categories
* Genres
* Movie metadata
* Streaming information
* Other registered Django models

---

# 🔑 Demo Credentials

### Admin

```text
Email: admin@moviesite.com
Password: admin123
```

### Demo User

```text
Email: demo@moviesite.com
Password: Password123!
```

> These credentials are intended for local/demo development. Change or remove them before deploying the application publicly.

---

# 🖥️ Frontend Setup

The frontend is built using:

* HTML5
* CSS3
* Bootstrap
* JavaScript

You can open the frontend using **VS Code Live Server** or another local static server.

For example:

```text
http://127.0.0.1:5500/
```

The frontend communicates with the Django backend through REST APIs.

---

# 🔗 API Base URL

During local development, the frontend can use:

```text
http://127.0.0.1:8000/api
```

Example JavaScript configuration:

```javascript
const API_BASE_URL = "http://127.0.0.1:8000/api";
```

Frontend requests can then be sent to the appropriate backend endpoints.

---

# 🔄 Application Workflow

The general application flow is:

```text
User
 │
 ▼
Frontend
 │
 │ HTTP Request
 ▼
Django REST API
 │
 ▼
Django Views / API Views
 │
 ▼
Business Logic
 │
 ▼
Django ORM
 │
 ▼
MySQL Database
 │
 ▼
Response
 │
 ▼
Frontend
 │
 ▼
User
```

---

# 🔐 Authentication Flow

A typical authentication workflow:

```text
User
 │
 ├── Register
 │
 ▼
Django API
 │
 ▼
User Validation
 │
 ▼
MySQL
 │
 ▼
Account Created
```

For login:

```text
User Login
     │
     ▼
Frontend
     │
     ▼
Authentication API
     │
     ▼
Django Authentication
     │
     ▼
User Database
     │
     ▼
Authentication Response
     │
     ▼
Frontend
```

---

# 🎬 Movie Data Flow

Movie information is managed by the Django backend.

```text
Admin
  │
  ▼
Django Admin
  │
  ▼
Movie Models
  │
  ▼
MySQL
  │
  ▼
REST API
  │
  ▼
Frontend
  │
  ▼
Movie Cards / Details
```

---

# 🧪 API Testing

The backend API can be tested using:

### Swagger

```text
http://127.0.0.1:8000/api/docs/
```

### ReDoc

```text
http://127.0.0.1:8000/api/redoc/
```

### Postman

You can also import and test API endpoints using Postman.

Typical API operations include:

```text
GET
POST
PUT
PATCH
DELETE
```

Depending on the endpoint and permissions configured in the backend.

---

# 🧰 Development Commands

## Start Django Server

```bash
python manage.py runserver 127.0.0.1:8000
```

## Create Migrations

```bash
python manage.py makemigrations
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Django Shell

```bash
python manage.py shell
```

## Run Tests

```bash
python manage.py test
```

---

# 🔍 Checking MySQL Connection

If Django cannot connect to MySQL, verify:

```text
MySQL Server → Running
Database Name → movie_streaming_db
Username → Correct
Password → Correct
Host → 127.0.0.1
Port → 3306
```

You can test MySQL manually:

```bash
mysql -u root -p
```

Then:

```sql
USE movie_streaming_db;
```

---

# ⚠️ Troubleshooting

## MySQL Connection Error

If Django reports a database connection error, check:

1. MySQL Server is running.
2. Database name is correct.
3. MySQL username is correct.
4. MySQL password is correct.
5. Host is correct.
6. Port is correct.
7. `mysqlclient` is installed.

Install the MySQL Django driver:

```bash
pip install mysqlclient
```

---

## Migration Error

Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

If the database was recreated, make sure the MySQL database exists before running migrations.

---

## Port 8000 Already in Use

Run Django on another port:

```bash
python manage.py runserver 127.0.0.1:8001
```

Then update the frontend API URL accordingly:

```javascript
const API_BASE_URL = "http://127.0.0.1:8001/api";
```

---

## Frontend Cannot Connect to Backend

Check that Django is running:

```text
http://127.0.0.1:8000/
```

Then check the API:

```text
http://127.0.0.1:8000/api/
```

Also verify:

* API URL
* CORS configuration
* Backend server
* Browser console errors
* Network requests
* API endpoint paths

---

# 🔒 Security Considerations

Before deploying the application to production:

* Change demo/admin passwords
* Never expose database passwords
* Use environment variables
* Set `DEBUG=False`
* Configure `ALLOWED_HOSTS`
* Configure CORS properly
* Enable HTTPS
* Protect API endpoints
* Configure CSRF protection
* Use secure authentication
* Protect session cookies
* Configure secure headers
* Restrict database access
* Validate user input
* Sanitize uploaded files
* Configure static and media files correctly
* Use a production WSGI/ASGI server
* Enable appropriate logging and monitoring

---

# 🌐 Production Deployment

For production deployment, the application can be deployed using services such as:

* AWS
* Google Cloud
* Microsoft Azure
* DigitalOcean
* Render
* Railway
* VPS hosting

A production architecture can look like:

```text
                     Internet
                        │
                        ▼
                   Nginx / CDN
                        │
                        ▼
                Django Application
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
           REST API           Static/Media
              │
              ▼
            MySQL
```

For large-scale streaming applications, video delivery should generally be handled using dedicated object storage and CDN infrastructure rather than serving large video files directly through Django.

---

# 🚀 Future Improvements

Planned or possible improvements include:

### 🔎 Search

* Movie search
* Advanced filtering
* Genre filtering
* Actor/director search

### ⭐ User Features

* Watchlist
* Favorites
* Watch history
* Continue watching
* Ratings
* Reviews
* Personalized profiles

### 🤖 AI Features

* Movie recommendation system
* Personalized recommendations
* Similar movie detection
* Content-based recommendations
* Collaborative filtering
* AI-powered movie search

### 🎞️ Streaming Improvements

* Multiple video qualities
* Adaptive streaming
* Subtitles
* Multiple languages
* Trailers
* Video progress tracking
* Continue watching

### 👥 Movie Information

* Actor profiles
* Director profiles
* Cast information
* Production information
* Related movies

### ⚡ Performance

* Redis caching
* Celery background tasks
* Database optimization
* API caching
* CDN integration
* Image optimization

### 🐳 DevOps

* Docker
* Docker Compose
* CI/CD
* Automated testing
* Cloud deployment
* Monitoring
* Logging

---

# 🧪 Testing Roadmap

Future testing can include:

```text
Unit Testing
Integration Testing
API Testing
Authentication Testing
Database Testing
Frontend Testing
Security Testing
Performance Testing
```

Django's built-in testing framework can be used for backend tests.

Run:

```bash
python manage.py test
```

---

# 📊 Database Design

The MySQL database can contain entities such as:

```text
Users
 │
 ├── Authentication
 └── User Profile

Movies
 │
 ├── Title
 ├── Description
 ├── Poster
 ├── Release Information
 ├── Genre
 └── Streaming Metadata

Genres
 │
 └── Movie Categories

Streaming
 │
 ├── Video URL
 ├── Quality
 ├── Language
 └── Subtitle Information
```

The exact schema depends on the Django models implemented in the backend.

---

# 📱 Responsive Design

The frontend is designed to work across different screen sizes:

```text
Desktop
   │
   ├── Large Screens
   │
   ├── Laptop
   │
   └── Tablet
       
Mobile
   │
   ├── Android
   └── iOS
```

Bootstrap's responsive grid and CSS media queries are used to improve compatibility across devices.

---

# 📌 Local Development URLs

| Service      | URL                                |
| ------------ | ---------------------------------- |
| Backend      | `http://127.0.0.1:8000/`           |
| Swagger      | `http://127.0.0.1:8000/api/docs/`  |
| ReDoc        | `http://127.0.0.1:8000/api/redoc/` |
| Django Admin | `http://127.0.0.1:8000/admin/`     |
| Frontend     | `http://127.0.0.1:5500/`           |

---

# 📝 Environment Variables

For production or collaborative development, use a `.env` file.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=False

DB_NAME=movie_streaming_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Do not commit `.env` to GitHub.

---

# 🚫 Recommended `.gitignore`

A `.gitignore` file should include:

```gitignore
venv/
env/
.venv/

__pycache__/
*.pyc

.env

*.log

.DS_Store

.idea/
.vscode/

media/
staticfiles/
```

---

# ⚖️ Content & Streaming Notice

This project is intended for **educational, development, and portfolio purposes**.

Only use movies, videos, posters, thumbnails, subtitles, trailers, and other media that you have the legal right or appropriate license to distribute.

The platform should not be used to distribute copyrighted content without authorization.

---

# 🎯 Learning Objectives

This project demonstrates practical experience with:

* Full-stack web development
* Django development
* Django REST Framework
* REST API architecture
* MySQL database integration
* Django ORM
* Authentication
* CRUD operations
* Frontend development
* Bootstrap responsive design
* JavaScript API integration
* Database migrations
* API documentation
* Django Admin
* Backend/frontend integration
* Application deployment concepts

---

# 👨‍💻 Author

## Md Rafej Khan

**AI/ML Engineer | Python Developer | Data Analyst | Full-Stack Developer**

### Areas of Expertise

* Artificial Intelligence
* Machine Learning
* Generative AI
* Python
* Django
* Django REST Framework
* FastAPI
* Data Science
* Deep Learning
* REST APIs
* Backend Development
* Full-Stack Web Development
* MySQL
* PostgreSQL
* Cloud Deployment

---

# ⭐ Project Purpose

This project was developed as a practical full-stack application to demonstrate how a modern web platform can combine:

```text
Frontend
   +
REST API
   +
Django Backend
   +
MySQL Database
   +
Authentication
   +
Admin Dashboard
   +
API Documentation
   =
Full-Stack Movie Streaming Platform
```

---

# 📄 License

This project can be used for educational and portfolio purposes.

If you plan to deploy or distribute the platform commercially, ensure that all third-party libraries, media assets, movie content, images, fonts, APIs, and other resources are used according to their respective licenses and terms.

---

# ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

**Built with Python, Django, Django REST Framework, MySQL, HTML, CSS, Bootstrap, and JavaScript.**

### Developed by Md Rafej Khan
