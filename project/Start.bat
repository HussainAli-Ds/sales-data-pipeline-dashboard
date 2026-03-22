@echo off
cd /d C:\project

start cmd /k python src\main.py
start cmd /k python -m streamlit run dashboard/app.py

pause