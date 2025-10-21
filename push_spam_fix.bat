@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH SPAM FIX - ИСПРАВЛЕНИЕ СПАМА
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\del\taxismenya"
echo Текущая директория:
cd
echo.

echo Добавляем все файлы:
git add .
echo.

echo Коммитим исправления:
git commit -m "ИСПРАВЛЕН СПАМ: убрана тестовая отправка, уменьшено расписание до 4 сообщений в день, исправлены ошибки Event loop"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    СПАМ ИСПРАВЛЕН!
echo ========================================
pause
