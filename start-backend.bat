@echo off
echo Starting Backend Server...
echo.

cd backend

echo Installing dependencies...
python -m pip install -r requirements.txt

echo Initializing database...
python -c "from init_db import init_database; init_database()"

echo Starting FastAPI server...
echo Server will start on http://localhost:8000
echo API documentation available at http://localhost:8000/docs
echo.
echo Demo credentials:
echo Username: admin  
echo Password: password
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000