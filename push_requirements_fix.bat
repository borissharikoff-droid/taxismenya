@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH REQUIREMENTS FIX
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\del\taxismenya"
echo Текущая директория:
cd
echo.

echo Добавляем все файлы:
git add .
echo.

echo Коммитим исправления requirements:
git commit -m "ИСПРАВЛЕНЫ requirements.txt: обновлен numpy для совместимости с Python 3.12, добавлены гибкие версии пакетов"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    REQUIREMENTS ИСПРАВЛЕНЫ!
echo ========================================
pause
