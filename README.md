# Project Management Assistant

An AI-powered project management system with comprehensive database integration, real-time features, and intelligent insights.

## Features

### ✅ Implemented Core Features
- **Database Integration**: Complete SQLAlchemy models for Users, Projects, Tasks, Teams, AI Interactions, Reports, Notifications, and Risks
- **Authentication System**: JWT-based authentication with secure login/logout
- **RESTful API**: FastAPI backend with full CRUD operations
- **React Frontend**: Modern, responsive React application with Tailwind CSS
- **Real-time Dashboard**: Live project metrics and analytics
- **Project Management**: Create, update, and track projects with progress monitoring
- **Demo Data**: Pre-loaded sample data with demo credentials

### 🚧 Advanced Features (In Development)
- **AI Assistant**: Intelligent project insights and recommendations
- **Real-time Updates**: WebSocket integration for live collaboration
- **Advanced Task Management**: Drag-and-drop, dependencies, and automated assignments
- **Risk Analysis**: Predictive risk assessment and mitigation strategies
- **Report Generation**: Automated reports with analytics and insights
- **Team Collaboration**: Advanced team management and permissions

## Quick Start

### Option 1: Quick Start (Recommended)
```bash
# Run the automated setup script
quick-start.bat
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Start backend server
start-backend.bat

# Or manually:
cd backend
pip install -r requirements.txt
python -c "from init_db import init_database; init_database()"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
# Start frontend application
start-frontend.bat

# Or manually:
cd frontend
npm install
npm start
```

## Demo Credentials

Access the application with these demo credentials:
- **Email**: `admin@demo.com`
- **Username**: `admin`
- **Password**: `password`

## Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with SQLite (development) / PostgreSQL (production)
- **JWT Authentication**: Secure token-based authentication
- **Pydantic**: Data validation and serialization
- **Alembic**: Database migrations

### Frontend Stack
- **React 18**: Modern React with hooks
- **React Router**: Client-side routing
- **React Query**: Data fetching and state management
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication

### Database Schema
- **Users**: Authentication, profiles, roles, permissions
- **Projects**: Metadata, status, deadlines, budget tracking
- **Tasks**: Assignments, dependencies, priorities, status updates
- **Teams**: Members, permissions, collaboration settings
- **AI Interactions**: Chat history, recommendations, context
- **Reports**: Generated content, analytics, insights
- **Notifications**: Alerts, messages, read status
- **Risks**: Analysis data, predictions, mitigation strategies

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /register` - Register new user
- `GET /users/me` - Get current user info

### Projects
- `GET /projects` - List all projects
- `POST /projects` - Create new project
- `GET /projects/{id}` - Get project by ID
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Tasks
- `GET /tasks` - List all tasks
- `POST /tasks` - Create new task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Documentation
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## Development

### Project Structure
```
Project_Management_assistant/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication utilities
│   ├── database.py         # Database configuration
│   ├── init_db.py          # Database initialization
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   └── App.js          # Main app component
│   ├── public/             # Static assets
│   └── package.json        # Node.js dependencies
├── quick-start.bat         # One-click startup script
├── start-backend.bat       # Backend startup script
├── start-frontend.bat      # Frontend startup script
└── README.md               # This file
```

### Environment Configuration

Create `.env` file in the backend directory:
```env
DATABASE_URL=sqlite:///./project_management.db
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your-openai-api-key-here
```

### Database Management

Initialize database with demo data:
```bash
cd backend
python -c "from init_db import init_database; init_database()"
```

### Testing

Run backend tests:
```bash
cd backend
python -m pytest
```

Run frontend tests:
```bash
cd frontend
npm test
```

## Deployment

### Production Database
For production, update the `DATABASE_URL` in your environment:
```env
DATABASE_URL=postgresql://user:password@localhost/project_management
```

### Docker Support (Coming Soon)
```bash
docker-compose up
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the sample data and demo credentials

---

**Happy Project Managing! 🚀**