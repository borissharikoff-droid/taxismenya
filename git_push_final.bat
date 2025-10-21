@echo off
chcp 65001 >nul
cd /d "C:\Users\fillo\OneDrive\Рабочий стол\del\taxismenya"
echo Текущая директория:
cd
echo.
echo Статус git:
git status
echo.
echo Добавляем файлы:
git add .
echo.
echo Коммитим изменения:
git commit -m "Обновлен бот: убраны фото, добавлен сельский стиль, больше мата, звуковые эффекты"
echo.
echo Пушим в репозиторий:
git push
echo.
echo Готово!
pause
