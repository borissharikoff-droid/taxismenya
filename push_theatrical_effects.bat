@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH THEATRICAL EFFECTS UPDATE
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
git commit -m "Добавлены театральные эффекты и тестовая отправка 5 голосовых сообщений"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    PUSH ЗАВЕРШЕН!
echo ========================================
pause
