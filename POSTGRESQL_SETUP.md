# PostgreSQL Setup Guide for LeetQode

This guide covers setting up PostgreSQL for both local development and production deployment.

## 🏠 Local Development Setup

### Prerequisites

1. **Install PostgreSQL**
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```

2. **Create Database User** (optional, can use default 'postgres' user)
   ```bash
   sudo -u postgres psql
   CREATE USER leetqode_user WITH PASSWORD 'your_password';
   ALTER USER leetqode_user CREATEDB;
   \q
   ```

### Quick Setup

1. **Run the setup script:**
   ```bash
   cd backend
   python setup_postgresql.py
   ```

2. **Or manual setup:**
   ```bash
   # Create database
   createdb leetqode_db
   
   # Update .env file
   DATABASE_URL=postgresql://postgres:password@localhost:5432/leetqode_db
   
   # Run migrations
   python manage.py migrate
   
   # Seed database
   python manage.py seed_problems
   ```

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql://postgres:password@localhost:5432/leetqode_db

# Google OAuth2 Settings
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# CORS Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## 🚀 Production Deployment

### Option 1: Heroku

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Add PostgreSQL Add-on**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set DEBUG=False
   heroku config:set GOOGLE_OAUTH2_CLIENT_ID=your-client-id
   heroku config:set GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   ```

5. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py seed_problems
   ```

### Option 2: DigitalOcean App Platform

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect your GitHub repository
   - Select "Web Service"

2. **Configure Environment**
   ```yaml
   # .do/app.yaml
   name: leetqode
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/leetqode
       branch: main
     run_command: gunicorn leetqode.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: SECRET_KEY
       value: your-production-secret-key
     - key: DEBUG
       value: "False"
     - key: GOOGLE_OAUTH2_CLIENT_ID
       value: your-client-id
     - key: GOOGLE_OAUTH2_CLIENT_SECRET
       value: your-client-secret
     - key: ALLOWED_HOSTS
       value: your-app-name.ondigitalocean.app
   databases:
   - name: leetqode-db
     engine: PG
     version: "13"
   ```

### Option 3: AWS RDS + EC2

1. **Create RDS PostgreSQL Instance**
   - Go to AWS RDS Console
   - Create PostgreSQL database
   - Note the endpoint and credentials

2. **Configure EC2 Instance**
   ```bash
   # On your EC2 instance
   sudo apt-get update
   sudo apt-get install python3-pip postgresql-client
   pip3 install -r requirements.txt
   
   # Set environment variables
   export DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/leetqode_db
   export SECRET_KEY=your-production-secret-key
   export DEBUG=False
   ```

3. **Run Application**
   ```bash
   python manage.py migrate
   python manage.py seed_problems
   gunicorn leetqode.wsgi:application --bind 0.0.0.0:8000
   ```

### Option 4: Docker

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   
   services:
     db:
       image: postgres:13
       environment:
         POSTGRES_DB: leetqode_db
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: password
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"
   
     web:
       build: .
       command: gunicorn leetqode.wsgi:application --bind 0.0.0.0:8000
       volumes:
         - .:/app
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://postgres:password@db:5432/leetqode_db
         - SECRET_KEY=your-production-secret-key
         - DEBUG=False
       depends_on:
         - db
   
   volumes:
     postgres_data:
   ```

2. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["gunicorn", "leetqode.wsgi:application", "--bind", "0.0.0.0:8000"]
   ```

3. **Run with Docker**
   ```bash
   docker-compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py seed_problems
   ```

## 🔧 Database Management

### Backup Database
```bash
# Local
pg_dump leetqode_db > backup.sql

# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# AWS RDS
aws rds create-db-snapshot --db-instance-identifier your-instance --db-snapshot-identifier backup-$(date +%Y%m%d)
```

### Restore Database
```bash
# Local
psql leetqode_db < backup.sql

# Heroku
heroku pg:backups:restore backup-url DATABASE_URL
```

### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check migration status
python manage.py showmigrations
```

## 🔒 Security Best Practices

1. **Environment Variables**
   - Never commit `.env` files
   - Use strong, unique secret keys
   - Rotate credentials regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Restrict database access by IP
   - Regular backups

3. **Production Settings**
   ```python
   # settings.py additions for production
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   SECURE_SSL_REDIRECT = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if PostgreSQL is running
   brew services list | grep postgresql
   sudo systemctl status postgresql
   ```

2. **Permission Denied**
   ```bash
   # Fix PostgreSQL permissions
   sudo -u postgres psql
   GRANT ALL PRIVILEGES ON DATABASE leetqode_db TO your_user;
   ```

3. **Migration Errors**
   ```bash
   # Reset migrations (development only!)
   python manage.py migrate --fake-initial
   ```

4. **Port Already in Use**
   ```bash
   # Kill process on port 5432
   lsof -ti:5432 | xargs kill -9
   ```

## 📊 Performance Optimization

1. **Database Indexing**
   ```python
   # Add indexes to frequently queried fields
   class Problem(models.Model):
       title = models.CharField(max_length=200, db_index=True)
       difficulty = models.CharField(max_length=20, db_index=True)
   ```

2. **Connection Pooling**
   ```python
   # Add to settings.py
   DATABASES['default']['CONN_MAX_AGE'] = 600
   ```

3. **Query Optimization**
   ```python
   # Use select_related and prefetch_related
   problems = Problem.objects.select_related('user').prefetch_related('tags')
   ```

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `DEBUG` | Debug mode | `True` or `False` |
| `GOOGLE_OAUTH2_CLIENT_ID` | Google OAuth client ID | `your-client-id` |
| `GOOGLE_OAUTH2_CLIENT_SECRET` | Google OAuth client secret | `your-client-secret` |
| `ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |

---

For more help, check the [Django Database Documentation](https://docs.djangoproject.com/en/4.2/ref/databases/) or [PostgreSQL Documentation](https://www.postgresql.org/docs/).

