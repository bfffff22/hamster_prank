#!/bin/bash
# HAMSTER PRANK - Linux Installer

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║         HAMSTER PRANK - Установка для Linux               ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Проверка Python
echo "[1/4] Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден!"
    echo ""
    echo "Установка Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi
echo "✓ Python3 найден: $(python3 --version)"

# Проверка pip
echo ""
echo "[2/4] Проверка pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден!"
    echo "Установка pip..."
    python3 -m ensurepip --default-pip
fi
echo "✓ pip готов"

# Установка зависимостей
echo ""
echo "[3/4] Установка зависимостей..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt --user --quiet
    echo "✓ Зависимости установлены"
else
    echo "⚠️  requirements.txt не найден, устанавливаю базовые пакеты..."
    pip3 install pexpect --user --quiet
    echo "✓ Базовые пакеты установлены"
fi

# Проверка структуры
echo ""
echo "[4/4] Проверка структуры проекта..."
mkdir -p pranks core tools payloads
echo "✓ Структура готова"

# Проверка GUI зависимостей
echo ""
echo "[Опционально] Проверка GUI зависимостей..."
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "⚠️  tkinter не найден (нужен для GUI пранков)"
    echo "Установка:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
else
    echo "✓ tkinter установлен"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                  ✓ Установка завершена!                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "Запуск: ./start.sh"
echo ""
