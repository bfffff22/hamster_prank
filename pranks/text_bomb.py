#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пранк: Текстовая бомба
Показывает текст на весь экран с различными эффектами
"""

import sys
import os
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.display import Display

def show_fullscreen_text(text, duration=5, style='box'):
    """
    Показать текст на весь экран
    
    Args:
        text: Текст для показа
        duration: Длительность показа
        style: Стиль ('box', 'center', 'fill', 'wave')
    """
    display = Display()
    display.clear()
    display.hide_cursor()
    
    try:
        if style == 'box':
            display.print_box(text)
        elif style == 'center':
            display.print_centered(text)
        elif style == 'fill':
            fill_screen_with_text(text)
        elif style == 'wave':
            wave_text(text, duration)
            return
        
        time.sleep(duration)
    
    finally:
        display.show_cursor()
        display.clear()


def fill_screen_with_text(text):
    """Заполнить весь экран повторяющимся текстом"""
    display = Display()
    width, height = display.get_terminal_size()
    
    for y in range(height):
        line = (text + ' ') * (width // (len(text) + 1) + 1)
        sys.stdout.write(line[:width])
    
    sys.stdout.flush()


def wave_text(text, duration=5):
    """Анимация волны текста"""
    display = Display()
    width, height = display.get_terminal_size()
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        display.clear()
        
        for i, char in enumerate(text):
            offset = int(3 * abs(time.time() * 2 + i * 0.5) % 6 - 3)
            y = height // 2 + offset
            x = width // 2 - len(text) // 2 + i
            
            if 0 <= y < height and 0 <= x < width:
                display.print_at(x, y, char)
        
        time.sleep(0.1)
        
        key = display.get_key()
        if key and key.lower() == 'q':
            break


def typing_effect(text, speed=0.1):
    """Эффект печатной машинки"""
    display = Display()
    display.clear()
    display.hide_cursor()
    
    width, height = display.get_terminal_size()
    start_x = width // 2 - len(text) // 2
    start_y = height // 2
    
    try:
        for i, char in enumerate(text):
            display.print_at(start_x + i, start_y, char)
            time.sleep(speed)
        
        time.sleep(2)
    
    finally:
        display.show_cursor()
        display.clear()


def rainbow_text(text, duration=5):
    """Радужный текст (цветной если терминал поддерживает)"""
    display = Display()
    display.clear()
    
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m']
    reset = '\033[0m'
    
    start_time = time.time()
    
    while time.time() - start_time < duration:
        display.clear()
        
        colored_text = ''
        for i, char in enumerate(text):
            color = colors[i % len(colors)]
            colored_text += color + char
        colored_text += reset
        
        display.print_centered(colored_text)
        
        # Сдвигаем цвета
        colors = colors[1:] + colors[:1]
        
        time.sleep(0.2)
        
        key = display.get_key()
        if key and key.lower() == 'q':
            break
    
    display.clear()


def zoom_text(text, duration=3):
    """Эффект приближения текста"""
    display = Display()
    display.hide_cursor()
    
    try:
        for size in range(1, len(text) + 1):
            display.clear()
            partial = text[:size]
            display.print_centered(partial)
            time.sleep(duration / len(text))
        
        time.sleep(2)
    
    finally:
        display.show_cursor()
        display.clear()


def shake_text(text, duration=5):
    """Трясущийся текст"""
    display = Display()
    width, height = display.get_terminal_size()
    display.hide_cursor()
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            display.clear()
            
            # Случайное смещение
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-1, 1)
            
            x = width // 2 - len(text) // 2 + offset_x
            y = height // 2 + offset_y
            
            if 0 <= y < height:
                display.print_at(max(0, x), y, text)
            
            time.sleep(0.05)
            
            key = display.get_key()
            if key and key.lower() == 'q':
                break
    
    finally:
        display.show_cursor()
        display.clear()


def spam_text(text, count=50, delay=0.1):
    """Спам текстом по всему экрану"""
    display = Display()
    width, height = display.get_terminal_size()
    display.clear()
    display.hide_cursor()
    
    try:
        for _ in range(count):
            x = random.randint(0, max(0, width - len(text)))
            y = random.randint(0, height - 1)
            
            display.print_at(x, y, text)
            time.sleep(delay)
        
        time.sleep(2)
    
    finally:
        display.show_cursor()
        display.clear()


def interactive_menu():
    """Интерактивное меню текстовых пранков"""
    display = Display()
    
    while True:
        display.clear()
        print("=== ТЕКСТОВЫЕ ПРАНКИ ===\n")
        print("1. Текст в рамке")
        print("2. Заполнить экран текстом")
        print("3. Волна")
        print("4. Печатная машинка")
        print("5. Радужный текст")
        print("6. Приближение")
        print("7. Тряска")
        print("8. Спам")
        print("0. Выход")
        print()
        
        choice = input("Выбери эффект: ").strip()
        
        if choice == '0':
            break
        
        if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
            text = input("Введи текст: ").strip()
            if not text:
                text = "ПРАНК!"
            
            print("\nЗапуск...")
            time.sleep(1)
            
            if choice == '1':
                show_fullscreen_text(text, duration=5, style='box')
            elif choice == '2':
                show_fullscreen_text(text, duration=5, style='fill')
            elif choice == '3':
                wave_text(text, duration=5)
            elif choice == '4':
                typing_effect(text, speed=0.1)
            elif choice == '5':
                rainbow_text(text, duration=5)
            elif choice == '6':
                zoom_text(text, duration=3)
            elif choice == '7':
                shake_text(text, duration=5)
            elif choice == '8':
                spam_text(text, count=50, delay=0.1)
        else:
            print("Неверный выбор!")
            time.sleep(1)


if __name__ == "__main__":
    try:
        interactive_menu()
    except KeyboardInterrupt:
        print("\n\nПрервано!")
        sys.exit(0)
