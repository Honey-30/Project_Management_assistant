"""Database initialization and seed data script."""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import models
import auth
from database import engine, SessionLocal

def create_tables():
    """Create all database tables."""
    models.Base.metadata.create_all(bind=engine)

def create_demo_user(db: Session):
    """Create demo user with admin@demo.com credentials."""
    # Check if demo user already exists
    existing_user = db.query(models.User).filter(models.User.email == "admin@demo.com").first()
    if existing_user:
        print("Demo user already exists")
        return existing_user
    
    # Create demo admin user
    demo_user = models.User(
        email="admin@demo.com",
        username="admin",
        full_name="Demo Administrator",
        hashed_password=auth.get_password_hash("password"),
        role=models.UserRole.ADMIN,
        is_active=True,
        bio="Demo administrator account for testing"
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    print("Demo user created: admin@demo.com / password")
    return demo_user

def create_sample_data(db: Session, user: models.User):
    """Create sample projects, tasks, and other data."""
    # Create sample project
    sample_project = models.Project(
        name="Website Redesign Project",
        description="Complete redesign of company website with modern UI/UX",
        status=models.ProjectStatus.ACTIVE,
        start_date=datetime.now(),
        deadline=datetime.now() + timedelta(days=90),
        budget=50000.0,
        spent_budget=12500.0,
        progress=25,
        owner_id=user.id
    )
    db.add(sample_project)
    db.commit()
    db.refresh(sample_project)
    
    # Create sample tasks
    tasks = [
        {
            "title": "Design wireframes",
            "description": "Create wireframes for all main pages",
            "status": models.TaskStatus.COMPLETED,
            "priority": models.TaskPriority.HIGH,
            "progress": 100,
            "estimated_hours": 40.0,
            "actual_hours": 35.0,
            "due_date": datetime.now() - timedelta(days=10)
        },
        {
            "title": "Develop homepage",
            "description": "Implement responsive homepage design",
            "status": models.TaskStatus.IN_PROGRESS,
            "priority": models.TaskPriority.HIGH,
            "progress": 60,
            "estimated_hours": 60.0,
            "actual_hours": 30.0,
            "due_date": datetime.now() + timedelta(days=7)
        },
        {
            "title": "Content migration",
            "description": "Migrate existing content to new structure",
            "status": models.TaskStatus.TODO,
            "priority": models.TaskPriority.MEDIUM,
            "progress": 0,
            "estimated_hours": 80.0,
            "actual_hours": 0.0,
            "due_date": datetime.now() + timedelta(days=30)
        },
        {
            "title": "Testing and QA",
            "description": "Comprehensive testing across all devices and browsers",
            "status": models.TaskStatus.TODO,
            "priority": models.TaskPriority.CRITICAL,
            "progress": 0,
            "estimated_hours": 50.0,
            "actual_hours": 0.0,
            "due_date": datetime.now() + timedelta(days=60)
        }
    ]
    
    for task_data in tasks:
        task = models.Task(
            project_id=sample_project.id,
            assignee_id=user.id,
            **task_data
        )
        db.add(task)
    
    # Create sample team
    team = models.Team(
        name="Web Development Team",
        description="Frontend and backend developers for website project",
        project_id=sample_project.id
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    
    # Add user to team
    team_member = models.TeamMember(
        team_id=team.id,
        user_id=user.id,
        role=models.UserRole.ADMIN
    )
    db.add(team_member)
    
    # Create sample notifications
    notifications = [
        {
            "title": "Welcome to Project Management Assistant",
            "message": "Your account has been set up successfully. Start by creating your first project!",
            "notification_type": "welcome",
            "status": models.NotificationStatus.UNREAD
        },
        {
            "title": "Task deadline approaching",
            "message": "The task 'Develop homepage' is due in 7 days",
            "notification_type": "deadline_warning",
            "status": models.NotificationStatus.UNREAD,
            "related_type": "task",
            "related_id": 2
        }
    ]
    
    for notif_data in notifications:
        notification = models.Notification(
            user_id=user.id,
            **notif_data
        )
        db.add(notification)
    
    # Create sample risk
    risk = models.Risk(
        title="Scope Creep Risk",
        description="Risk of project scope expanding beyond original requirements",
        level=models.RiskLevel.MEDIUM,
        probability=0.6,
        impact=0.7,
        mitigation_strategy="Regular stakeholder meetings and change request process",
        status="identified",
        project_id=sample_project.id,
        identified_by=user.id
    )
    db.add(risk)
    
    # Create sample AI interaction
    ai_interaction = models.AIInteraction(
        user_id=user.id,
        project_id=sample_project.id,
        message="What's the current status of my website project?",
        response="Your website redesign project is currently 25% complete and on track. The design wireframes have been completed, and the homepage development is 60% done. You have 2 pending tasks scheduled for completion in the next 30 days.",
        context={"project_analysis": True, "status_requested": True}
    )
    db.add(ai_interaction)
    
    db.commit()
    print("Sample data created successfully")

def init_database():
    """Initialize database with tables and demo data."""
    print("Initializing database...")
    
    # Create tables
    create_tables()
    print("Database tables created")
    
    # Create session
    db = SessionLocal()
    try:
        # Create demo user
        demo_user = create_demo_user(db)
        
        # Create sample data
        create_sample_data(db, demo_user)
        
        print("Database initialization completed successfully")
        print("Demo credentials: admin@demo.com / password")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()