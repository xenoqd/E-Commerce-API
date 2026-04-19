# E-Commerce-API

E-Commerce-API is a backend API for e-commerce platformwith user authentication, shopping cart, product search.

## How to Run the Project without Docker

Requirements

- Python 3.8+

- PostgreSQL

- pip

- virtualenv (recommended)

- Redis

---

### 1. Clone the repository

```bash
git clone https://github.com/xenoqd/E-Commerce-API.git
cd E-Commerce-API

```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux / macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a .env file in the project root:

```env
# Database Configuration

# For local development without Docker (use psycopg2)
DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/ecommerce_db

# For Docker
# DATABASE_URL=postgresql+asyncpg://postgres:your_password@db:5432/ecommerce_db

# Alembic (sync driver required)
DATABASE_URL_ALEMBIC=postgresql+psycopg2://postgres:your_password@localhost:5432/ecommerce_db

POSTGRES_DB=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_strong_password_here
DB_HOST=localhost          # Use 'db' when running with Docker Compose
DB_PORT=5432

# Security & JWT

SECRET_KEY=your_super_secret_key_here_change_in_production
REFRESH_SECRET_KEY=your_refresh_secret_key_here_change_in_production

ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=30

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password   # Leave empty if no password

```

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Run development server

```bash
fastapi dev main.py
```

Run Celery services in separate terminals

```bash
# Celery Worker
celery -A backend.infrastructure.celery.celery_app worker -l info -P solo
```

```bash
# Celery Beat
celery -A backend.infrastructure.celery.celery_app beat -l info
```

```bash
# Order Worker
python -m backend.workers.order_worker
```

---

## How to Run the Project with Docker

### Edit the .env file and make sure you use the Docker-compatible settings

```env
# Database Configuration

# For local development without Docker (use psycopg2)
#DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/ecommerce_db

# For Docker
DATABASE_URL=postgresql+asyncpg://postgres:your_password@db:5432/ecommerce_db

# Alembic (sync driver required)
DATABASE_URL_ALEMBIC=postgresql+psycopg2://postgres:your_password@localhost:5432/ecommerce_db

POSTGRES_DB=ecommerce_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_strong_password_here
DB_HOST=db
DB_PORT=5432

# Security & JWT

SECRET_KEY=your_super_secret_key_here_change_in_production
REFRESH_SECRET_KEY=your_refresh_secret_key_here_change_in_production

ACCESS_TOKEN_EXPIRE_MINUTES=120
REFRESH_TOKEN_EXPIRE_DAYS=30

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password   # Leave empty if no password
```

Use DB_HOST=db, REDIS_HOST=redis and DATABASE_URL for docker when running with Docker

Start the Application with Docker Compose

```bash
# Build and start all services (first time or after changes)
docker compose up --build

# Run in detached mode (background)
docker compose up -d --build
```

---

## Features

User Authentication:

- User registration and login

- JWT based authentication stored in cookies

Cart:

- User can get cart

- User can add item to cart

- User can remove item from cart

- User can clear cart

Order:

- User can checkout

- User can get orders

- User can get order by id

Payments:

- User can pay order

Products:

- User can search products

- User can get products by id

## Admin Features

Products:

- Admin can create product

- Admin can edit product
