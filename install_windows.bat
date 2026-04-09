@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════════════════════════╗
echo ║         HAMSTER PRANK - Установка для Windows             ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Проверка Python
echo [1/4] Проверка Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo.
    echo Установи Python с https://www.python.org/downloads/
    echo Не забудь поставить галочку "Add Python to PATH"!
    pause
    exit /b 1
)
echo ✓ Python найден

REM Проверка pip
echo.
echo [2/4] Проверка pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip не найден!
    echo Устанавливаю pip...
    python -m ensurepip --default-pip
)
echo ✓ pip готов

REM Установка зависимостей
echo.
echo [3/4] Установка зависимостей...
if exist requirements.txt (
    python -m pip install -r requirements.txt --quiet
    echo ✓ Зависимости установлены
) else (
    echo ⚠️  requirements.txt не найден, устанавливаю базовые пакеты...
    python -m pip install pexpect pywin32 --quiet
    echo ✓ Базовые пакеты установлены
)

REM Проверка структуры
echo.
echo [4/4] Проверка структуры проекта...
if not exist "pranks" mkdir pranks
if not exist "core" mkdir core
if not exist "tools" mkdir tools
if not exist "payloads" mkdir payloads
echo ✓ Структура готова

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║                  ✓ Установка завершена!                  ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo Запуск: start.bat
echo.
pause
