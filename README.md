# Library Project

A project for managing a library, 
including book borrowing and payments, user notifications, and inventory management. 
This project is built using Django REST Framework for the main API, FastAPI for a Telegram bot, Celery for asynchronous tasks, and Redis for caching.

## Table of Contents

- [Technologies](#technologies)
- [Features](#features)
- [Installation](#installation)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Technologies

The project is built with the following technologies:

- Django REST Framework – main API
- FastAPI – Telegram bot
- Stripe - for payment system
- Celery – for asynchronous tasks (notifications)
- Redis – as a broker for Celery and for caching
- PostgreSQL – database
- Docker – containerization of services

## Features

- Books: CRUD operations for managing books
- Users: authentication system, JWT tokens, updating Telegram ID
- Borrowings: book borrowing with inventory check and return reminders
- Payments: implemented simple payment system using Stripe API
- Telegram Bot: notifications for new borrowings and return reminders
- Caching: caching requests to improve performance
- Documentation: detailed explanation of all api endpoints

## Installation

1. Clone the repository:
```
git clone https://github.com/Narberal90/library-service-app.git
cd library-service-app
```

2. Set up `.env` files: Copy `.env.sample` as .env and configure environment variables:
- DJANGO_SECRET_KEY: The secret key for Django used to provide security.
- POSTGRES_HOST: The hostname or IP address of the PostgreSQL database server.
- POSTGRES_DB: The name of the PostgreSQL database to use.
- POSTGRES_USER: The username for connecting to the PostgreSQL database.
- POSTGRES_PASSWORD: The password for authenticating the PostgreSQL user.
- POSTGRES_PORT: The port on which the PostgreSQL database is running, typically 5432.
- STRIPE_SECRET_KEY: The secret API key for Stripe
- STRIPE_PUBLIC_KEY: The public API key for Stripe
- TELEGRAM_BOT_TOKEN: The token for accessing the Telegram Bot API to interact with Telegram users.

3. Run Docker Compose:
```bash
docker-compose up --build
```

4. Load initial data (if needed):
* load book data
```
docker-compose run app sh -c "python manage.py loaddata book_data.json"
```
* load user data
```
docker-compose run app sh -c "python manage.py loaddata user_data.json"
```
* load periodic tasks
```
docker-compose run app sh -c "python manage.py loaddata periodic_tasks.json"
```



### Using the Telegram Bot

- To receive notifications, users should send their email to the bot in Telegram to save their Telegram ID for notifications.

## Testing

To run tests:
```
docker-compose run app sh -c "python manage.py test"
```
## Troubleshooting

- Database Connection: If the database is unavailable, check .env configurations.
- Telegram Bot: If the bot is not sending messages, verify the token and bot permissions.
