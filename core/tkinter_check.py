#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для проверки наличия tkinter и предоставления альтернатив
"""

import sys
import subprocess

class TkinterChecker:
    """Проверка наличия tkinter локально и удаленно"""
    
    def __init__(self):
        self.local_available = None
        self.remote_available = {}
    
    def check_local(self):
        """Проверить наличие tkinter локально"""
        if self.local_available is not None:
            return self.local_available
        
        try:
            import tkinter
            self.local_available = True
            return True
        except ImportError:
            self.local_available = False
            return False
    
    def check_remote(self, ssh_client, host_key):
        """Проверить наличие tkinter на удаленной машине"""
        if host_key in self.remote_available:
            return self.remote_available[host_key]
        
        # Проверяем через SSH
        check_cmd = 'python3 -c "import tkinter; print(\'OK\')" 2>/dev/null && echo "TKINTER_OK" || echo "TKINTER_MISSING"'
        success, output = ssh_client.execute_command(check_cmd)
        
        has_tkinter = "TKINTER_OK" in output
        self.remote_available[host_key] = has_tkinter
        return has_tkinter
    
    def get_install_instructions(self, platform='linux'):
        """Получить инструкции по установке tkinter"""
        if platform == 'linux':
            return """
Для установки tkinter на Linux выполните:

Ubuntu/Debian:
  sudo apt-get update
  sudo apt-get install python3-tk

Fedora/RHEL:
  sudo dnf install python3-tkinter

Arch Linux:
  sudo pacman -S tk

После установки перезапустите программу.
"""
        elif platform == 'windows':
            return """
На Windows tkinter обычно идет в комплекте с Python.
Если его нет, переустановите Python с официального сайта:
  https://www.python.org/downloads/

При установке убедитесь, что выбрана опция "tcl/tk and IDLE".
"""
        else:
            return "Установите tkinter для вашей системы."
    
    def prompt_user_choice(self, has_tkinter):
        """Предложить пользователю выбор режима работы"""
        if has_tkinter:
            print("\n✓ tkinter обнаружен!")
            print("\nВыберите режим работы:")
            print("1. С GUI (полноэкранные окна, графические эффекты)")
            print("2. Только консоль (текстовые эффекты в терминале)")
            print()
            choice = input("Ваш выбор (1/2, по умолчанию 1): ").strip()
            return choice != '2'
        else:
            print("\n✗ tkinter не обнаружен!")
            print("\nДоступны только консольные пранки (текстовые эффекты).")
            print("Для полноэкранных GUI пранков установите tkinter.")
            print(self.get_install_instructions('linux' if sys.platform.startswith('linux') else 'windows'))
            print("\nПродолжить в консольном режиме?")
            choice = input("(y/n, по умолчанию y): ").strip().lower()
            return False if choice == 'n' else True
    
    def filter_menu_options(self, has_tkinter, menu_type='local'):
        """Фильтровать опции меню в зависимости от наличия tkinter"""
        if has_tkinter:
            return None  # Все опции доступны
        
        # Опции, требующие tkinter
        gui_options = {
            'local': [2, 4],  # Полноэкранные пранки, Управление окнами
            'ssh': [2]  # Полноэкранные пранки
        }
        
        return gui_options.get(menu_type, [])
    
    def show_unavailable_message(self):
        """Показать сообщение о недоступности функции"""
        print("\n✗ Эта функция требует tkinter!")
        print("Установите tkinter для использования GUI пранков.")
        print(self.get_install_instructions('linux' if sys.platform.startswith('linux') else 'windows'))

# Глобальный экземпляр
checker = TkinterChecker()
