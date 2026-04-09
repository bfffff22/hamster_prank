#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hamster Prank - Swiss Army Knife для пранков и удаленного управления
Запуск: python main.py
"""

import os
import sys
import json
import time
from pathlib import Path

# Фикс кодировки для Windows
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# Определяем платформу
IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')

class HamsterPrank:
    def __init__(self):
        self.config_path = Path(__file__).parent / "config.json"
        self.config = self.load_config()
        
    def load_config(self):
        """Загрузка конфига"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"ssh_hosts": [], "last_mode": None}
    
    def save_config(self):
        """Сохранение конфига"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if IS_WINDOWS else 'clear')
    
    def print_banner(self):
        """Вывод баннера"""
        banner = """
========================================
    HAMSTER PRANK - Swiss Knife
        Pranks & Remote Control
========================================
"""
        print(banner)
    
    def main_menu(self):
        """Главное меню"""
        while True:
            self.clear_screen()
            self.print_banner()
            print("1. Локальные операции")
            print("2. SSH пранки")
            print("3. Установка софта")
            print("4. Настройки")
            print("0. Выход")
            print()
            
            choice = input("Выбери опцию: ").strip()
            
            if choice == '1':
                self.local_menu()
            elif choice == '2':
                self.ssh_menu()
            elif choice == '3':
                self.installer_menu()
            elif choice == '4':
                self.settings_menu()
            elif choice == '0':
                print("Пока!")
                break
            else:
                input("Неверный выбор. Нажми Enter...")
    
    def local_menu(self):
        """Меню локальных операций"""
        while True:
            self.clear_screen()
            print("=== ЛОКАЛЬНЫЕ ОПЕРАЦИИ ===\n")
            print("1. Пранки в консоли (матрица, глитч)")
            print("2. Полноэкранные пранки (GUI окна)")
            print("3. Текстовые эффекты")
            print("4. Управление окнами")
            print("5. Запустить программу")
            print("6. Показать Skull (ASCII-арт)")
            print("7. Показать Anime (ASCII-арт)")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                from pranks.screen_flood import interactive_menu
                interactive_menu()
            elif choice == '2':
                from pranks.fullscreen_pranks import interactive_menu
                interactive_menu()
            elif choice == '3':
                from pranks.text_bomb import interactive_menu
                interactive_menu()
            elif choice == '4':
                from pranks.window_chaos import interactive_menu
                interactive_menu()
            elif choice == '5':
                cmd = input("Команда для запуска: ")
                os.system(cmd)
            elif choice == '6':
                self.show_ascii_art('skull.txt')
            elif choice == '7':
                self.show_ascii_art('anime.txt')
            elif choice == '0':
                break
            
            if choice != '0' and choice == '5':
                input("\nНажми Enter для продолжения...")
    
    def ssh_menu(self):
        """Меню SSH операций"""
        while True:
            self.clear_screen()
            print("=== SSH ПРАНКИ ===\n")
            
            # Показываем сохраненные хосты
            if self.config['ssh_hosts']:
                print("Сохраненные хосты:")
                for i, host in enumerate(self.config['ssh_hosts'][-3:], 1):
                    print(f"  {i}. {host['user']}@{host['host']}")
                print()
            
            print("1. Подключиться и выполнить пранк")
            print("2. Залить экран на удаленке")
            print("3. Показать текст на удаленке")
            print("4. Запустить команду на удаленке")
            print("5. Открыть SSH сессию")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                self.ssh_prank_menu()
            elif choice == '2':
                self.ssh_flood()
            elif choice == '3':
                self.ssh_text()
            elif choice == '4':
                self.ssh_command()
            elif choice == '5':
                self.ssh_shell()
            elif choice == '0':
                break
            else:
                print("Неверный выбор!")
                input("\nНажми Enter...")
    
    def ssh_get_connection(self):
        """Получить SSH подключение"""
        from core.ssh_client_expect import SSHClientExpect, parse_ssh_string
        
        print("\n=== SSH ПОДКЛЮЧЕНИЕ ===")
        
        # Показываем сохраненные
        if self.config['ssh_hosts']:
            print("\nСохраненные хосты:")
            for i, host in enumerate(self.config['ssh_hosts'], 1):
                print(f"{i}. {host['user']}@{host['host']}")
            print("0. Ввести новый")
            
            choice = input("\nВыбери хост или 0: ").strip()
            
            if choice.isdigit() and 0 < int(choice) <= len(self.config['ssh_hosts']):
                saved = self.config['ssh_hosts'][int(choice) - 1]
                host_str = f"{saved['user']}@{saved['host']}"
            else:
                host_str = input("Хост (user@ip:port): ").strip()
        else:
            host_str = input("Хост (user@ip:port): ").strip()
        
        if not host_str:
            return None
        
        host, port, user = parse_ssh_string(host_str)
        
        # Сохраняем в конфиг
        if host not in [h.get('host') for h in self.config['ssh_hosts']]:
            self.config['ssh_hosts'].append({
                'host': host,
                'user': user
            })
            self.save_config()
        
        client = SSHClientExpect(host, port, user)
        success, msg = client.connect()
        
        if success:
            print(f"✓ {msg}")
            return client
        else:
            print(f"✗ {msg}")
            input("\nНажми Enter...")
            return None
    
    def ssh_prank_menu(self):
        """Меню пранков через SSH"""
        client = self.ssh_get_connection()
        if not client:
            return
        
        from core.ssh_pranks_files import SSHPranksFiles
        pranks = SSHPranksFiles(client)
        
        while True:
            self.clear_screen()
            print("=== SSH ОПЕРАЦИИ (на удаленной машине) ===\n")
            print("1. Пранки в консоли (матрица, глитч)")
            print("2. Полноэкранные пранки (GUI окна)")
            print("3. Текстовые эффекты")
            print("4. Управление окнами")
            print("5. Запустить программу")
            print("6. Показать Skull (ASCII-арт)")
            print("7. Показать Anime (ASCII-арт)")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                self.ssh_console_pranks(pranks)
            elif choice == '2':
                self.ssh_fullscreen_pranks(pranks)
            elif choice == '3':
                self.ssh_text_effects(pranks)
            elif choice == '4':
                self.ssh_window_control(pranks)
            elif choice == '5':
                cmd = input("Команда для запуска: ")
                if cmd:
                    print("\nВыполняю...")
                    success, output = pranks.client.execute_command(cmd)
                    print("\n--- Результат ---")
                    print(output)
                    input("\nНажми Enter...")
            elif choice == '6':
                self.ssh_show_ascii_art(pranks, 'skull.txt')
            elif choice == '7':
                self.ssh_show_ascii_art(pranks, 'anime.txt')
            elif choice == '0':
                break
    
    def ssh_console_pranks(self, pranks):
        """Подменю консольных пранков через SSH"""
        while True:
            self.clear_screen()
            print("=== ПРАНКИ В КОНСОЛИ (SSH) ===\n")
            print("1. Заливка символами")
            print("2. Матрица")
            print("3. Глитч эффект")
            print("4. Тряска экрана")
            print("5. Кастомная заливка")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                duration = input("Длительность (сек, по умолчанию 10): ").strip()
                duration = int(duration) if duration.isdigit() else 10
                print("\nЗапускаю заливку на удаленке...")
                pranks.screen_flood(duration)
                input("\nНажми Enter...")
            elif choice == '2':
                duration = input("Длительность (сек, по умолчанию 15): ").strip()
                duration = int(duration) if duration.isdigit() else 15
                print("\nЗапускаю матрицу на удаленке...")
                pranks.matrix_effect(duration)
                input("\nНажми Enter...")
            elif choice == '3':
                duration = input("Длительность (сек, по умолчанию 10): ").strip()
                duration = int(duration) if duration.isdigit() else 10
                print("\nЗапускаю глитч на удаленке...")
                pranks.glitch_effect(duration)
                input("\nНажми Enter...")
            elif choice == '4':
                duration = input("Длительность (сек, по умолчанию 5): ").strip()
                duration = int(duration) if duration.isdigit() else 5
                print("\nЗапускаю тряску на удаленке...")
                pranks.screen_shake(duration)
                input("\nНажми Enter...")
            elif choice == '5':
                char = input("Символ для заливки (Enter = случайные): ").strip()
                dur = input("Длительность в секундах (10): ").strip()
                speed = input("Скорость (slow/medium/fast/insane): ").strip()
                
                duration = int(dur) if dur.isdigit() else 10
                char = char if char else None
                speed = speed if speed in ['slow', 'medium', 'fast', 'insane'] else 'fast'
                
                print("\nЗапускаю кастомную заливку на удаленке...")
                pranks.screen_flood(duration, char, speed)
                input("\nНажми Enter...")
            elif choice == '0':
                break
    
    def ssh_fullscreen_pranks(self, pranks):
        """Подменю полноэкранных пранков через SSH"""
        while True:
            self.clear_screen()
            print("=== ПОЛНОЭКРАННЫЕ ПРАНКИ (SSH) ===\n")
            print("1. Полноэкранный текст")
            print("2. Полноэкранная заливка")
            print("3. Китайская атака ⭐")
            print("4. Полноэкранная картинка")
            print("5. Спам окнами")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                text = input("Текст: ").strip()
                if not text:
                    text = "ПРАНК!"
                duration = input("Длительность (сек, по умолчанию 5): ").strip()
                duration = int(duration) if duration.isdigit() else 5
                print("\nЗапускаю полноэкранный текст на удаленке...")
                pranks.fullscreen_text(text, duration)
                input("\nНажми Enter...")
            elif choice == '2':
                duration = input("Длительность (сек, по умолчанию 10): ").strip()
                duration = int(duration) if duration.isdigit() else 10
                print("\nЗапускаю полноэкранную заливку на удаленке...")
                pranks.screen_flood(duration)
                input("\nНажми Enter...")
            elif choice == '3':
                duration = input("Длительность (сек, по умолчанию 15): ").strip()
                duration = int(duration) if duration.isdigit() else 15
                print("\nЗапускаю китайскую атаку на удаленке...")
                pranks.chinese_attack(duration)
                input("\nНажми Enter...")
            elif choice == '4':
                image_url = input("URL картинки: ").strip()
                if not image_url:
                    print("Нужно указать URL картинки")
                    input("\nНажми Enter...")
                    continue
                duration = input("Длительность (сек, по умолчанию 5): ").strip()
                duration = int(duration) if duration.isdigit() else 5
                print("\nЗапускаю отображение картинки на удаленке...")
                # Используем команду для загрузки и показа картинки
                cmd = f'wget "{image_url}" -O /tmp/temp_img && DISPLAY=:0 feh -F /tmp/temp_img &'
                pranks.client.execute_command(cmd)
                time.sleep(duration)
                pranks.client.execute_command('killall feh 2>/dev/null')
                print("✓ Картинка показана!")
                input("\nНажми Enter...")
            elif choice == '5':
                text = input("Текст для окна: ").strip()
                if not text:
                    text = "ПРАНК!"
                count = input("Количество окон (по умолчанию 5): ").strip()
                count = int(count) if count.isdigit() else 5
                duration = input("Длительность (сек, по умолчанию 3): ").strip()
                duration = int(duration) if duration.isdigit() else 3
                print(f"\nЗапускаю {count} окон на удаленке...")
                
                for i in range(count):
                    # Создаем GUI окно с текстом
                    script = f'''#!/usr/bin/env python3
import tkinter as tk
root = tk.Tk()
root.title("Спам окном #{i+1}")
root.attributes('-fullscreen', True)
root.configure(bg='red')

text_widget = tk.Text(root, bg='black', fg='white', font=('Courier', 24), wrap='word')
text_widget.pack(expand=True, fill='both', padx=100, pady=200)
text_widget.insert('1.0', '{text} #{i+1}')
text_widget.config(state='disabled')

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after({duration}000, close)
root.mainloop()
'''
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                        f.write(script)
                        local_path = f.name
                    
                    remote_path = f"~/.spam_window_{i}.py"
                    success, msg = pranks.client.upload_file(local_path, remote_path)
                    
                    if success:
                        pranks.client.execute_command(f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &")
                        time.sleep(0.5)
                        pranks.client.execute_command(f"rm {remote_path}")
                    
                    import os
                    os.unlink(local_path)
                
                print("✓ Окна запущены!")
                input("\nНажми Enter...")
            elif choice == '0':
                break
    
    def ssh_text_effects(self, pranks):
        """Подменю текстовых эффектов через SSH"""
        while True:
            self.clear_screen()
            print("=== ТЕКСТОВЫЕ ЭФФЕКТЫ (SSH) ===\n")
            print("1. Текст в рамке")
            print("2. Заполнить экран текстом")
            print("3. Волна")
            print("4. Печатная машинка")
            print("5. Радужный текст")
            print("6. Приближение")
            print("7. Тряска")
            print("8. Спам")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '0':
                break
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                text = input("Текст: ").strip()
                if not text:
                    text = "ПРАНК!"
                
                print("\nЗапускаю эффект на удаленке...")
                
                # Создаем соответствующий GUI скрипт для каждого типа
                if choice == '1':  # Текст в рамке
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
root.title("Текст в рамке")
root.attributes('-fullscreen', True)
root.configure(bg='red')

font = tkFont.Font(family='Courier', size=14, weight='bold')
text_widget = tk.Text(root, bg='black', fg='white', font=font, relief='solid', bd=2)
text_widget.pack(expand=True, fill='both', padx=50, pady=50)
text_widget.insert('1.0', '{text}')
text_widget.config(state='disabled')

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '2':  # Заполнить экран текстом
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont
import random

root = tk.Tk()
root.title("Заполнение текстом")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

def draw_text():
    canvas.delete('all')
    width, height = root.winfo_width(), root.winfo_height()
    
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        canvas.create_text(x, y, text='{text}', fill='white', font=('Courier', 16))

for _ in range(10):
    root.after(_ * 100, draw_text)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '3':  # Волна
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import math
import time

root = tk.Tk()
root.title("Волна")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

width, height = root.winfo_width(), root.winfo_height()
chars = list('{text}')
char_count = len(chars)

def animate_wave():
    canvas.delete('all')
    center_y = height // 2
    amp = 50
    freq = 0.1
    
    for i, char in enumerate(chars):
        x = (width // char_count) * i + 50
        y = center_y + amp * math.sin(time.time() * 5 + i * freq)
        canvas.create_text(x, y, text=char, fill='cyan', font=('Courier', 20))

root.after(50, lambda: animate_wave())
root.update()

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '4':  # Печатная машинка
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import time

root = tk.Tk()
root.title("Печатная машинка")
root.attributes('-fullscreen', True)
root.configure(bg='black')

text_widget = tk.Text(root, bg='black', fg='green', font=('Courier', 24), wrap='word')
text_widget.pack(expand=True, fill='both', padx=100, pady=200)

def type_text():
    text = '{text}'
    for i in range(len(text) + 1):
        text_widget.delete('1.0', 'end')
        text_widget.insert('1.0', text[:i])
        text_widget.see('end')
        root.update()
        time.sleep(0.1)

type_text()

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '5':  # Радужный текст
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
root.title("Радужный текст")
root.attributes('-fullscreen', True)
root.configure(bg='black')

colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
text = '{text}'
text_length = len(text)

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

for i, char in enumerate(text):
    color = colors[i % len(colors)]
    x = 50 + i * 30
    canvas.create_text(x, height//2, text=char, fill=color, font=('Courier', 24))

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '6':  # Приближение
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import math

root = tk.Tk()
root.title("Приближение")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

def zoom_effect():
    canvas.delete('all')
    width, height = root.winfo_width(), root.winfo_height()
    
    for scale in range(1, 6):
        font_size = 10 * scale
        canvas.after(scale * 200, lambda fs=font_size: canvas.create_text(
            width//2, height//2, text='{text}', fill='yellow', 
            font=('Arial', fs), tags='zoom'))

for scale in range(1, 6):
    root.after(scale * 200, zoom_effect)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '7':  # Тряска
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import random
import time

root = tk.Tk()
root.title("Тряска")
root.attributes('-fullscreen', True)
root.configure(bg='black')

text_widget = tk.Text(root, bg='black', fg='white', font=('Courier', 24), wrap='word')
text_widget.pack(expand=True, fill='both', padx=100, pady=200)
text_widget.insert('1.0', '{text}')
text_widget.tag_add('shake', '1.0', 'end')

def shake():
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    root.geometry(f"+{root.winfo_x() + dx}+{root.winfo_y() + dy}")
    root.after(50, shake)

shake()

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''
                elif choice == '8':  # Спам
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import random

root = tk.Tk()
root.title("Спам")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

for _ in range(20):
    x = random.randint(50, root.winfo_width()-50)
    y = random.randint(50, root.winfo_height()-50)
    canvas.create_text(x, y, text='{text}', fill='white', font=('Courier', random.randint(10, 30)))

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)
root.mainloop()
'''

                # Загружаем и запускаем скрипт на удаленке
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                    f.write(script)
                    local_path = f.name
                
                remote_path = f"~/.text_effect_{choice}.py"
                print(f"Загружаю Эффект {choice} на удаленку...")
                success, msg = pranks.client.upload_file(local_path, remote_path)
                
                if success:
                    print("Запускаю эффект на удаленке...")
                    pranks.client.execute_command(f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &")
                    time.sleep(1)
                    pranks.client.execute_command(f"rm {remote_path}")
                    print("✓ Эффект запущен на удаленке!")
                else:
                    print(f"Ошибка: {msg}")
                
                import os
                os.unlink(local_path)
                input("\nНажми Enter...")
            else:
                print("Неверный выбор!")
                input("\nНажми Enter...")
    
    def ssh_window_control(self, pranks):
        """Подменю управления окнами через SSH"""
        while True:
            self.clear_screen()
            print("=== УПРАВЛЕНИЕ ОКНАМИ (SSH) ===\n")
            print("1. Свернуть все окна")
            print("2. Развернуть все окна")
            print("3. Танец окон")
            print("4. Спам программами")
            print("5. Открыть CD привод")
            print("6. Спам CD приводом")
            print("7. Хаос с громкостью")
            print("8. Озвучить текст")
            print("9. Заблокировать экран")
            print("10. Случайный хаос")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                print("\nСворачиваю окна на удаленке...")
                pranks.minimize_windows()
                input("\nНажми Enter...")
            elif choice == '2':
                print("\nРазворачиваю окна на удаленке...")
                success, output = pranks.client.execute_command("DISPLAY=:0 wmctrl -k off 2>/dev/null || DISPLAY=:0 xdotool key super+d 2>/dev/null")
                print("✓ Окна развернуты" if success else f"Результат: {output}")
                input("\nНажми Enter...")
            elif choice == '3':
                cycles = input("Количество циклов (по умолчанию 5): ").strip()
                cycles = int(cycles) if cycles.isdigit() else 5
                print(f"\nЗапускаю танец окон ({cycles} циклов) на удаленке...")
                for i in range(cycles):
                    print(f"  Цикл {i+1}/{cycles}")
                    pranks.minimize_windows()
                    time.sleep(0.5)
                    pranks.client.execute_command("DISPLAY=:0 wmctrl -k off 2>/dev/null")
                    time.sleep(0.5)
                print("✓ Танец завершен!")
                input("\nНажми Enter...")
            elif choice == '4':
                prog = input("Программа для спама (например firefox): ").strip()
                if not prog:
                    prog = "firefox"
                count = input("Количество (по умолчанию 5): ").strip()
                count = int(count) if count.isdigit() else 5
                print(f"\nЗапускаю {count} экземпляров {prog} на удаленке...")
                pranks.spam_programs(prog, count)
                input("\nНажми Enter...")
            elif choice == '5':
                print("\nОткрываю CD привод на удаленке...")
                success, output = pranks.client.execute_command('eject')
                print(f"{'✓ CD открыт' if success else f'✗ Ошибка: {output}'}")
                input("\nНажми Enter...")
            elif choice == '6':
                count = input("Количество (по умолчанию 5): ").strip()
                count = int(count) if count.isdigit() else 5
                print(f"\nОткрываю CD привод {count} раз на удаленке...")
                for i in range(count):
                    print(f"  [{i+1}] Открываю...")
                    pranks.client.execute_command('eject')
                    time.sleep(2)
                    pranks.client.execute_command('eject -t')  # закрыть
                    time.sleep(0.5)
                print("✓ Готово!")
                input("\nНажми Enter...")
            elif choice == '7':
                duration = input("Длительность (сек, по умолчанию 10): ").strip()
                duration = int(duration) if duration.isdigit() else 10
                print(f"\nЗапускаю хаос с громкостью ({duration} сек)...")
                # Временная команда для случайной громкости
                for i in range(duration):
                    vol = (i * 10) % 101
                    pranks.client.execute_command(f'amixer set Master {vol}% 2>/dev/null || alsamixer -c 0 -s set Master {vol}% 2>/dev/null')
                    time.sleep(1)
                print("✓ Хаос завершен!")
                input("\nНажми Enter...")
            elif choice == '8':
                text = input("Текст для озвучки: ").strip()
                if not text:
                    text = "ПРАНК!"
                print("\nОзвучиваю на удаленке...")
                # Используем espeak если доступен
                cmd = f'espeak "{text}" 2>/dev/null || spd-say "{text}" 2>/dev/null || echo "{text}"'
                success, output = pranks.client.execute_command(cmd)
                print("✓ Сообщение озвучено!" if success else f"✗ Ошибка: {output}")
                input("\nНажми Enter...")
            elif choice == '9':
                confirm = input("Точно заблокировать экран? (y/n): ").strip().lower()
                if confirm == 'y':
                    print("\nБлокирую экран на удаленке...")
                    success, output = pranks.client.execute_command('gnome-screensaver-command --lock 2>/dev/null || xscreensaver-command -lock 2>/dev/null || dm-tool lock 2>/dev/null')
                    print("✓ Экран заблокирован!" if success else f"✗ Ошибка: {output}")
                input("\nНажми Enter...")
            elif choice == '10':
                duration = input("Длительность хаоса (сек, по умолчанию 30): ").strip()
                duration = int(duration) if duration.isdigit() else 30
                print(f"\nЗапускаю случайный хаос ({duration} сек)...")
                print("Нажмите Enter в другом окне для остановки")
                
                # Комбинация разных команд случайным образом
                import random
                commands = [
                    'wmctrl -k on',
                    'wmctrl -k off',
                    'gnome-calculator 2>/dev/null &',
                    'gedit 2>/dev/null &',
                    'eject',
                    'eject -t',
                    'xset dpms force off',
                    'xset dpms force on',
                    'amixer set Master $(shuf -i 0-100 -n 1)%'
                ]
                
                start_time = time.time()
                for i in range(duration):
                    if time.time() - start_time >= duration:
                        break
                    cmd = random.choice(commands)
                    pranks.client.execute_command(cmd)
                    time.sleep(random.uniform(1, 3))
                
                print("✓ Хаос завершен!")
                input("\nНажми Enter...")
            elif choice == '0':
                break
            else:
                print("Неверный выбор!")
                input("\nНажми Enter...")
    
    def ssh_flood(self):
        """Заливка экрана через SSH"""
        client = self.ssh_get_connection()
        if not client:
            return
        
        from core.ssh_pranks import SSHPranks
        pranks = SSHPranks(client)
        
        duration = input("Длительность (сек, по умолчанию 10): ").strip()
        duration = int(duration) if duration.isdigit() else 10
        
        print("\nЗапускаю заливку на УДАЛЕННОЙ машине...")
        pranks.screen_flood(duration)
        input("\nНажми Enter...")
    
    def ssh_text(self):
        """Показать текст через SSH"""
        client = self.ssh_get_connection()
        if not client:
            return
        
        from core.ssh_pranks import SSHPranks
        pranks = SSHPranks(client)
        
        text = input("\nТекст для показа: ").strip()
        if not text:
            text = "ПРАНК!"
        
        duration = input("Длительность (сек, по умолчанию 5): ").strip()
        duration = int(duration) if duration.isdigit() else 5
        
        print("\nПоказываю текст на УДАЛЕННОЙ машине...")
        pranks.fullscreen_text(text, duration)
        input("\nНажми Enter...")
    
    def ssh_command(self):
        """Выполнить команду через SSH"""
        client = self.ssh_get_connection()
        if not client:
            return
        
        cmd = input("\nКоманда: ").strip()
        if not cmd:
            return
        
        print("\nВыполняю...")
        success, output = client.execute_command(cmd)
        print("\n--- Результат ---")
        print(output)
        input("\nНажми Enter...")
    
    def ssh_shell(self):
        """Открыть SSH shell"""
        client = self.ssh_get_connection()
        if not client:
            return
        
        print("\nОткрываю SSH сессию...")
        print("(Для выхода используй exit или Ctrl+D)")
        time.sleep(1)
        client.open_shell()
    
    def installer_menu(self):
        """Меню установки софта"""
        while True:
            self.clear_screen()
            print("=== УСТАНОВКА СОФТА ===\n")
            print("1. Установить PortProton")
            print("2. Установить другой софт")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                from tools.installer import install_portproton
                install_portproton()
            elif choice == '0':
                break
            else:
                print("В разработке...")
            
            if choice != '0':
                input("\nНажми Enter...")
    
    def settings_menu(self):
        """Настройки"""
        while True:
            self.clear_screen()
            print("=== НАСТРОЙКИ ===\n")
            print(f"Сохраненные SSH хосты: {len(self.config['ssh_hosts'])}")
            print()
            print("1. Показать сохраненные хосты")
            print("2. Очистить историю")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                print("\nСохраненные хосты:")
                for i, host in enumerate(self.config['ssh_hosts'], 1):
                    print(f"{i}. {host['user']}@{host['host']}")
                input("\nНажми Enter...")
            elif choice == '2':
                self.config['ssh_hosts'] = []
                self.save_config()
                print("История очищена!")
                input("\nНажми Enter...")
            elif choice == '0':
                break
    
    def show_ascii_art(self, filename):
        """Показать ASCII-арт локально"""
        try:
            art_path = Path(__file__).parent / filename
            with open(art_path, 'r', encoding='utf-8') as f:
                art = f.read()
            self.clear_screen()
            print(art)
            input("\nНажми Enter...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("\nНажми Enter...")
    
    def ssh_show_ascii_art(self, pranks, filename):
        """Показать ASCII-арт на удаленной машине в GUI окне без обрезания"""
        try:
            art_path = Path(__file__).parent / filename
            with open(art_path, 'r', encoding='utf-8') as f:
                art = f.read()
            
            # Определяем цвет в зависимости от файла
            if 'skull' in filename.lower():
                color = 'white'
                bg_color = 'black'
            elif 'anime' in filename.lower():
                color = 'orange'
                bg_color = 'black'
            else:
                color = 'white'
                bg_color = 'black'
            
            # Создаем скрипт для показа ASCII-арт в полноэкранном GUI окне без обрезания
            script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.font as tkFont

# Рассчитываем размер шрифта в зависимости от размера арта
def calculate_font_size(art_lines):
    height_chars = len(art_lines)
    width_chars = max([len(line) for line in art_lines]) if art_lines else 80
    
    # Определяем размеры экрана
    root = tk.Tk()
    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()
    
    # Рассчитываем размер шрифта чтобы всё поместилось
    font_w = screen_width // width_chars if width_chars > 0 else 10
    font_h = screen_height // height_chars if height_chars > 0 else 20
    
    font_size = min(font_w, font_h, 20)  # максимум 20, минимум расчёт
    return max(font_size, 6)  # минимум 6

root = tk.Tk()
root.title("ASCII Art")
root.attributes('-fullscreen', True)
root.configure(bg='{bg_color}')

# Разбиваем арт на строки и рассчитываем размер шрифта
art_lines = """{art}""".splitlines()
font_size = calculate_font_size(art_lines)

# Создаем Canvas для отображения текста
canvas = tk.Canvas(root, bg='{bg_color}', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Сначала нужно дождаться полной инициализации окна
def render_art():
    # Получаем размеры окна
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    
    # Создаем шрифт
    font = tkFont.Font(family='Courier', size=font_size)
    
    # Отображаем каждую строку арта
    y_offset = canvas_height // 2 - (len(art_lines) * font.metrics('linespace')) // 2
    
    for i, line in enumerate(art_lines):
        y_pos = y_offset + i * font.metrics('linespace')
        canvas.create_text(canvas_width // 2, y_pos, text=line, fill='{color}', font=font, anchor='center')

# Ждем полной инициализации окна и отрисовываем арт
root.after(100, render_art)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.bind('Q', close)
root.after(5000, close)
root.mainloop()
'''
            
            # Загружаем и запускаем на удаленке
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                f.write(script)
                local_path = f.name
            
            remote_path = f"~/.ascii_art.py"
            print(f"Загружаю {filename} на удаленку...")
            success, msg = pranks.client.upload_file(local_path, remote_path)
            
            if success:
                print("Показываю ASCII-арт в полноэкранном окне на удаленке...")
                # Запускаем в фоне с DISPLAY
                pranks.client.execute_command(f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &")
                time.sleep(1)
                pranks.client.execute_command(f"rm {remote_path}")
                print("✓ ASCII-арт показан полностью на удаленке!")
            else:
                print(f"Ошибка: {msg}")
            
            import os
            os.unlink(local_path)
            input("\nНажми Enter...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("\nНажми Enter...")

if __name__ == "__main__":
    app = HamsterPrank()
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем. Пока!")
        sys.exit(0)
