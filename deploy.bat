@echo off
cd /d "C:\Users\Ivan\Desktop\сайт покер"
if errorlevel 1 (
    echo Failed to change directory
    pause
    exit /b 1
)

echo Initializing git repository...
git init

echo Adding files...
git add .

echo Creating commit...
git commit -m "Initial commit: Poker club website"

echo Adding remote origin...
git remote add origin https://github.com/1vanKatkov/golubayaustrica.git

echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo Push failed, trying master branch...
    git push -u origin master
)

echo Done!
pause
