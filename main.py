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
            print("1. Заливка экрана")
            print("2. Матрица")
            print("3. Глитч эффект")
            print("4. Тряска экрана")
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
                duration = input("Длительность (сек, по умолчанию 10): ").strip()
                duration = int(duration) if duration.isdigit() else 10
                print("\nЗапускаю тряску на удаленке...")
                pranks.screen_shake(duration)
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
            elif choice == '0':
                break
    
    def ssh_text_effects(self, pranks):
        """Подменю текстовых эффектов через SSH"""
        while True:
            self.clear_screen()
            print("=== ТЕКСТОВЫЕ ЭФФЕКТЫ (SSH) ===\n")
            print("1. Волна текста")
            print("2. Радужный текст")
            print("0. Назад")
            print()
            
            choice = input("Выбери: ").strip()
            
            if choice == '1':
                text = input("Текст: ").strip()
                if not text:
                    text = "ВОЛНА!"
                print("\nЗапускаю волну на удаленке...")
                pranks.wave_text(text)
                input("\nНажми Enter...")
            elif choice == '2':
                text = input("Текст: ").strip()
                if not text:
                    text = "РАДУГА!"
                print("\nЗапускаю радугу на удаленке...")
                pranks.rainbow_text(text)
                input("\nНажми Enter...")
            elif choice == '0':
                break
    
    def ssh_window_control(self, pranks):
        """Подменю управления окнами через SSH"""
        while True:
            self.clear_screen()
            print("=== УПРАВЛЕНИЕ ОКНАМИ (SSH) ===\n")
            print("1. Свернуть все окна")
            print("2. Развернуть все окна")
            print("3. Танец окон")
            print("4. Спам программами")
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
            elif choice == '0':
                break
    
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
        """Показать ASCII-арт на удаленной машине в GUI окне"""
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
            
            # Создаем скрипт для показа ASCII-арт в GUI окне
            script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import sys

art = """{art}"""

root = tk.Tk()
root.title("ASCII Art")
root.attributes('-fullscreen', True)
root.configure(bg='{bg_color}')

text = tk.Text(root, bg='{bg_color}', fg='{color}', font=('Courier', 10), wrap='none')
text.pack(fill='both', expand=True)
text.insert('1.0', art)
text.config(state='disabled')

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

if __name__ == "__main__":
    app = HamsterPrank()
    try:
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем. Пока!")
        sys.exit(0)
