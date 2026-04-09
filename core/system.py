#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Системные операции: управление окнами, процессами, файлами
Кроссплатформенные функции без внешних зависимостей
"""

import sys
import os
import subprocess
import platform
import time

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')

class SystemOps:
    """Класс для системных операций"""
    
    @staticmethod
    def get_platform_info():
        """Получить информацию о платформе"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
    
    @staticmethod
    def run_command(command, shell=True, capture=True):
        """Выполнить системную команду"""
        try:
            if capture:
                result = subprocess.run(
                    command,
                    shell=shell,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return True, result.stdout if result.returncode == 0 else result.stderr
            else:
                result = subprocess.run(command, shell=shell)
                return result.returncode == 0, ""
        except subprocess.TimeoutExpired:
            return False, "Таймаут команды"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    @staticmethod
    def minimize_all_windows():
        """Свернуть все окна"""
        if IS_WINDOWS:
            # Win+D эмуляция через PowerShell
            cmd = '''
            $shell = New-Object -ComObject Shell.Application
            $shell.MinimizeAll()
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            # Для Linux используем wmctrl если есть
            return SystemOps.run_command('wmctrl -k on', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def restore_all_windows():
        """Развернуть все окна"""
        if IS_WINDOWS:
            cmd = '''
            $shell = New-Object -ComObject Shell.Application
            $shell.UndoMinimizeAll()
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command('wmctrl -k off', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def get_active_window():
        """Получить активное окно"""
        if IS_WINDOWS:
            cmd = '''
            Add-Type @"
            using System;
            using System.Runtime.InteropServices;
            using System.Text;
            public class Window {
                [DllImport("user32.dll")]
                public static extern IntPtr GetForegroundWindow();
                [DllImport("user32.dll")]
                public static extern int GetWindowText(IntPtr hWnd, StringBuilder text, int count);
            }
"@
            $handle = [Window]::GetForegroundWindow()
            $title = New-Object System.Text.StringBuilder 256
            [Window]::GetWindowText($handle, $title, 256)
            $title.ToString()
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command('xdotool getactivewindow getwindowname')
        return False, "Не поддерживается"
    
    @staticmethod
    def open_program(program_name):
        """Запустить программу"""
        try:
            if IS_WINDOWS:
                subprocess.Popen(['start', program_name], shell=True)
            elif IS_LINUX:
                subprocess.Popen([program_name], shell=False)
            return True, f"Запущено: {program_name}"
        except Exception as e:
            return False, f"Ошибка запуска: {str(e)}"
    
    @staticmethod
    def kill_process(process_name):
        """Убить процесс по имени"""
        if IS_WINDOWS:
            return SystemOps.run_command(f'taskkill /F /IM {process_name}', capture=False)
        elif IS_LINUX:
            return SystemOps.run_command(f'pkill -9 {process_name}', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def list_processes():
        """Список процессов"""
        if IS_WINDOWS:
            return SystemOps.run_command('tasklist')
        elif IS_LINUX:
            return SystemOps.run_command('ps aux')
        return False, "Не поддерживается"
    
    @staticmethod
    def set_volume(level):
        """Установить громкость (0-100)"""
        if IS_WINDOWS:
            # Используем nircmd если есть, иначе PowerShell
            cmd = f'''
            $obj = New-Object -ComObject WScript.Shell
            1..50 | ForEach-Object {{ $obj.SendKeys([char]174) }}
            1..{level//2} | ForEach-Object {{ $obj.SendKeys([char]175) }}
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command(f'amixer set Master {level}%')
        return False, "Не поддерживается"
    
    @staticmethod
    def screenshot(filename='screenshot.png'):
        """Сделать скриншот"""
        if IS_WINDOWS:
            cmd = f'''
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
            $bitmap.Save("{filename}")
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command(f'import -window root {filename}', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def lock_screen():
        """Заблокировать экран"""
        if IS_WINDOWS:
            return SystemOps.run_command('rundll32.exe user32.dll,LockWorkStation', capture=False)
        elif IS_LINUX:
            # Пробуем разные методы блокировки
            for cmd in ['gnome-screensaver-command -l', 'xdg-screensaver lock', 'loginctl lock-session']:
                success, _ = SystemOps.run_command(cmd, capture=False)
                if success:
                    return True, "Экран заблокирован"
            return False, "Не удалось заблокировать"
        return False, "Не поддерживается"
    
    @staticmethod
    def eject_cd():
        """Открыть CD привод"""
        if IS_WINDOWS:
            cmd = '''
            $sh = New-Object -ComObject "WMPlayer.OCX.7"
            $colCDROMs = $sh.cdromCollection
            if ($colCDROMs.Count -ge 1) {
                For($i = 0; $i -lt $colCDROMs.Count; $i++){
                    $colCDROMs.Item($i).Eject()
                }
            }
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command('eject', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def speak_text(text):
        """Озвучить текст"""
        if IS_WINDOWS:
            cmd = f'''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.Speak("{text}")
            '''
            return SystemOps.run_command(['powershell', '-Command', cmd], shell=False)
        elif IS_LINUX:
            return SystemOps.run_command(f'espeak "{text}"', capture=False)
        return False, "Не поддерживается"
    
    @staticmethod
    def create_file(filepath, content=""):
        """Создать файл"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Файл создан: {filepath}"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    @staticmethod
    def download_file(url, destination):
        """Скачать файл (без внешних библиотек)"""
        try:
            if IS_WINDOWS:
                cmd = f'powershell -Command "Invoke-WebRequest -Uri \'{url}\' -OutFile \'{destination}\'"'
            else:
                cmd = f'wget -O "{destination}" "{url}"'
            
            return SystemOps.run_command(cmd, capture=False)
        except Exception as e:
            return False, f"Ошибка: {str(e)}"


if __name__ == "__main__":
    # Тест
    ops = SystemOps()
    info = ops.get_platform_info()
    print("Информация о системе:")
    for key, value in info.items():
        print(f"  {key}: {value}")
