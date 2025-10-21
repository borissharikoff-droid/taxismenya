@echo off
chcp 65001 >nul
echo ========================================
echo    PUSH TO GITHUB REPOSITORY
echo ========================================
echo.

cd /d "C:\Users\fillo\OneDrive\Рабочий стол\del\taxismenya"
echo Текущая директория:
cd
echo.

echo Проверяем статус git:
git status
echo.

echo Добавляем удаленный репозиторий (если не добавлен):
git remote add origin https://github.com/borissharikoff-droid/taxismenya.git 2>nul || echo "Репозиторий уже добавлен"
echo.

echo Добавляем все файлы:
git add .
echo.

echo Коммитим изменения:
git commit -m "Обновлен бот: убраны фото, добавлен сельский стиль, больше мата, звуковые эффекты"
echo.

echo Пушим в GitHub:
git push -u origin main
echo.

echo ========================================
echo    PUSH ЗАВЕРШЕН!
echo ========================================
pause
