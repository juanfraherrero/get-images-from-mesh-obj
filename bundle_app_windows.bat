@echo off
echo Building the application with PyInstaller...
pyinstaller --onefile --windowed --add-data "docs/*;docs/" app.py
echo Build complete!