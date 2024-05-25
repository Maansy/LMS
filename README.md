
# Learning Management System (LMS)

This project is a Learning Management System (LMS) built with Django and Docker, utilizing PostgreSQL as the database and Adminer for database management.

## Features

- User authentication and authorization
- Course creation and management
- Module and lesson management
- Student enrollments
- Certificate generation upon course completion
- RESTful API endpoints
- Dockerized setup for easy deployment

## Prerequisites

- Docker
- Docker Compose
- Python 3.12 (if running without Docker)
- PostgreSQL (if running without Docker)

## Getting Started

### Clone the Repository

```sh
git clone https://github.com/Maansy/LMS.git
cd LMS
```

### Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```env
DB_NAME=lms
DB_USER=lmsuser
DB_PASS=lmspassword
DB_HOST=db
SECRET_KEY=your_django_secret_key
DEBUG=True
```

## Running with Docker

### Docker Setup

Build and start the Docker containers:

```sh
docker-compose build
docker-compose up
```

This will set up the Django application, PostgreSQL database, and Adminer, and will run the necessary migrations and commands.

### Access the Application

- **Django App**: `http://localhost:8000`
- **Adminer**: `http://localhost:8080`

### Adminer Login

Use the following credentials to log into Adminer:

- **System**: PostgreSQL
- **Server**: db
- **Username**: lmsuser
- **Password**: lmspassword
- **Database**: lms

### Running Management Commands

To run Django management commands inside the Docker container:

```sh
docker-compose run web python manage.py <command>
```

### Useful Commands

- **Migrations**: `docker-compose run web python manage.py makemigrations`
- **Apply Migrations**: `docker-compose run web python manage.py migrate`
- **Create Superuser**: `docker-compose run web python manage.py createsuperuser`
- **Run Tests**: `docker-compose run web python manage.py test`

## Running without Docker

### Setup PostgreSQL Database

Ensure PostgreSQL is installed and running. Create a database and user:

```sh
sudo -u postgres psql
```

Within the PostgreSQL shell:

```sql
CREATE DATABASE lms;
CREATE USER lmsuser WITH PASSWORD 'lmspassword';
GRANT ALL PRIVILEGES ON DATABASE lms TO lmsuser;
```

### Install Dependencies

Create a virtual environment and install dependencies:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Apply Migrations

Apply the database migrations:

```sh
python manage.py makemigrations
python manage.py migrate
```

### Create Groups and Permissions

Run the custom management command to create groups and assign permissions:

```sh
python manage.py create_group
```

### Start the Server

Start the Django development server:

```sh
python manage.py runserver
```

### Access the Application

- **Django App**: `http://localhost:8000`

## API Endpoints

### Authentication

- **Register**: `POST /api/register/`
- **Login**: `POST /api/token/`
- **Profile**: `GET /api/profile/`

### Courses

- **List/Create Courses**: `GET/POST /api/courses/`
- **Course Detail**: `GET/PUT/DELETE /api/courses/{course_id}/`
- **List/Create Modules**: `GET/POST /api/courses/{course_id}/modules/`
- **Module Detail**: `GET/PUT/DELETE /api/courses/{course_id}/modules/{module_id}/`
- **List/Create Lessons**: `GET/POST /api/courses/{course_id}/modules/{module_id}/lessons/`
- **Lesson Detail**: `GET/PUT/DELETE /api/courses/{course_id}/modules/{module_id}/lessons/{lesson_id}/`

### Enrollments

- **List/Create Enrollments**: `GET/POST /api/enrollments/`

### Certificates

- **List Certificates**: `GET /api/certificates/`
- **Generate Certificate**: `POST /api/certificates/generate/{course_id}/`

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## Acknowledgments

- Django REST framework for providing the tools to build the API
- Docker for containerization
- ReportLab for generating PDF certificates
- Adminer for database management

---