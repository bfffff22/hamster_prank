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
        self.use_gui = False  # Режим работы: GUI или только консоль
        self.tkinter_available = False  # Доступен ли tkinter
        
    def load_config(self):
        """Загрузка конфига"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"last_mode": None}
    
    def save_config(self):
        """Сохранение конфига"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def clear_screen(self):
        """Очистка экрана"""
        os.system('cls' if IS_WINDOWS else 'clear')
    
    def print_banner(self):
        """Вывод баннера"""
        mode = "GUI + Console" if self.use_gui else "Console Only"
        banner = f"""
========================================
    HAMSTER PRANK - Swiss Knife
        Pranks & Remote Control
    Режим: {mode}
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
            print("6. ASCII-арт")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                from pranks.screen_flood import interactive_menu
                interactive_menu()
            elif choice == '2':
                self._launch_prank_with_tkinter_check('fullscreen')
            elif choice == '3':
                from pranks.text_bomb import interactive_menu
                interactive_menu()
            elif choice == '4':
                self._launch_prank_with_tkinter_check('window_chaos')
            elif choice == '5':
                cmd = input("Команда для запуска: ")
                os.system(cmd)
            elif choice == '6':
                self.ascii_art_menu()
            elif choice == '0':
                break
            
            if choice != '0' and choice == '5':
                input("\nНажми Enter для продолжения...")
    
    def ascii_art_menu(self):
        """Меню ASCII-арт"""
        while True:
            self.clear_screen()
            print("=== ASCII-АРТ ===\n")
            print("1. Skull")
            print("2. Chill")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                self.show_ascii_art('skull.txt')
            elif choice == '2':
                self.show_ascii_art('chill.txt')
            elif choice == '0':
                break
    
    def _launch_prank_with_tkinter_check(self, prank_type):
        """Запустить пранк с проверкой tkinter"""
        from core.tkinter_check import checker
        
        if not checker.check_local():
            print("\n✗ tkinter не обнаружен!")
            print("\nВыберите действие:")
            print("1. Установить tkinter автоматически")
            print("2. Запустить альтернативный вариант (без GUI)")
            print("0. Отмена")
            print()
            
            choice = input("Ваш выбор: ").strip()
            
            if choice == '1':
                print("\nУстанавливаю tkinter...")
                if IS_LINUX:
                    os.system("sudo apt-get install -y python3-tk 2>/dev/null || sudo dnf install -y python3-tkinter 2>/dev/null || sudo pacman -S tk 2>/dev/null")
                else:
                    print("На Windows переустановите Python с официального сайта с опцией tcl/tk")
                    input("\nНажми Enter...")
                    return
                
                # Проверяем снова
                if checker.check_local():
                    print("✓ tkinter установлен!")
                    self.use_gui = True
                else:
                    print("✗ Не удалось установить tkinter")
                    input("\nНажми Enter...")
                    return
            elif choice == '2':
                print("\nЗапускаю альтернативный вариант...")
                # Запускаем консольную версию
                if prank_type == 'fullscreen':
                    from pranks.screen_flood import interactive_menu
                    interactive_menu()
                elif prank_type == 'window_chaos':
                    from pranks.screen_flood import interactive_menu
                    interactive_menu()
                return
            else:
                return
        
        # Запускаем GUI версию
        if prank_type == 'fullscreen':
            from pranks.fullscreen_pranks import interactive_menu
            interactive_menu()
        elif prank_type == 'window_chaos':
            from pranks.window_chaos import interactive_menu
            interactive_menu()
    
    def ssh_menu(self):
        """Меню SSH операций"""
        while True:
            self.clear_screen()
            print("=== SSH ПРАНКИ ===\n")
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
        from core.ssh_client_paramiko import SSHClientSimple, parse_ssh_string
        
        print("\n=== SSH ПОДКЛЮЧЕНИЕ ===")
        host_str = input("Хост (user@ip:port): ").strip()
        
        if not host_str:
            return None
        
        host, port, user = parse_ssh_string(host_str)
        
        # Запрашиваем пароль
        import getpass
        password = getpass.getpass(f"Пароль для {user}@{host}: ")
        
        client = SSHClientSimple(host, port, user, password)
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
        from core.tkinter_check import checker
        
        pranks = SSHPranksFiles(client)
        
        # Проверяем наличие tkinter на удаленной машине
        host_key = f"{client.host}:{client.port}"
        remote_has_tkinter = checker.check_remote(client, host_key)
        
        if remote_has_tkinter:
            print(f"\n✓ tkinter обнаружен на удаленной машине!")
        else:
            print(f"\n✗ tkinter не обнаружен на удаленной машине!")
            print("Доступны только консольные пранки.")
        
        input("\nНажми Enter для продолжения...")
        
        while True:
            self.clear_screen()
            print("=== SSH ОПЕРАЦИИ (на удаленной машине) ===\n")
            print("1. Пранки в консоли (матрица, глитч)")
            print("2. Полноэкранные пранки (GUI окна)")
            print("3. Текстовые эффекты")
            print("4. Управление окнами")
            print("5. Запустить программу")
            print("6. ASCII-арт")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                self.ssh_console_pranks(pranks)
            elif choice == '2':
                self._ssh_launch_prank_with_tkinter_check(pranks, client, 'fullscreen')
            elif choice == '3':
                self.ssh_text_effects(pranks, client)
            elif choice == '4':
                self._ssh_launch_prank_with_tkinter_check(pranks, client, 'window_control')
            elif choice == '5':
                cmd = input("Команда для запуска: ")
                if cmd:
                    print("\nВыполняю...")
                    success, output = pranks.client.execute_command(cmd)
                    print("\n--- Результат ---")
                    print(output)
                    input("\nНажми Enter...")
            elif choice == '6':
                self.ssh_ascii_art_menu(pranks)
            elif choice == '0':
                break
    
    def ssh_ascii_art_menu(self, pranks):
        """Меню ASCII-арт для SSH"""
        while True:
            self.clear_screen()
            print("=== ASCII-АРТ (SSH) ===\n")
            print("1. Skull")
            print("2. Chill")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                self.ssh_show_ascii_art(pranks, 'skull.txt')
            elif choice == '2':
                self.ssh_show_ascii_art(pranks, 'chill.txt')
            elif choice == '0':
                break
    
    def _ssh_launch_prank_with_tkinter_check(self, pranks, client, prank_type):
        """Запустить SSH пранк с проверкой tkinter на удаленной машине"""
        from core.tkinter_check import checker
        
        host_key = f"{client.host}:{client.port}"
        remote_has_tkinter = checker.check_remote(client, host_key)
        
        if not remote_has_tkinter:
            print("\n✗ tkinter не обнаружен на удаленной машине!")
            print("\nВыберите действие:")
            print("1. Установить tkinter на удаленной машине")
            print("2. Запустить альтернативный вариант (без GUI)")
            print("0. Отмена")
            print()
            
            choice = input("Ваш выбор: ").strip()
            
            if choice == '1':
                print("\nУстанавливаю tkinter на удаленной машине...")
                pranks.client.execute_command("sudo apt-get install -y python3-tk 2>/dev/null || sudo dnf install -y python3-tkinter 2>/dev/null || sudo pacman -S tk 2>/dev/null")
                
                # Проверяем снова
                checker.remote_available.pop(host_key, None)  # Сбрасываем кеш
                if checker.check_remote(client, host_key):
                    print("✓ tkinter установлен на удаленной машине!")
                else:
                    print("✗ Не удалось установить tkinter")
                    input("\nНажми Enter...")
                    return
            elif choice == '2':
                print("\nЗапускаю альтернативный вариант...")
                # Запускаем консольную версию
                if prank_type == 'fullscreen':
                    self.ssh_console_pranks(pranks)
                elif prank_type == 'window_control':
                    self.ssh_console_pranks(pranks)
                return
            else:
                return
        
        # Запускаем GUI версию
        if prank_type == 'fullscreen':
            self.ssh_fullscreen_pranks(pranks)
        elif prank_type == 'window_control':
            self.ssh_window_control(pranks)
    
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
                
                # Создаем скрипт для показа изображения
                script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

root = tk.Tk()
root.withdraw()
root.title("Полноэкранная картинка")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{{screen_width}}x{{screen_height}}+0+0')

root.deiconify()
root.focus_force()

try:
    # Загружаем изображение по URL
    response = requests.get("{image_url}", timeout=10)
    response.raise_for_status()
    
    # Открываем изображение
    img_data = Image.open(BytesIO(response.content))
    
    # Изменяем размер чтобы поместить в экран
    img_width, img_height = img_data.size
    ratio = min(screen_width/img_width, screen_height/img_height)
    new_width = int(img_width * ratio)
    new_height = int(img_height * ratio)
    
    img_resized = img_data.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Конвертируем в PhotoImage
    photo = ImageTk.PhotoImage(img_resized)
    
    # Создаем Label для отображения
    label = tk.Label(root, image=photo, bg='black')
    label.pack(expand=True)
    
    # Сохраняем ссылку на фото
    label.image = photo

except Exception as e:
    # Если ошибка загрузки, показываем сообщение
    error_label = tk.Label(root, text=f'Ошибка загрузки изображения:\\n{{e}}', 
                          bg='black', fg='red', font=('Courier', 16))
    error_label.pack(expand=True)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.bind('Q', close)
root.after({duration}000, close)

try:
    root.mainloop()
except:
    pass
'''
                
                # Загружаем и запускаем на удаленке
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
                    f.write(script)
                    local_path = f.name
                
                remote_path = "/tmp/.image_viewer.py"
                success, msg = pranks.client.upload_file(local_path, remote_path)
                
                if success:
                    print("Проверяю PIL...")
                    # Проверяем, установлен ли PIL
                    check_pil = 'python3 -c "from PIL import Image, ImageTk; import requests" 2>&1'
                    pil_check_success, pil_result = pranks.client.execute_command(check_pil)
                    
                    if "ModuleNotFoundError" in pil_result or "No module named" in pil_result:
                        print("Устанавливаю PIL и requests на удаленной машине...")
                        pranks.client.execute_command("pip3 install Pillow requests 2>&1 || sudo apt-get install -y python3-pil python3-requests 2>&1")
                    
                    print("Запускаю показ картинки...")
                    pranks.client.execute_command("export DISPLAY=:0 && xhost +local: 2>/dev/null || true")
                    pranks.client.execute_command(f"chmod +x {remote_path}")
                    
                    # Запускаем БЕЗ удаления файла
                    pranks.client.execute_command(f"DISPLAY=:0 python3 {remote_path} &")
                    
                    time.sleep(3)  # Даем время на запуск
                    
                    # Проверяем процесс
                    ps_success, ps_out = pranks.client.execute_command("ps aux | grep image_viewer | grep -v grep")
                    if "python3" in ps_out:
                        print("✓ Процесс запущен и работает!")
                    else:
                        print("⚠ Процесс завершился")
                    
                    print("✓ Картинка показана!")
                else:
                    print(f"✗ Ошибка: {msg}")
                
                import os
                os.unlink(local_path)
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
    
    def ssh_text_effects(self, pranks, client):
        """Подменю текстовых эффектов через SSH"""
        from core.tkinter_check import checker
        
        while True:
            self.clear_screen()
            print("=== ТЕКСТОВЫЕ ЭФФЕКТЫ (SSH) ===\n")
            print("1. Текст в рамке (GUI)")
            print("2. Заполнить экран текстом (GUI)")
            print("3. Волна")
            print("4. Печатная машинка (GUI)")
            print("5. Радужный текст")
            print("6. Приближение (GUI)")
            print("7. Тряска (GUI)")
            print("8. Спам (GUI)")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '0':
                break
            elif choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                # Проверяем, требует ли выбранная опция GUI
                gui_required = choice in ['1', '2', '4', '6', '7', '8']
                
                if gui_required:
                    host_key = f"{client.host}:{client.port}"
                    remote_has_tkinter = checker.check_remote(client, host_key)
                    
                    if not remote_has_tkinter:
                        print("\n✗ tkinter не обнаружен на удаленной машине!")
                        print("\nВыберите действие:")
                        print("1. Установить tkinter на удаленной машине")
                        print("2. Запустить альтернативный вариант (консоль)")
                        print("0. Отмена")
                        print()
                        
                        action = input("Ваш выбор: ").strip()
                        
                        if action == '1':
                            print("\nУстанавливаю tkinter...")
                            pranks.client.execute_command("sudo apt-get install -y python3-tk 2>/dev/null || sudo dnf install -y python3-tkinter 2>/dev/null")
                            checker.remote_available.pop(host_key, None)
                            
                            if not checker.check_remote(client, host_key):
                                print("✗ Не удалось установить tkinter")
                                input("\nНажми Enter...")
                                continue
                            print("✓ tkinter установлен!")
                        elif action == '2':
                            # Используем консольные эффекты
                            choice = '3'  # Волна или радуга
                        else:
                            continue
                
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
                    print(f"Запускаю волну на удаленке...")
                    pranks.wave_text(text)
                    input("\nНажми Enter...")
                    continue  # пропускаем общий код загрузки скрипта
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
                    print(f"Запускаю радугу на удаленке...")
                    pranks.rainbow_text(text)
                    input("\nНажми Enter...")
                    continue  # пропускаем общий код загрузки скрипта
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
import os

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

root = tk.Tk()
root.withdraw()
root.title("Тряска")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{{screen_width}}x{{screen_height}}+0+0')

root.deiconify()
root.focus_force()

text_widget = tk.Text(root, bg='black', fg='white', font=('Courier', 24), wrap='word')
text_widget.pack(expand=True, fill='both', padx=100, pady=200)
text_widget.insert('1.0', '{text}')
text_widget.tag_add('shake', '1.0', 'end')
text_widget.config(state='disabled')

shake_count = [0]

def shake():
    if shake_count[0] < 100:
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 5)
        text_widget.place(x=100+dx, y=200+dy)
        shake_count[0] += 1
        root.after(50, shake)

shake()

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)

try:
    root.mainloop()
except:
    pass
'''
                elif choice == '8':  # Спам
                    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import random
import os

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

root = tk.Tk()
root.withdraw()
root.title("Спам")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f'{{screen_width}}x{{screen_height}}+0+0')

root.deiconify()
root.focus_force()

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

root.update()

for _ in range(50):
    x = random.randint(50, screen_width-50)
    y = random.randint(50, screen_height-50)
    canvas.create_text(x, y, text='{text}', fill='white', font=('Courier', random.randint(10, 50)))

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.after(5000, close)

try:
    root.mainloop()
except:
    pass
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
            print("1. О программе")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                print("\nHamster Prank - Swiss Army Knife для пранков")
                print("Версия: 2.0")
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
            elif 'chill' in filename.lower():
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

root = tk.Tk()
root.title("ASCII Art")
root.attributes('-fullscreen', True)
root.configure(bg='{bg_color}')

# Разбиваем арт на строки
art_lines = """{art}""".splitlines()

# Создаем Canvas для отображения текста
canvas = tk.Canvas(root, bg='{bg_color}', highlightthickness=0)
canvas.pack(fill='both', expand=True)

# Ждем полной инициализации окна и отрисовываем арт
def render_art():
    # Получаем размеры окна
    canvas_width = root.winfo_width()
    canvas_height = root.winfo_height()
    
    # Рассчитываем размер шрифта в зависимости от размера арта и экрана
    height_chars = len(art_lines)
    width_chars = max([len(line) for line in art_lines]) if art_lines else 80
    
    # Уменьшаем шрифт, чтобы всё поместилось
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    font_w = screen_width // width_chars if width_chars > 0 else 10
    font_h = screen_height // (height_chars * 2) if height_chars > 0 else 10  # уменьшил в 2 раза
    
    font_size = min(font_w, font_h, 10)  # уменьшил до 10
    font_size = max(font_size, 5)  # минимум 5
    
    # Создаем шрифт
    font = tkFont.Font(family='Courier', size=font_size)
    
    # Отображаем каждую строку арта с прокруткой если нужно
    for i, line in enumerate(art_lines):
        # Рассчитываем позицию чтобы текст был по центру
        text_height = len(art_lines) * font.metrics('linespace')
        start_y = (canvas_height - text_height) // 2 if text_height < canvas_height else 10
        
        y_pos = start_y + i * font.metrics('linespace')
        if y_pos < canvas_height:  # только видимые строки
            canvas.create_text(canvas_width // 2, y_pos, text=line, fill='{color}', font=font, anchor='center')

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
                print("✓ ASCII-арт показан на удаленке!")
            else:
                print(f"Ошибка: {msg}")
            
            import os
            os.unlink(local_path)
            input("\nНажми Enter...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("\nНажми Enter...")
    
    def ssh_show_ascii_art_console(self, pranks, filename):
        """Показать ASCII-арт на удаленной машине в консоли (без tkinter)"""
        try:
            art_path = Path(__file__).parent / filename
            with open(art_path, 'r', encoding='utf-8') as f:
                art = f.read()
            
            print(f"\nПоказываю {filename} в консоли на удаленке...")
            
            # Создаем временный файл с артом
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(art)
                local_path = f.name
            
            remote_path = f"~/.ascii_art.txt"
            success, msg = pranks.client.upload_file(local_path, remote_path)
            
            if success:
                # Показываем в консоли через cat
                pranks.client.execute_command(f"cat {remote_path}")
                pranks.client.execute_command(f"rm {remote_path}")
                print("✓ ASCII-арт показан в консоли на удаленке!")
            else:
                print(f"Ошибка: {msg}")
            
            import os
            os.unlink(local_path)
            input("\nНажми Enter...")
        except Exception as e:
            print(f"Ошибка: {e}")
            input("\nНажми Enter...")

if __name__ == "__main__":
    # Проверяем обновления при запуске
    try:
        from core.auto_update import check_and_update
        if check_and_update():
            print("\nПрограмма обновлена. Перезапустите её.")
            sys.exit(0)
    except Exception as e:
        print(f"Ошибка проверки обновлений: {e}")
    
    app = HamsterPrank()
    
    # Проверяем наличие tkinter при запуске
    from core.tkinter_check import checker
    
    print("\nПроверка системы...")
    app.tkinter_available = checker.check_local()
    
    if app.tkinter_available:
        print("✓ tkinter обнаружен")
        print("\nВыберите режим работы:")
        print("1. С GUI (полноэкранные окна, графические эффекты)")
        print("2. Только консоль (текстовые эффекты в терминале)")
        print()
        choice = input("Ваш выбор (1/2, по умолчанию 1): ").strip()
        app.use_gui = (choice != '2')
    else:
        print("✗ tkinter не обнаружен")
        print("\nДоступны только консольные пранки.")
        print("Для GUI пранков установите tkinter:")
        print(checker.get_install_instructions('linux' if IS_LINUX else 'windows'))
        print("\nПродолжить в консольном режиме?")
        choice = input("(y/n, по умолчанию y): ").strip().lower()
        if choice == 'n':
            print("Выход...")
            sys.exit(0)
        app.use_gui = False
    
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем. Пока!")
        sys.exit(0)
