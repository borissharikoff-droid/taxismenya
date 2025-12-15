@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH UNIQUE IMAGES UPDATE
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
git commit -m "Улучшена система подбора изображений: случайные страницы + предотвращение повторов + gtts"
echo.

echo Пушим в GitHub:
git push
echo.

echo ========================================
echo    ИЗМЕНЕНИЯ ОТПРАВЛЕНЫ!
echo ========================================
pause

