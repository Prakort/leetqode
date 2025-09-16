#!/usr/bin/env python3
"""
PostgreSQL Setup Script for LeetQode

This script helps you set up PostgreSQL for local development and production.
"""

import os
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with PostgreSQL configuration."""
    env_content = """# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database Configuration
# For SQLite (current):
# DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL (uncomment and configure):
DATABASE_URL=postgresql://postgres:password@localhost:5432/leetqode_db

# Google OAuth2 Settings
GOOGLE_OAUTH2_CLIENT_ID=283307083033-qh48bj9liq495l3ge5s843s4uhm7q07j.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret

# CORS Settings
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
"""
    
    env_path = Path('.env')
    if env_path.exists():
        print("⚠️  .env file already exists. Backing up to .env.backup")
        env_path.rename('.env.backup')
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with PostgreSQL configuration")

def check_postgresql_installation():
    """Check if PostgreSQL is installed."""
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL is installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ PostgreSQL is not installed")
            return False
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed")
        return False

def create_database():
    """Create PostgreSQL database."""
    db_name = "leetqode_db"
    db_user = "postgres"
    
    print(f"Creating database '{db_name}'...")
    
    # Create database
    create_db_cmd = [
        'psql', '-U', db_user, '-h', 'localhost',
        '-c', f'CREATE DATABASE {db_name};'
    ]
    
    try:
        result = subprocess.run(create_db_cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Database '{db_name}' created successfully")
        else:
            if "already exists" in result.stderr:
                print(f"ℹ️  Database '{db_name}' already exists")
            else:
                print(f"❌ Error creating database: {result.stderr}")
                return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def run_migrations():
    """Run Django migrations."""
    print("Running Django migrations...")
    
    try:
        # Make migrations
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        print("✅ Made migrations")
        
        # Apply migrations
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Applied migrations")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration error: {e}")
        return False

def seed_database():
    """Seed the database with initial data."""
    print("Seeding database with problems...")
    
    try:
        subprocess.run([sys.executable, 'manage.py', 'seed_problems'], check=True)
        print("✅ Database seeded with problems")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Seeding error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 LeetQode PostgreSQL Setup")
    print("=" * 40)
    
    # Check PostgreSQL installation
    if not check_postgresql_installation():
        print("\n📋 To install PostgreSQL:")
        print("   macOS: brew install postgresql")
        print("   Ubuntu: sudo apt-get install postgresql postgresql-contrib")
        print("   Windows: Download from https://www.postgresql.org/download/")
        return
    
    # Create .env file
    create_env_file()
    
    # Create database
    if not create_database():
        print("\n❌ Failed to create database. Please check PostgreSQL is running.")
        print("   Start PostgreSQL: brew services start postgresql (macOS)")
        return
    
    # Run migrations
    if not run_migrations():
        print("\n❌ Failed to run migrations")
        return
    
    # Seed database
    if not seed_database():
        print("\n❌ Failed to seed database")
        return
    
    print("\n🎉 PostgreSQL setup complete!")
    print("\n📋 Next steps:")
    print("   1. Update .env file with your PostgreSQL credentials")
    print("   2. Run: python manage.py runserver")
    print("   3. Visit: http://localhost:8000")

if __name__ == "__main__":
    main()
