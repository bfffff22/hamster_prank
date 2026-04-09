#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пранк: Хаос с окнами
Управление окнами - сворачивание, разворачивание, открытие программ
"""

import sys
import os
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.system import SystemOps
from core.display import Display

def minimize_all():
    """Свернуть все окна"""
    print("Сворачиваю все окна...")
    success, msg = SystemOps.minimize_all_windows()
    if success:
        print("✓ Все окна свернуты!")
    else:
        print(f"✗ Ошибка: {msg}")
    time.sleep(2)


def restore_all():
    """Развернуть все окна"""
    print("Разворачиваю все окна...")
    success, msg = SystemOps.restore_all_windows()
    if success:
        print("✓ Все окна развернуты!")
    else:
        print(f"✗ Ошибка: {msg}")
    time.sleep(2)


def window_dance(cycles=5):
    """Танец окон - сворачивание и разворачивание"""
    print(f"Запускаю танец окон ({cycles} циклов)...")
    
    for i in range(cycles):
        print(f"Цикл {i+1}/{cycles}")
        
        # Сворачиваем
        SystemOps.minimize_all_windows()
        time.sleep(0.5)
        
        # Разворачиваем
        SystemOps.restore_all_windows()
        time.sleep(0.5)
    
    print("✓ Танец завершен!")
    time.sleep(2)


def spam_programs(programs, count=5):
    """Спам запуском программ"""
    print(f"Запускаю {count} экземпляров программ...")
    
    for i in range(count):
        for prog in programs:
            success, msg = SystemOps.open_program(prog)
            print(f"  [{i+1}] {prog}: {msg}")
            time.sleep(0.3)
    
    print("✓ Программы запущены!")
    time.sleep(2)


def open_notepad_spam(count=10, with_text=None):
    """Спам блокнотами"""
    print(f"Открываю {count} блокнотов...")
    
    for i in range(count):
        if sys.platform == 'win32':
            SystemOps.open_program('notepad')
        else:
            SystemOps.open_program('gedit')
        
        time.sleep(0.2)
    
    print("✓ Блокноты открыты!")
    time.sleep(2)


def open_browser_tabs(urls, count=5):
    """Открыть множество вкладок браузера"""
    print(f"Открываю {count} вкладок...")
    
    browser_cmd = 'start' if sys.platform == 'win32' else 'xdg-open'
    
    for i in range(count):
        url = random.choice(urls) if urls else 'about:blank'
        SystemOps.run_command(f'{browser_cmd} {url}', capture=False)
        time.sleep(0.3)
    
    print("✓ Вкладки открыты!")
    time.sleep(2)


def eject_cd_spam(count=5):
    """Спам открытием CD привода"""
    print(f"Открываю CD привод {count} раз...")
    
    for i in range(count):
        success, msg = SystemOps.eject_cd()
        print(f"  [{i+1}] {msg}")
        time.sleep(2)
    
    print("✓ Готово!")
    time.sleep(2)


def volume_chaos(duration=10):
    """Хаос с громкостью"""
    print(f"Запускаю хаос с громкостью ({duration} сек)...")
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        volume = random.randint(0, 100)
        SystemOps.set_volume(volume)
        print(f"  Громкость: {volume}%")
        time.sleep(1)
    
    print("✓ Хаос завершен!")
    time.sleep(2)


def speak_spam(messages, count=3):
    """Спам голосовыми сообщениями"""
    print(f"Озвучиваю сообщения {count} раз...")
    
    for i in range(count):
        for msg in messages:
            print(f"  [{i+1}] Говорю: {msg}")
            SystemOps.speak_text(msg)
            time.sleep(1)
    
    print("✓ Готово!")
    time.sleep(2)


def lock_screen_prank():
    """Заблокировать экран"""
    print("Блокирую экран через 3 секунды...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    success, msg = SystemOps.lock_screen()
    print(msg)


def random_chaos(duration=30):
    """Случайный хаос - комбинация разных пранков"""
    print(f"Запускаю случайный хаос ({duration} сек)...")
    print("Нажми Ctrl+C для остановки")
    
    pranks = [
        lambda: SystemOps.minimize_all_windows(),
        lambda: SystemOps.restore_all_windows(),
        lambda: SystemOps.open_program('notepad' if sys.platform == 'win32' else 'gedit'),
        lambda: SystemOps.eject_cd(),
    ]
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            prank = random.choice(pranks)
            prank()
            time.sleep(random.uniform(1, 3))
    except KeyboardInterrupt:
        print("\n✓ Хаос остановлен!")
    
    time.sleep(2)


def interactive_menu():
    """Интерактивное меню пранков с окнами"""
    display = Display()
    
    while True:
        display.clear()
        print("=== ПРАНКИ С ОКНАМИ ===\n")
        print("1. Свернуть все окна")
        print("2. Развернуть все окна")
        print("3. Танец окон (5 циклов)")
        print("4. Спам блокнотами (10 шт)")
        print("5. Открыть CD привод")
        print("6. Спам CD приводом (5 раз)")
        print("7. Хаос с громкостью (10 сек)")
        print("8. Озвучить текст")
        print("9. Заблокировать экран")
        print("10. Случайный хаос (30 сек)")
        print("0. Выход")
        print()
        
        choice = input("Выбери пранк: ").strip()
        
        if choice == '1':
            minimize_all()
        elif choice == '2':
            restore_all()
        elif choice == '3':
            window_dance(cycles=5)
        elif choice == '4':
            open_notepad_spam(count=10)
        elif choice == '5':
            success, msg = SystemOps.eject_cd()
            print(msg)
            time.sleep(2)
        elif choice == '6':
            eject_cd_spam(count=5)
        elif choice == '7':
            volume_chaos(duration=10)
        elif choice == '8':
            text = input("Текст для озвучки: ").strip()
            if text:
                print("Озвучиваю...")
                SystemOps.speak_text(text)
                time.sleep(2)
        elif choice == '9':
            confirm = input("Точно заблокировать? (y/n): ").strip().lower()
            if confirm == 'y':
                lock_screen_prank()
                break
        elif choice == '10':
            random_chaos(duration=30)
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")
            time.sleep(1)


if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано!")
        sys.exit(0)
