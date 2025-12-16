@echo off
echo Installiere/Update PyInstaller...
py -m pip install pyinstaller

echo Erstelle AetherLink.exe...
py -m PyInstaller --noconsole --onefile --uac-admin --clean --icon=assets\app_icon.ico --add-data "assets;assets" --name=AetherLink aetherlink.pyw

echo Verschiebe EXE in den Hauptordner...
move /Y "dist\AetherLink.exe" "..\AetherLink.exe"

echo Bereinige temporaere Dateien...
del /q *.spec
rmdir /s /q build
rmdir /s /q dist

echo.
echo FERTIG! Die exe liegt nun im Ordner drueber.
