# LeetQode Setup Guide

## 🎉 Current Status
✅ **Backend**: Running on http://localhost:8000  
✅ **Frontend**: Running on http://localhost:3000  
✅ **Database**: 100 LeetCode problems seeded  
✅ **API**: Working (test endpoints available)  

## 🔧 Next Steps: Configure Google OAuth2

### 1. Get Google OAuth2 Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. Create OAuth2 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Application type: "Web application"
   - Authorized redirect URIs:
     ```
     http://localhost:8000/auth/google/login/callback/
     http://127.0.0.1:8000/auth/google/login/callback/
     ```

### 2. Configure Django with Your Credentials

Run this command with your Google OAuth2 credentials:

```bash
cd backend
source venv/bin/activate
python manage.py setup_google_oauth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

### 3. Test the Application

1. **Open the app**: http://localhost:3000
2. **Click "Sign in with Google"**
3. **Complete Google OAuth2 flow**
4. **Start using LeetQode!**

## 🧪 Test Endpoints (No Auth Required)

- **Health Check**: http://localhost:8000/api/health/
- **Sample Problems**: http://localhost:8000/api/public/problems/
- **Admin Panel**: http://localhost:8000/admin/ (username: admin)

## 🚀 Features Available After Login

- **Dashboard**: View problems due today
- **Problem Browser**: Search and filter 100 LeetCode problems
- **Confidence Tracking**: Track your progress on each problem
- **Spaced Repetition**: Intelligent scheduling based on performance
- **Statistics**: View your practice statistics

## 🛠️ Development Commands

### Backend
```bash
cd backend
source venv/bin/activate
python manage.py runserver          # Start Django server
python manage.py migrate            # Run migrations
python manage.py seed_problems      # Seed problems
python manage.py createsuperuser    # Create admin user
```

### Frontend
```bash
cd frontend
npm run dev                         # Start Vite dev server
npm run build                       # Build for production
npm run lint                        # Run linter
```

## 🔍 Troubleshooting

### Google OAuth2 Issues
- Make sure redirect URI matches exactly: `http://localhost:8000/auth/google/login/callback/`
- Check that Google+ API is enabled in Google Cloud Console
- Verify client ID and secret are correct

### Port Issues
```bash
# Kill processes on ports
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Database Issues
```bash
cd backend
source venv/bin/activate
python manage.py migrate
python manage.py seed_problems
```

## 📱 Access Points

- **Main App**: http://localhost:3000
- **API Health**: http://localhost:8000/api/health/
- **Admin Panel**: http://localhost:8000/admin/
- **Google Login**: http://localhost:8000/auth/google/login/

## 🎯 What's Working Right Now

✅ Django REST API with 100 LeetCode problems  
✅ React frontend with modern UI  
✅ Google OAuth2 authentication (needs credentials)  
✅ Spaced repetition algorithm  
✅ Confidence tracking system  
✅ Responsive design with TailwindCSS  
✅ Problem filtering and search  
✅ Dashboard with statistics  

The app is fully functional - you just need to add your Google OAuth2 credentials to enable user authentication!
