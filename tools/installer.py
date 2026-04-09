#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Установщик программ
Автоматическая установка PortProton и других программ
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.system import SystemOps

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')

def check_internet():
    """Проверка интернет соединения"""
    try:
        if IS_WINDOWS:
            result = subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                                  capture_output=True, 
                                  timeout=5)
        else:
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], 
                                  capture_output=True, 
                                  timeout=5)
        return result.returncode == 0
    except:
        return False


def install_portproton():
    """Установка PortProton (только для Linux)"""
    if not IS_LINUX:
        print("✗ PortProton доступен только для Linux!")
        return False
    
    print("=== УСТАНОВКА PORTPROTON ===\n")
    
    # Проверка интернета
    print("Проверка интернет соединения...")
    if not check_internet():
        print("✗ Нет интернет соединения!")
        return False
    print("✓ Интернет доступен\n")
    
    # Определяем домашнюю директорию
    home = Path.home()
    install_dir = home / "PortProton"
    
    print(f"Директория установки: {install_dir}")
    
    # Создаем директорию если нужно
    if not install_dir.exists():
        print("Создаю директорию...")
        install_dir.mkdir(parents=True, exist_ok=True)
    
    # Скачиваем установщик
    print("\nСкачиваю PortProton...")
    url = "https://github.com/Castro-Fidel/PortProton_ALT/releases/latest/download/PortProton"
    
    script_path = install_dir / "PortProton"
    
    success, msg = SystemOps.download_file(url, str(script_path))
    
    if not success:
        print(f"✗ Ошибка скачивания: {msg}")
        return False
    
    print("✓ Скачано!")
    
    # Делаем исполняемым
    print("\nУстанавливаю права...")
    os.chmod(script_path, 0o755)
    print("✓ Права установлены!")
    
    # Запускаем установку
    print("\nЗапускаю установку PortProton...")
    print("(Это может занять несколько минут)\n")
    
    try:
        result = subprocess.run([str(script_path)], cwd=str(install_dir))
        
        if result.returncode == 0:
            print("\n✓ PortProton успешно установлен!")
            print(f"Путь: {script_path}")
            return True
        else:
            print("\n✗ Ошибка установки!")
            return False
    
    except Exception as e:
        print(f"\n✗ Ошибка: {str(e)}")
        return False


def install_wine():
    """Установка Wine"""
    if not IS_LINUX:
        print("✗ Wine устанавливается только на Linux!")
        return False
    
    print("=== УСТАНОВКА WINE ===\n")
    
    # Определяем дистрибутив
    try:
        with open('/etc/os-release', 'r') as f:
            os_info = f.read().lower()
    except:
        print("✗ Не удалось определить дистрибутив!")
        return False
    
    # Команды установки для разных дистрибутивов
    if 'ubuntu' in os_info or 'debian' in os_info or 'mint' in os_info:
        print("Обнаружен Debian/Ubuntu")
        cmd = "sudo apt update && sudo apt install -y wine wine64 wine32"
    elif 'arch' in os_info or 'manjaro' in os_info:
        print("Обнаружен Arch/Manjaro")
        cmd = "sudo pacman -S --noconfirm wine wine-mono wine-gecko"
    elif 'fedora' in os_info:
        print("Обнаружен Fedora")
        cmd = "sudo dnf install -y wine"
    elif 'opensuse' in os_info:
        print("Обнаружен openSUSE")
        cmd = "sudo zypper install -y wine"
    else:
        print("✗ Неизвестный дистрибутив!")
        print("Установи Wine вручную")
        return False
    
    print(f"\nКоманда: {cmd}")
    print("Запускаю установку...\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode == 0:
        print("\n✓ Wine успешно установлен!")
        return True
    else:
        print("\n✗ Ошибка установки!")
        return False


def install_steam():
    """Установка Steam"""
    print("=== УСТАНОВКА STEAM ===\n")
    
    if IS_WINDOWS:
        print("Скачиваю Steam для Windows...")
        url = "https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe"
        dest = str(Path.home() / "Downloads" / "SteamSetup.exe")
        
        success, msg = SystemOps.download_file(url, dest)
        
        if success:
            print(f"✓ Скачано: {dest}")
            print("Запускаю установщик...")
            SystemOps.open_program(dest)
            return True
        else:
            print(f"✗ Ошибка: {msg}")
            return False
    
    elif IS_LINUX:
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
        except:
            print("✗ Не удалось определить дистрибутив!")
            return False
        
        if 'ubuntu' in os_info or 'debian' in os_info or 'mint' in os_info:
            cmd = "sudo apt update && sudo apt install -y steam"
        elif 'arch' in os_info or 'manjaro' in os_info:
            cmd = "sudo pacman -S --noconfirm steam"
        elif 'fedora' in os_info:
            cmd = "sudo dnf install -y steam"
        else:
            print("✗ Неизвестный дистрибутив!")
            return False
        
        print(f"Команда: {cmd}")
        print("Запускаю установку...\n")
        
        result = subprocess.run(cmd, shell=True)
        
        if result.returncode == 0:
            print("\n✓ Steam успешно установлен!")
            return True
        else:
            print("\n✗ Ошибка установки!")
            return False


def install_python_package(package_name):
    """Установка Python пакета через pip"""
    print(f"=== УСТАНОВКА {package_name.upper()} ===\n")
    
    print(f"Устанавливаю {package_name}...")
    
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', package_name])
        
        if result.returncode == 0:
            print(f"\n✓ {package_name} успешно установлен!")
            return True
        else:
            print(f"\n✗ Ошибка установки {package_name}!")
            return False
    
    except Exception as e:
        print(f"\n✗ Ошибка: {str(e)}")
        return False


def install_custom_script(url, name):
    """Скачать и установить кастомный скрипт"""
    print(f"=== УСТАНОВКА {name.upper()} ===\n")
    
    home = Path.home()
    scripts_dir = home / ".local" / "bin"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    
    script_path = scripts_dir / name
    
    print(f"Скачиваю {name}...")
    success, msg = SystemOps.download_file(url, str(script_path))
    
    if not success:
        print(f"✗ Ошибка: {msg}")
        return False
    
    print("✓ Скачано!")
    
    # Делаем исполняемым
    os.chmod(script_path, 0o755)
    
    print(f"✓ {name} установлен в {script_path}")
    return True


def interactive_menu():
    """Интерактивное меню установщика"""
    while True:
        os.system('cls' if IS_WINDOWS else 'clear')
        print("=== УСТАНОВЩИК ПРОГРАММ ===\n")
        print(f"Платформа: {platform.system()} {platform.release()}")
        print(f"Интернет: {'✓' if check_internet() else '✗'}\n")
        print("1. Установить PortProton (Linux)")
        print("2. Установить Wine (Linux)")
        print("3. Установить Steam")
        print("4. Установить Python пакет")
        print("5. Установить скрипт по URL")
        print("0. Выход")
        print()
        
        choice = input("Выбери: ").strip()
        
        if choice == '1':
            install_portproton()
            input("\nНажми Enter...")
        elif choice == '2':
            install_wine()
            input("\nНажми Enter...")
        elif choice == '3':
            install_steam()
            input("\nНажми Enter...")
        elif choice == '4':
            package = input("Имя пакета: ").strip()
            if package:
                install_python_package(package)
            input("\nНажми Enter...")
        elif choice == '5':
            url = input("URL скрипта: ").strip()
            name = input("Имя файла: ").strip()
            if url and name:
                install_custom_script(url, name)
            input("\nНажми Enter...")
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")
            input("\nНажми Enter...")


if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано!")
        sys.exit(0)
