@echo off
cd /d "%~dp0"
git config user.email "developer@recipeapp.com"
git config user.name "Recipe Developer"
git add -A
git commit -m "Update: All changes - UI fixes, backend API integration, cloudscraper, ready for deployment"
git push origin main
echo.
echo Push complete!
pause
