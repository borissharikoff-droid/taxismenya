@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🚀 Запуск Git Push из: %CD%
echo.

git add .
echo ✅ Файлы добавлены

git commit -m "Оптимизация бота v2.0: -74%% кода, +33%% голосовых, контент смешнее"
echo ✅ Коммит создан

git push --set-upstream origin master
if %errorlevel% equ 0 (
    echo ✅ Изменения запушены!
    echo.
    echo 🎉 Готово! Бот задеплоится на Railway автоматически.
) else (
    echo ❌ Ошибка при push
    git push
)

echo.
pause

