@echo off
echo Starting Project Management Assistant...
echo.

echo [1/3] Installing backend dependencies...
cd backend
python -m pip install -r requirements.txt
echo Backend dependencies installed.
echo.

echo [2/3] Initializing database...
python -c "from init_db import init_database; init_database()"
echo Database initialized.
echo.

echo [3/3] Starting backend server...
echo Backend server will start on http://localhost:8000
echo API documentation available at http://localhost:8000/docs
echo.
start cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Starting frontend...
cd ..\frontend
start cmd /k "npm install && npm start"

echo.
echo ===================================
echo Project Management Assistant Started!
echo ===================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Demo credentials:
echo Username: admin
echo Password: password
echo.
echo Press any key to exit...
pause > nul