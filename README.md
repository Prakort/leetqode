# LeetQode - LeetCode Practice Tracker

Tracking LeetCode practice with confidence-based spaced repetition and company-specific problem filtering.

## Features

- **Google OAuth2 Authentication** - Secure login with Google accounts
- **Confidence Tracking** - Track your confidence level for each problem (0-100%)
- **Spaced Repetition** - Intelligent scheduling based on your performance
- **Company Tag Filtering** - Filter problems by company (Amazon, Google, Microsoft, Meta)
- **Problem Management** - Add problems to your practice queue
- **Dashboard** - View problems due today and your progress statistics
- **Advanced Filtering** - Find problems by difficulty, tags, and company
- **Responsive Design** - Beautiful UI that works on all devices
- **Persistent State** - Filters and progress persist across navigation

## Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Django Allauth** - Google OAuth2 authentication
- **SQLite** - Database (default, no setup required)
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

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Google OAuth2 credentials** (see setup below)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd leetqode
```

### 2. Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp env.example .env
   
   # Edit .env file with your settings
   # You'll need to add your Google OAuth2 credentials here
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
   *Note: This creates a SQLite database file automatically - no additional database setup required!*

6. **Seed the database with 100 LeetCode problems:**
   ```bash
   python manage.py seed_problems
   ```

7. **Start the Django development server:**
   ```bash
   python manage.py runserver
   ```

   The backend API will be available at `http://localhost:8000`

### 3. Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env file with your Google OAuth2 Client ID
   # Add: VITE_GOOGLE_CLIENT_ID=your_google_client_id_here
   ```

4. **Start the React development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

### 4. Access the Application

1. Open your browser and go to `http://localhost:3000`
2. Click "Sign in with Google" to authenticate
3. Start practicing LeetCode problems!

## Google OAuth2 Setup

### Step 1: Create Google Cloud Project

1. **Go to Google Cloud Console:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one

2. **Enable Google Identity Services:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google Identity" and enable it

### Step 2: Create OAuth2 Credentials

1. **Create OAuth2 credentials:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Set application type to "Web application"
   - Add authorized JavaScript origins:
     - `http://localhost:3000`
     - `http://127.0.0.1:3000`
   - Add authorized redirect URIs:
     - `http://localhost:8000/auth/google/callback/`
     - `http://127.0.0.1:8000/auth/google/callback/`

2. **Copy your credentials:**
   - Copy the **Client ID** (you'll need this for both frontend and backend)
   - Copy the **Client Secret** (you'll need this for the backend)

### Step 3: Configure Environment Variables

1. **Backend `.env` file:**
   ```bash
   # In backend/.env
   GOOGLE_OAUTH2_CLIENT_ID=your_client_id_here
   GOOGLE_OAUTH2_CLIENT_SECRET=your_client_secret_here
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   ```

2. **Frontend `.env` file:**
   ```bash
   # In frontend/.env
   VITE_GOOGLE_CLIENT_ID=your_client_id_here
   ```

## API Endpoints

### Authentication
- `GET /api/auth/profile/` - Get user profile
- `GET /api/auth/status/` - Check authentication status
- `POST /api/auth/google/` - Google OAuth2 login
- `POST /api/auth/logout/` - Logout user

### Problems
- `GET /api/problems/` - List all 100 problems
- `GET /api/user/problems/` - List user's practice problems
- `POST /api/user/problems/` - Add problem to practice queue
- `PUT /api/user/problems/{id}/update/` - Update problem progress
- `GET /api/dashboard/` - Get problems due today
- `GET /api/stats/` - Get user statistics

### Health Check
- `GET /api/health/` - API health status

## Usage

1. **Sign in** with your Google account
2. **Browse problems** on the Problems page with company tags
3. **Filter problems** by:
   - Company (Amazon, Google, Microsoft, Meta)
   - Difficulty (Easy, Medium, Hard)
   - Technical tags (Array, Hash Table, etc.)
   - Search by title or problem ID
4. **Add problems** to your practice queue
5. **Track your progress** with confidence levels (0-100%)
6. **Review due problems** on the Dashboard
7. **Mark problems as solved or struggling** to update your schedule
8. **Navigate between pages** - your filters and progress persist!

## Spaced Repetition Algorithm

The app uses a spaced repetition algorithm to schedule problem reviews:

- **Successful attempts** increase confidence and extend the review interval
- **Failed attempts** decrease confidence and shorten the review interval
- **Confidence levels** range from 0-100%
- **Review intervals** start at 1 day and can extend up to 30 days

## Current Data

The application comes pre-loaded with:

- **100 LeetCode problems** from the most commonly asked questions
- **Company tags** for 35 problems:
  - **Amazon**: 25+ problems
  - **Google**: 20+ problems  
  - **Microsoft**: 15+ problems
  - **Meta**: 5+ problems
- **Technical tags** for all problems (Array, Hash Table, String, etc.)
- **Difficulty levels** (Easy, Medium, Hard)

## Troubleshooting

### Common Issues

1. **"Authentication credentials were not provided" error:**
   - Make sure you're logged in with Google
   - Check that both frontend and backend servers are running
   - Verify your Google OAuth2 credentials are correct

2. **Problems list is empty:**
   - Run `python manage.py seed_problems` to populate the database
   - Check that the backend server is running on port 8000

3. **Google Sign-In not working:**
   - Verify your Google OAuth2 Client ID is set in both `.env` files
   - Check that authorized origins include `http://localhost:3000`
   - Make sure Google Identity Services is enabled in Google Cloud Console

4. **Filters not persisting:**
   - This should be fixed in the current version
   - If issues persist, try refreshing the page

### Development

### Backend Development

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed database with problems
python manage.py seed_problems

# Run development server
python manage.py runserver
```

### Frontend Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

### Running Both Servers

To run the complete application, you need both servers running:

1. **Terminal 1 - Backend:**
   ```bash
   cd backend
   source venv/bin/activate
   python manage.py runserver
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the app:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

## Deployment

### Backend Deployment

1. Set `DEBUG=False` in production
2. Use PostgreSQL for production database (optional - SQLite works for small deployments)
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
