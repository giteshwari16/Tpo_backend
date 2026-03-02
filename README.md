# TPO Backend - Django REST API

## Overview
This is the Django backend for the TPO (Training and Placement Office) Portal system. It provides RESTful APIs for job management, student applications, training events, resume analysis, and wellness tracking.

## Features
- JWT Authentication
- Job Management & Applications
- Training Event Registration
- Resume Analysis with Scoring
- Wellness Tracking with ML Integration
- File Upload Support
- Admin Management Interface

## Vercel Deployment Requirements

### 1. Dependencies
The backend is configured for Vercel deployment with the following requirements:

```bash
# Core Django dependencies
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
PyJWT==2.8.0
python-decouple==3.8
gunicorn==21.2.0
```

### 2. Vercel Configuration Files

#### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "manage.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend_project/wsgi.py"
    }
  ],
  "env": {
    "DJANGO_SETTINGS_MODULE": "backend_project.settings"
  }
}
```

#### requirements.txt
```txt
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
PyJWT==2.8.0
python-decouple==3.8
gunicorn==21.2.0
```

### 3. Environment Variables for Vercel
Set these in your Vercel dashboard:

```bash
# Database (use PostgreSQL for production)
DATABASE_URL=postgresql://username:password@host:port/dbname

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-vercel-app-url.vercel.app

# CORS Settings
FRONTEND_URL=https://your-frontend-url.vercel.app
```

### 4. Production Settings
The backend is configured with production-ready settings:

- **Database**: PostgreSQL (recommended for production)
- **Static Files**: Served via Django (or configure CDN)
- **Security**: HTTPS enforced, secure headers
- **Performance**: Gunicorn WSGI server
- **Logging**: Production error logging

## Local Development

### Setup
```bash
# Clone and setup
git clone <repository-url>
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Environment Variables (Local)
Create `.env` file:
```bash
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
FRONTEND_URL=http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/register/` - User registration
- `GET /api/user/` - Current user info

### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create job (admin only)
- `GET /api/jobs/{id}/` - Get job details

### Applications
- `GET /api/applications/` - User's applications
- `POST /api/applications/` - Apply for job
- `PUT /api/applications/{id}/` - Update application

### Trainings
- `GET /api/trainings/` - List trainings
- `POST /api/trainings/` - Register for training
- `GET /api/my-trainings/` - User's training registrations

### Resume Analysis
- `GET /api/resume-analysis/` - User's analyses
- `POST /api/resume-analysis/` - Upload and analyze resume
- `DELETE /api/resume-analysis/{id}/` - Delete analysis

### Wellness
- `POST /api/fatigue/` - Analyze wellness data
- `GET /api/fatigue-data/` - Get wellness history

## Database Models

### Core Models
- **User**: Custom user model with email authentication
- **StudentProfile**: Extended student information
- **JobProfile**: Job postings and details
- **JobApplication**: Student job applications
- **Training**: Training events and workshops
- **TrainingRegistration**: Student training registrations
- **ResumeAnalysis**: Resume analysis results
- **PrepMaterial**: Study materials and resources
- **FatigueData**: Wellness tracking data

## Admin Interface

Access the Django admin at `/admin/` with superuser credentials:
- Manage all models
- Create/edit jobs and trainings
- Review applications and analyses
- User management

## Security Features

- JWT token authentication
- CORS protection
- File upload validation
- SQL injection prevention
- XSS protection
- CSRF protection

## Performance Optimizations

- Database query optimization
- Select_related/prefetch_related usage
- Efficient file handling
- API response caching (ready to implement)

## Monitoring & Logging

- Production error logging
- API request tracking
- Database query monitoring
- File upload monitoring

## Deployment Checklist for Vercel

1. **Environment Variables**: Set all required env vars
2. **Database**: Configure PostgreSQL connection
3. **Static Files**: Ensure proper static file serving
4. **Domain**: Configure custom domain if needed
5. **SSL**: HTTPS automatically provided by Vercel
6. **Monitoring**: Set up error tracking (optional)

## Support

For deployment issues:
1. Check Vercel logs
2. Verify environment variables
3. Test API endpoints
4. Check database connectivity
