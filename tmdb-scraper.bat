@echo off

set DIR=%~dp0

cd /d %DIR%

python3 tmdb-scraper.py

pause
