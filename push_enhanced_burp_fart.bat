@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH ENHANCED BURP & FART SOUNDS
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
git commit -m "УЛУЧШЕНЫ звуки рыгания и пердежа: более реалистичные, приоритет рыганию, 100% шанс добавления"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    PUSH ЗАВЕРШЕН!
echo ========================================
pause
