@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH: FASTER VOICE + NEW SCHEDULE
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\tazi\taxismenya"
echo Текущая директория:
cd
echo.

echo Добавляем файлы:
git add bot.py requirements.txt
echo.

echo Коммитим:
git commit -m "Ускорен голос на 30%% + новое расписание: 3 голосовых, 2 текстовых, 1 реплай в день"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    ИЗМЕНЕНИЯ ОТПРАВЛЕНЫ!
echo    - Голос теперь на 30%% быстрее
echo    - 6 сообщений в день (было 4)
echo    - Уникальные изображения
echo ========================================
pause

