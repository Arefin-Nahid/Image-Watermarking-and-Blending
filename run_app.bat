@echo off
echo Image Processing Application
echo ============================
echo.

echo Installing dependencies...
pip install opencv-python numpy Pillow

echo.
echo Running the application...
python main.py

pause
