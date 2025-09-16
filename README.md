# LeetQode - LeetCode Practice Tracker

A production-ready Django + React application for tracking LeetCode practice with confidence-based spaced repetition and intelligent problem queues.

## Features

- **Google OAuth2 Authentication** - Secure login with Google accounts
- **Confidence Tracking** - Track your confidence level for each problem (0-100%)
- **Spaced Repetition** - Intelligent scheduling based on your performance
- **Problem Management** - Add problems to your practice queue
- **Dashboard** - View problems due today and your progress statistics
- **Filtering & Search** - Find problems by difficulty, tags, and more
- **Responsive Design** - Beautiful UI that works on all devices

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Django Allauth** - Google OAuth2 authentication
- **PostgreSQL/SQLite** - Database
- **CORS Headers** - Cross-origin resource sharing

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Zustand** - State management
- **Axios** - HTTP client
- **React Router** - Client-side routing
- **Lucide React** - Icon library

## Project Structure

```
leetqode/
├── backend/                 # Django backend
│   ├── leetqode/           # Main Django project
│   ├── accounts/           # User authentication app
│   ├── problems/           # Problems and user progress app
│   ├── requirements.txt    # Python dependencies
│   └── manage.py          # Django management script
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/         # Page components
│   │   ├── store/         # Zustand stores
│   │   └── App.jsx        # Main App component
│   ├── package.json       # Node.js dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google OAuth2 credentials

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed the database with problems:**
   ```bash
   python manage.py seed_problems
   ```

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your settings
   ```

4. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:3000`

## Google OAuth2 Setup

1. **Go to Google Cloud Console:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Google+ API:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it

3. **Create OAuth2 credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Set application type to "Web application"
   - Add authorized redirect URIs:
     - `http://localhost:8000/auth/google/callback/`
     - `http://127.0.0.1:8000/auth/google/callback/`

4. **Update environment variables:**
   - Copy the Client ID and Client Secret
   - Add them to your `.env` files in both backend and frontend

## API Endpoints

### Authentication
- `GET /api/auth/profile/` - Get user profile
- `GET /api/auth/status/` - Check authentication status
- `POST /auth/google/` - Google OAuth2 login

### Problems
- `GET /api/problems/` - List all problems (with filtering)
- `GET /api/user/problems/` - List user's problems
- `POST /api/user/problems/` - Add problem to user's list
- `PATCH /api/user/problems/{id}/update/` - Update problem progress
- `GET /api/dashboard/` - Get problems due today
- `GET /api/stats/` - Get user statistics

## Usage

1. **Sign in** with your Google account
2. **Browse problems** on the Problems page
3. **Add problems** to your practice queue
4. **Track your progress** with confidence levels
5. **Review due problems** on the Dashboard
6. **Mark problems as solved or struggling** to update your schedule

## Spaced Repetition Algorithm

The app uses a spaced repetition algorithm to schedule problem reviews:

- **Successful attempts** increase confidence and extend the review interval
- **Failed attempts** decrease confidence and shorten the review interval
- **Confidence levels** range from 0-100%
- **Review intervals** start at 1 day and can extend up to 30 days

## Development

### Backend Development

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run development server
python manage.py runserver
```

### Frontend Development

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Deployment

### Backend Deployment

1. Set `DEBUG=False` in production
2. Use PostgreSQL for production database
3. Set up proper environment variables
4. Use a production WSGI server like Gunicorn
5. Set up static file serving with WhiteNoise or CDN

### Frontend Deployment

1. Build the production bundle: `npm run build`
2. Serve the `dist` folder with a web server
3. Configure API base URL for production
4. Set up proper CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
