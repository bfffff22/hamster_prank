#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH пранки - УПРОЩЕННАЯ ВЕРСИЯ
Выполнение пранков напрямую в терминале на удаленной машине
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ssh_client import SSHClient

class SSHPranksSimple:
    """Упрощенный класс для SSH пранков - запуск в видимом терминале"""
    
    def __init__(self, client):
        self.client = client
    
    def run_in_terminal(self, command, title="Hamster Prank"):
        """
        Запустить команду в новом терминале на удаленке
        Терминал будет виден на экране!
        """
        # Команды для открытия терминала с командой
        terminal_cmds = [
            f"DISPLAY=:0 qterminal -e bash -c '{command}; echo; echo \"Нажми Enter для закрытия\"; read' &",
            f"DISPLAY=:0 gnome-terminal --title='{title}' -- bash -c '{command}; echo; echo \"Нажми Enter для закрытия\"; read' &",
            f"DISPLAY=:0 xterm -T '{title}' -e bash -c '{command}; echo; echo \"Нажми Enter для закрытия\"; read' &",
            f"DISPLAY=:0 konsole --title '{title}' -e bash -c '{command}; echo; echo \"Нажми Enter для закрытия\"; read' &",
            f"DISPLAY=:0 xfce4-terminal --title='{title}' -e 'bash -c \"{command}; echo; echo Нажми Enter; read\"' &"
        ]
        
        print(f"Открываю терминал на удаленке...")
        
        for cmd in terminal_cmds:
            success, output = self.client.execute_command(cmd)
            if success or "not found" not in output.lower():
                print(f"✓ Терминал открыт на удаленной машине!")
                print(f"  Команда: {command[:50]}...")
                return True
        
        print("✗ Не удалось открыть терминал")
        return False
    
    def screen_flood(self, duration=10):
        """Заливка экрана"""
        cmd = f"python3 -c \"import random,time; start=time.time()\\nwhile time.time()-start<{duration}:\\n  print(''.join(random.choices('#@%&*+=',k=100)))\\n  time.sleep(0.05)\""
        return self.run_in_terminal(cmd, "ЗАЛИВКА ЭКРАНА")
    
    def matrix_effect(self, duration=15):
        """Матрица"""
        cmd = f"python3 -c \"import random,time; start=time.time()\\nwhile time.time()-start<{duration}:\\n  print(''.join(random.choices('01',k=80)))\\n  time.sleep(0.1)\""
        return self.run_in_terminal(cmd, "МАТРИЦА")
    
    def fullscreen_text(self, text, duration=5):
        """Полноэкранный текст"""
        text_escaped = text.replace("'", "'\\''").replace('"', '\\\\"')
        cmd = f"clear; python3 -c \"import time\\nprint('\\\\n'*10)\\nprint('{text_escaped}'.center(80))\\nprint('\\\\n'*10)\\ntime.sleep({duration})\""
        return self.run_in_terminal(cmd, "ПРАНК")
    
    def glitch_effect(self, duration=10):
        """Глитч"""
        cmd = f"python3 -c \"import random,time,os; start=time.time()\\nwhile time.time()-start<{duration}:\\n  if random.random()<0.1: os.system('clear')\\n  for _ in range(random.randint(5,20)): print(''.join(random.choices('#@%&*',k=random.randint(10,50))))\\n  time.sleep(random.uniform(0.01,0.1))\""
        return self.run_in_terminal(cmd, "ГЛИТЧ")
    
    def spam_programs(self, program, count=5):
        """Спам программами"""
        cmd = f"for i in {{1..{count}}}; do DISPLAY=:0 {program} & sleep 0.3; done"
        success, output = self.client.execute_command(cmd)
        if success:
            print(f"✓ Запущено {count} экземпляров {program}")
            return True
        else:
            print(f"✗ Ошибка: {output}")
            return False
    
    def minimize_windows(self):
        """Свернуть все окна"""
        cmd = "DISPLAY=:0 wmctrl -k on 2>/dev/null || DISPLAY=:0 xdotool key super+d 2>/dev/null"
        success, output = self.client.execute_command(cmd)
        if success:
            print("✓ Окна свернуты")
        else:
            print(f"Результат: {output}")
        return success
    
    def show_gui_message(self, text, duration=5):
        """Показать GUI сообщение"""
        text_escaped = text.replace("'", "'\\''")
        
        # Пробуем zenity
        cmd = f"DISPLAY=:0 timeout {duration} zenity --info --text='{text_escaped}' --width=800 --height=600 2>/dev/null"
        success, output = self.client.execute_command(cmd)
        
        if "not found" in output.lower():
            # Пробуем xmessage
            cmd = f"DISPLAY=:0 timeout {duration} xmessage -center '{text_escaped}' 2>/dev/null"
            success, output = self.client.execute_command(cmd)
        
        if success or "not found" not in output.lower():
            print("✓ GUI сообщение показано")
            return True
        else:
            print("✗ Не удалось показать GUI (установи zenity или xmessage)")
            return False


if __name__ == "__main__":
    print("SSH Pranks Simple Module")
