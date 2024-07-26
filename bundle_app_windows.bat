@echo off
echo Building the application with PyInstaller...
pyinstaller --onefile --windowed --add-data "./docs/index.html;./docs/" --add-data "./docs/images/*;./docs/images/" app.py
echo Build complete!
