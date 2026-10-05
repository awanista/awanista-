@echo off
chcp 65001 >nul
title Sekkeena - مطبخك
cd /d "%~dp0"
echo.
echo   بدء تشغيل موقع سكينة...
echo   (سيفتح المتصفح تلقائيا - سيب النافذة دي مفتوحة وانت بتتصفح)
echo.
start "sekkeena-server" /min cmd /c "python -m http.server 8765"
timeout /t 1 >nul
start "" "http://localhost:8765/index.html"
echo   الموقع فتح - كل حاجة شغالة دلوقتي (الـ 3D والأنيميشن)
echo   لعشان تقفل السيرفر: اقفل النافذة السوداء الصغيرة
echo.
pause
