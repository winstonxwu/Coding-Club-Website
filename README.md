# Coding-Club-Website

A modern, full-stack web application for managing coding club activities, meetings, and member attendance. Built with Django REST API backend and React frontend.

## Features

- **User Management**: Teacher and student account types with role-based access
- **Meeting Management**: Create, schedule, and track coding club meetings
- **Attendance Tracking**: Record and monitor student attendance at meetings
- **AI-Powered Summaries**: Automatic meeting summaries using AI
- **Responsive Design**: Modern UI that works on all devices
- **JWT Authentication**: Secure user authentication and authorization
- **Real-time Updates**: Dynamic content updates without page refresh

## Architecture

- **Backend**: Django 4.2+ with Django REST Framework
- **Frontend**: React with modern JavaScript
- **Database**: SQLite (easily configurable for production)
- **Authentication**: JWT tokens with refresh capability
- **API**: RESTful API with CORS support
- **Deployment**: Ready for production deployment

## Tech Stack

### Backend
- Django 4.2+
- Django REST Framework 3.14+
- Django CORS Headers
- JWT Authentication
- SQLite Database

### Frontend
- React
- Axios for API calls
- Modern CSS with responsive design

### Development Tools
- Python 3.9+
- Node.js and npm
- Virtual environment support

## Prerequisites

Before running this project, make sure you have:

- Python 3.9 or higher
- Node.js 14+ and npm
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/coding-club-website.git
cd coding-club-website
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd coding_club_backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd coding_club_frontend

# Install dependencies
npm install

# Start the development server
npm start
```

### 4. Access the Application

- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- Admin Panel: http://localhost:8000/admin

## Configuration

### Environment Variables

Create a `.env` file in the `coding_club_backend` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration

The project uses SQLite by default. For production, update the database settings in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## API Documentation

### Authentication Endpoints

- `POST /api/token/` - Get JWT access token
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### Member Endpoints

- `GET /api/members/` - List all members
- `POST /api/members/` - Create new member
- `GET /api/members/{id}/` - Get member details
- `PUT /api/members/{id}/` - Update member
- `DELETE /api/members/{id}/` - Delete member

### Meeting Endpoints

- `GET /api/meetings/` - List all meetings
- `POST /api/meetings/` - Create new meeting
- `GET /api/meetings/{id}/` - Get meeting details
- `PUT /api/meetings/{id}/` - Update meeting
- `DELETE /api/meetings/{id}/` - Delete meeting

### Attendance Endpoints

- `GET /api/attendance/` - List attendance records
- `POST /api/attendance/` - Record attendance
- `PUT /api/attendance/{id}/` - Update attendance

## 🗄️ Database Models

### Member
- Email (unique identifier)
- Account type (teacher/student)
- Personal information (name, grade)
- Authentication details

### Meeting
- Title and description
- Date and location
- AI-generated summary
- Creator information

### Attendance
- Meeting and student references
- Present/absent status
- Recording details

## Deployment

### Production Checklist

1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure CORS for production domains
5. Set secure `SECRET_KEY`
6. Use HTTPS in production

### Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use meaningful commit messages
- Add tests for new features
- Update documentation as needed

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Django community for the excellent framework
- React team for the powerful frontend library
- All contributors and users of this project

## Support

If you have any questions or need help:

- Open an issue on GitHub
- Contact the dev team
- Check the documentation
