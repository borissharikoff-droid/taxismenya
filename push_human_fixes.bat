@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH HUMAN FIXES UPDATE
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\del\taxismenya"
echo Текущая директория:
cd
echo.

echo Добавляем все файлы:
git add .
echo.

echo Коммитим изменения:
git commit -m "Исправлены повторы в подарках, добавлены человеческие выражения, усилены звуковые эффекты"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    PUSH ЗАВЕРШЕН!
echo ========================================
pause
