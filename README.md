# Task Assignment System

A Django-based full-stack application for managing and assigning tasks to users.

## Features
- Single login page for all users.
- Role-based experience: Admin (Staff) vs. Normal User.
- Admin: Full CRUD on tasks, assign tasks to users.
- User: View only assigned tasks, update task status.
- Railway-ready configuration with SQLite, WhiteNoise, and Gunicorn.

## Local Setup

1. **Clone the repository** (or navigate to the project directory).
2. **Install dependencies**:
   ```bash
   pip install django gunicorn whitenoise python-dotenv
   ```
3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```
4. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```
5. **Run the server**:
   ```bash
   python manage.py runserver
   ```

## Admin Instructions
- Log in and go to "Manage All Tasks".
- Click "Assign New Task".
- Choose a user and set task details.
- The "assigned_by" field is automatically set to the logged-in admin.

## User Experience
- Log in to see "My Assigned Tasks".
- Click "Update Status" to change the status of a task.
- Users cannot see tasks assigned to others or access admin URLs.

## Railway Deployment
1. Connect your repo to Railway.
2. Set Environment Variables:
   - `SECRET_KEY`: (Your Django secret key)
   - `DEBUG`: `False` (for production)
   - `ALLOWED_HOSTS`: `.railway.app`
3. Add a **Volume** mounted at `/data`.
4. Set `SQLITE_PATH`: `/data/db.sqlite3`.
5. Railway will use the `Procfile` to migrate, collect static, and run the server.
