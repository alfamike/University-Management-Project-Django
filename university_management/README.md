# Academic Management Application


## Introduction

This application is an academic management interface built using Django to interact with an Hyperledfge Fabric blockchain network. It provides functionalities for managing students, courses, titles, and activities within a university.

## Prerequisites

Ensure you have the following set up:
1. Python 3.11 or higher
2. Django 4.0 or higher
3. Hyperledge Fabric 2.4 or higher
4. Hyperledge Fabric Python SDK 0.9
5. Docker 20.10 or higher
6. Docker Compose 1.29 or higher
7. MetaMask browser extension and a test Ethereum account

## Features

- User authentication and authorization (Web3 + JWT + CSRF)
- Student management (create, modify, remove, list)
- Course management (create, modify, remove, list)
- Title management (create, modify, remove, list)
- Activity management (create, modify, remove, list)
- Enroll and de-enroll students in courses
- Manage grades for courses and activities
- Chat functionality
- Connection via Hyperledge Fabric Python SDK to a Hyperledge Fabric

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd university-management
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the development server:
    ```bash
    python manage.py runserver_plus 0.0.0.0:8000 --cert-file certs/django.crt --key-file certs/django.key
    ```

## Configuration

### Settings

- `settings.py` contains the configuration for the Django project.
- Ensure to set the `SECRET_KEY` and `ALLOWED_HOSTS` appropriately for your environment.

### URLs

- The URL patterns are defined in `urls.py`.
- Ensure the URL names match the views and templates used in the project.

## Usage

1. Access the application at `http://127.0.0.1:8000/`.
2. Use the web interface to interact with titles, courses and students

## Templates

- The HTML templates are located in the `registration_app/templates` directory.


## Middleware

- Custom middleware for JWT authentication is defined in `registration_app/middleware.py`.


## License

This project is licensed under the GPL-3.0 License - see the `LICENSE` file for details.