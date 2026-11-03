@echo off
title EduAura - Personalized Learning Recommendation System
cd /d "%~dp0"
echo ========================================================
echo Starting EduAura Personalized Learning Recommendation System...
echo ========================================================
echo Opening browser at http://localhost:5000 ...
start http://localhost:5000
".venv\Scripts\python.exe" app.py
pause

