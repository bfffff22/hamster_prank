#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Полноэкранные пранки - выводятся на весь экран, а не только в консоль
"""

import sys
import os
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.fullscreen import FullscreenWindow
from core.display import Display

def fullscreen_text_prank():
    """Полноэкранный текст"""
    print("\n=== ПОЛНОЭКРАННЫЙ ТЕКСТ ===")
    text = input("Текст для показа: ").strip()
    if not text:
        text = "ТЫ ВЗЛОМАН!"
    
    duration = input("Длительность (сек, по умолчанию 5): ").strip()
    duration = int(duration) if duration.isdigit() else 5
    
    print("\nЦвет фона:")
    print("1. Черный")
    print("2. Красный")
    print("3. Синий")
    bg_choice = input("Выбери (1-3): ").strip()
    
    bg_colors = {'1': 'Black', '2': 'Red', '3': 'Blue'}
    bg_color = bg_colors.get(bg_choice, 'Black')
    
    print("\nЦвет текста:")
    print("1. Красный")
    print("2. Белый")
    print("3. Желтый")
    print("4. Зеленый")
    fg_choice = input("Выбери (1-4): ").strip()
    
    fg_colors = {'1': 'Red', '2': 'White', '3': 'Yellow', '4': 'Lime'}
    fg_color = fg_colors.get(fg_choice, 'Red')
    
    print(f"\nЗапускаю полноэкранное окно на {duration} сек...")
    print("(Нажми ESC или Q для закрытия)")
    time.sleep(1)
    
    success, msg = FullscreenWindow.create_fullscreen_text(text, duration, bg_color, fg_color)
    print(msg)


def fullscreen_flood_prank():
    """Полноэкранная заливка"""
    print("\n=== ПОЛНОЭКРАННАЯ ЗАЛИВКА ===")
    
    duration = input("Длительность (сек, по умолчанию 10): ").strip()
    duration = int(duration) if duration.isdigit() else 10
    
    print(f"\nЗапускаю заливку на {duration} сек...")
    print("(Нажми ESC или Q для закрытия)")
    time.sleep(1)
    
    success, msg = FullscreenWindow.create_fullscreen_flood(duration)
    print(msg)


def fullscreen_image_prank():
    """Полноэкранная картинка"""
    print("\n=== ПОЛНОЭКРАННАЯ КАРТИНКА ===")
    
    image_path = input("Путь к картинке: ").strip()
    
    if not image_path or not os.path.exists(image_path):
        print("✗ Файл не найден!")
        return
    
    duration = input("Длительность (сек, по умолчанию 5): ").strip()
    duration = int(duration) if duration.isdigit() else 5
    
    print(f"\nПоказываю картинку на {duration} сек...")
    time.sleep(1)
    
    success, msg = FullscreenWindow.create_image_fullscreen(image_path, duration)
    print(msg)


def multiple_windows_spam():
    """Спам полноэкранными окнами"""
    print("\n=== СПАМ ОКНАМИ ===")
    
    text = input("Текст: ").strip()
    if not text:
        text = "ПРАНК!"
    
    count = input("Количество окон (по умолчанию 5): ").strip()
    count = int(count) if count.isdigit() else 5
    
    print(f"\nЗапускаю {count} окон...")
    time.sleep(1)
    
    for i in range(count):
        FullscreenWindow.create_fullscreen_text(f"{text} #{i+1}", duration=3)
        time.sleep(0.5)
    
    print("✓ Окна запущены!")


def interactive_menu():
    """Меню полноэкранных пранков"""
    display = Display()
    
    while True:
        display.clear()
        print("=== ПОЛНОЭКРАННЫЕ ПРАНКИ ===\n")
        print("1. Полноэкранный текст")
        print("2. Полноэкранная заливка")
        print("3. Китайская атака (символы летают)")
        print("4. Полноэкранная картинка")
        print("5. Спам окнами")
        print("0. Назад")
        print()
        
        choice = input("Выбери: ").strip()
        
        if choice == '1':
            fullscreen_text_prank()
            input("\nНажми Enter...")
        elif choice == '2':
            fullscreen_flood_prank()
            input("\nНажми Enter...")
        elif choice == '3':
            from pranks.chinese_attack import chinese_attack
            duration = input("Длительность (сек, по умолчанию 15): ").strip()
            duration = int(duration) if duration.isdigit() else 15
            print(f"\nЗапускаю китайскую атаку на {duration} сек...")
            success, msg = chinese_attack(duration)
            print(msg)
            input("\nНажми Enter...")
        elif choice == '4':
            fullscreen_image_prank()
            input("\nНажми Enter...")
        elif choice == '5':
            multiple_windows_spam()
            input("\nНажми Enter...")
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
