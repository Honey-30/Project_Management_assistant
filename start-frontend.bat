@echo off
echo Starting Frontend Application...
echo.

cd frontend

echo Installing dependencies...
call npm install

echo Starting React development server...
echo Frontend will start on http://localhost:3000
echo.

call npm start