@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH GTTS UPDATE
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\tazi\taxismenya"
echo Текущая директория:
cd
echo.

echo Добавляем requirements.txt:
git add requirements.txt
echo.

echo Коммитим:
git commit -m "Add gtts for voice messages fallback"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    GTTS ДОБАВЛЕН!
echo ========================================
pause

