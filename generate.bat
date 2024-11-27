@echo off
echo Building the application...
pyinstaller --onefile --windowed --add-data "TUKE.jpg;." --clean main.py 
echo Build complete. Check the "dist" folder for the .exe file.
pause