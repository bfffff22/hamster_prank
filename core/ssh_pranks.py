#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH пранки - выполнение пранков на удаленной машине
"""

import sys
import os
import time
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ssh_client import SSHClient, parse_ssh_string

class SSHPranks:
    """Класс для выполнения пранков через SSH"""
    
    def __init__(self, client):
        self.client = client
    
    def upload_and_run_script(self, script_content, script_name="prank.py"):
        """
        Загрузить скрипт на удаленку и запустить
        
        Args:
            script_content: Содержимое Python скрипта
            script_name: Имя файла
        """
        # Определяем ОС удаленной машины
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
        
        # Создаем временный файл локально
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script_content)
            local_path = f.name
        
        try:
            # Загружаем на удаленку - путь зависит от ОС
            if remote_os == "windows":
                remote_path = f"~/.{script_name}"
            else:
                remote_path = f"/tmp/{script_name}"
            
            print(f"Загружаю скрипт на удаленку...")
            success, msg = self.client.upload_file(local_path, remote_path)
            
            if not success:
                print(f"✗ Ошибка загрузки: {msg}")
                return False
            
            print("✓ Скрипт загружен")
            
            # Делаем исполняемым и запускаем
            print("Запускаю на удаленке...")
            
            if remote_os == "windows":
                # Windows: используем Task Scheduler для запуска в активной сессии
                task_name = f"HamsterPrank_{int(time.time())}"
                cmd = f'schtasks /create /tn "{task_name}" /tr "python \\"{remote_path}\\"" /sc once /st 00:00 /f && schtasks /run /tn "{task_name}" && timeout /t 2 /nobreak >nul && schtasks /delete /tn "{task_name}" /f'
                success, output = self.client.execute_command(cmd)
                if success or not output:
                    print("✓ Пранк запущен на Windows!")
                    return True
                else:
                    print(f"✗ Ошибка: {output}")
                    return False
            else:
                # Linux: используем setsid для отвязки
                self.client.execute_command(f"chmod +x {remote_path}")
                
                # Запускаем в активном терминале через DISPLAY
                # Для GUI пранков нужен DISPLAY, для консольных - терминал
                print("Открываю терминал на удаленке и запускаю пранк...")
                
                # Пробуем разные способы запуска терминала
                terminal_commands = [
                    f"setsid DISPLAY=:0 gnome-terminal -- bash -c 'python3 {remote_path}; read -p \"Нажми Enter\"' </dev/null >/dev/null 2>&1 &",
                    f"setsid DISPLAY=:0 xterm -e 'python3 {remote_path}; read -p \"Нажми Enter\"' </dev/null >/dev/null 2>&1 &",
                    f"setsid DISPLAY=:0 konsole -e bash -c 'python3 {remote_path}; read -p \"Нажми Enter\"' </dev/null >/dev/null 2>&1 &",
                    f"setsid DISPLAY=:0 xfce4-terminal -e 'bash -c \"python3 {remote_path}; read -p \\\"Нажми Enter\\\"\"' </dev/null >/dev/null 2>&1 &"
                ]
                
                success = False
                for cmd in terminal_commands:
                    result, output = self.client.execute_command(cmd)
                    if result or "command not found" not in output.lower():
                        success = True
                        break
                
                if success:
                    print("✓ Пранк запущен в терминале на удаленной машине!")
                    print("  (Должен открыться терминал на экране Kali)")
                    return True
                else:
                    print("✗ Не удалось открыть терминал")
                    print("  Попробую запустить напрямую...")
                    # Fallback - запускаем напрямую
                    success, output = self.client.execute_command(f"python3 {remote_path}")
                    print(f"Вывод: {output}")
                    return success
        
        finally:
            # Удаляем локальный временный файл
            try:
                os.unlink(local_path)
            except:
                pass
    
    def screen_flood(self, duration=10):
        """Заливка экрана на удаленке"""
        script = f'''#!/usr/bin/env python3
import random
import time
import sys

chars = '█▓▒░!@#$%%^&*()0123456789'
start = time.time()

while time.time() - start < {duration}:
    line = ''.join(random.choices(chars, k=100))
    print(line)
    time.sleep(0.01)
'''
        return self.upload_and_run_script(script, "flood.py")
    
    def matrix_effect(self, duration=15):
        """Матрица на удаленке"""
        script = f'''#!/usr/bin/env python3
import random
import time
import sys

chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
start = time.time()

while time.time() - start < {duration}:
    line = ''.join(random.choices(chars, k=80))
    print(line)
    time.sleep(0.1)
'''
        return self.upload_and_run_script(script, "matrix.py")
    
    def fullscreen_text(self, text, duration=5):
        """Полноэкранный текст на удаленке"""
        # Экранируем текст для безопасной передачи
        text_escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        
        script = f'''#!/usr/bin/env python3
import time
import os

text = "{text_escaped}"

# Очищаем экран
os.system('clear')

# Выводим текст по центру
print('\\n' * 10)
print(text.center(80))
print('\\n' * 10)

time.sleep({duration})
'''
        return self.upload_and_run_script(script, "text.py")
    
    def fullscreen_gui_text(self, text, duration=5):
        """Полноэкранное GUI окно с текстом на удаленке"""
        text_escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        
        # Для Linux используем zenity или xmessage
        script = f'''#!/usr/bin/env python3
import subprocess
import time

text = "{text_escaped}"

try:
    # Пробуем zenity
    proc = subprocess.Popen(['zenity', '--info', '--text', text, '--width', '800', '--height', '600'])
    time.sleep({duration})
    proc.terminate()
except:
    try:
        # Пробуем xmessage
        proc = subprocess.Popen(['xmessage', '-center', text])
        time.sleep({duration})
        proc.terminate()
    except:
        # Fallback - терминал на весь экран
        subprocess.run(['gnome-terminal', '--full-screen', '--', 'bash', '-c', f'echo "{{text}}"; sleep {duration}'])
'''
        return self.upload_and_run_script(script, "gui_text.py")
    
    def spam_programs(self, program, count=5):
        """Спам программами на удаленке"""
        script = f'''#!/usr/bin/env python3
import subprocess
import time

program = '{program}'
count = {count}

for i in range(count):
    subprocess.Popen([program])
    time.sleep(0.3)
'''
        return self.upload_and_run_script(script, "spam.py")
    
    def minimize_windows(self):
        """Свернуть все окна на удаленке"""
        cmd = "wmctrl -k on 2>/dev/null || xdotool key super+d 2>/dev/null || echo 'Не удалось свернуть окна'"
        success, output = self.client.execute_command(cmd)
        print(output)
        return success
    
    def window_dance(self, cycles=5):
        """Танец окон на удаленке"""
        script = f'''#!/usr/bin/env python3
import subprocess
import time

cycles = {cycles}

for i in range(cycles):
    # Сворачиваем
    subprocess.run(['wmctrl', '-k', 'on'], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
    
    # Разворачиваем
    subprocess.run(['wmctrl', '-k', 'off'], stderr=subprocess.DEVNULL)
    time.sleep(0.5)
'''
        return self.upload_and_run_script(script, "dance.py")
    
    def glitch_effect(self, duration=10):
        """Глитч эффект на удаленке"""
        script = f'''#!/usr/bin/env python3
import random
import time
import sys

glitch_chars = '█▓▒░▀▄▌▐│─┼╬═║╔╗╚╝'
start = time.time()

while time.time() - start < {duration}:
    for _ in range(random.randint(5, 20)):
        glitch = ''.join(random.choices(glitch_chars, k=random.randint(10, 50)))
        print(glitch)
    
    time.sleep(random.uniform(0.01, 0.1))
    
    if random.random() < 0.1:
        print('\\033[2J\\033[H')  # Очистка экрана
'''
        return self.upload_and_run_script(script, "glitch.py")
    
    def execute_command(self, cmd):
        """Выполнить произвольную команду"""
        return self.client.execute_command(cmd)


if __name__ == "__main__":
    # Тест
    print("SSH Pranks Module")
