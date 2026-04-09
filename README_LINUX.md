# HAMSTER PRANK - Установка на Linux

## 🐧 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/bfffff22/hamster_prank.git
cd hamster_prank
```

### 2. Установка
```bash
chmod +x install_linux.sh
./install_linux.sh
```

### 3. Запуск
```bash
chmod +x start.sh
./start.sh
```

## 📋 Требования

### Обязательно:
- **Python 3.7+**
- **pip3**
- **pexpect** (устанавливается автоматически)

### Для GUI пранков (опционально):
- **python3-tk** (tkinter)

## 🔧 Установка зависимостей вручную

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
pip3 install pexpect
```

### Fedora:
```bash
sudo dnf install python3 python3-pip python3-tkinter
pip3 install pexpect
```

### Arch Linux:
```bash
sudo pacman -S python python-pip tk
pip3 install pexpect
```

### Kali Linux:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk
pip3 install pexpect
```

## 🎯 Возможности на Linux

### Локальные пранки:
1. ✅ Пранки в консоли (матрица, глитч, тряска)
2. ✅ Полноэкранные GUI пранки (требует tkinter)
3. ✅ Текстовые эффекты (волна, радуга)
4. ✅ Управление окнами (требует wmctrl/xdotool)
5. ✅ Skull и Anime ASCII-арт

### SSH пранки:
- ✅ Все локальные пранки работают через SSH
- ✅ Полноэкранные GUI окна на удаленной машине
- ✅ Управление окнами удаленки

## 🛠️ Дополнительные инструменты

### Для управления окнами:
```bash
# Ubuntu/Debian
sudo apt install wmctrl xdotool

# Fedora
sudo dnf install wmctrl xdotool

# Arch
sudo pacman -S wmctrl xdotool
```

## 🚀 Использование

### Локально:
```bash
./start.sh
→ 1 (Локальные операции)
→ Выбери категорию
→ Выбери пранк
```

### SSH:
```bash
./start.sh
→ 2 (SSH пранки)
→ 1 (Подключиться)
→ Ввести SSH данные
→ Выбери категорию
→ Выбери пранк
```

## 📁 Структура

```
hamster_prank/
├── main.py              # Главный файл
├── start.sh             # Запуск (Linux)
├── install_linux.sh     # Установщик (Linux)
├── requirements.txt     # Зависимости
├── config.json          # Настройки (создается автоматически)
├── skull.txt           # ASCII череп
├── anime.txt           # ASCII аниме
├── hom.txt             # ASCII хомяк
├── core/               # Ядро
│   ├── ssh_pranks_files.py
│   ├── fullscreen.py
│   └── display.py
├── pranks/             # Пранки
│   ├── screen_flood.py
│   ├── fullscreen_pranks.py
│   ├── text_bomb.py
│   └── window_chaos.py
└── tools/              # Утилиты
```

## 🐛 Решение проблем

### Python не найден:
```bash
# Проверь версию
python3 --version

# Если нет, установи
sudo apt install python3
```

### pip не найден:
```bash
sudo apt install python3-pip
```

### tkinter не работает:
```bash
sudo apt install python3-tk
```

### Пранки не запускаются:
```bash
# Проверь права
chmod +x start.sh install_linux.sh

# Проверь зависимости
pip3 list | grep pexpect
```

### GUI пранки не работают:
```bash
# Проверь DISPLAY
echo $DISPLAY

# Должно быть :0 или :1
export DISPLAY=:0
```

## 🔒 Безопасность

⚠️ **ВАЖНО**: Используй только на своих системах или с разрешения владельца!

## 📞 Поддержка

Если что-то не работает:
1. Проверь что Python 3.7+ установлен
2. Запусти `./install_linux.sh` еще раз
3. Проверь что все зависимости установлены
4. Для GUI пранков нужен tkinter

## 🎉 Готово!

```bash
./start.sh
```

Хомяк готов к пранкам на Linux! 🐹
