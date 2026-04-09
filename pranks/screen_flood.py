#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пранк: Заливка экрана символами
Заполняет весь экран случайными символами с анимацией
"""

import sys
import os
import time
import random
from pathlib import Path

# Добавляем путь к core модулям
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.display import Display

def screen_flood(duration=10, char=None, speed='fast'):
    """
    Залить экран символами
    
    Args:
        duration: Длительность в секундах
        char: Символ для заливки (None = случайные)
        speed: Скорость ('slow', 'medium', 'fast', 'insane')
    """
    display = Display()
    width, height = display.get_terminal_size()
    
    # Скорость задержки
    speeds = {
        'slow': 0.1,
        'medium': 0.05,
        'fast': 0.01,
        'insane': 0.001
    }
    delay = speeds.get(speed, 0.01)
    
    # Набор символов для случайной генерации
    chars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789'
    
    display.clear()
    display.hide_cursor()
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Случайная позиция
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            
            # Случайный символ
            symbol = char if char else random.choice(chars)
            
            display.print_at(x, y, symbol)
            time.sleep(delay)
            
            # Проверка на прерывание
            key = display.get_key()
            if key and key.lower() == 'q':
                break
    
    finally:
        display.show_cursor()
        display.clear()
        print("Пранк завершен!")


def matrix_rain(duration=15):
    """
    Эффект 'Матрицы' - падающие символы
    """
    display = Display()
    width, height = display.get_terminal_size()
    
    # Создаем колонки
    columns = []
    for i in range(width):
        columns.append({
            'y': random.randint(-height, 0),
            'speed': random.randint(1, 3),
            'length': random.randint(5, 20)
        })
    
    chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン'
    
    display.clear()
    display.hide_cursor()
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            for x, col in enumerate(columns):
                # Очищаем хвост
                if col['y'] - col['length'] >= 0:
                    display.print_at(x, col['y'] - col['length'], ' ')
                
                # Рисуем голову
                if 0 <= col['y'] < height:
                    display.print_at(x, col['y'], random.choice(chars))
                
                # Двигаем колонку
                col['y'] += col['speed']
                
                # Сброс колонки
                if col['y'] - col['length'] > height:
                    col['y'] = random.randint(-height, 0)
                    col['speed'] = random.randint(1, 3)
                    col['length'] = random.randint(5, 20)
            
            time.sleep(0.05)
            
            # Проверка на прерывание
            key = display.get_key()
            if key and key.lower() == 'q':
                break
    
    finally:
        display.show_cursor()
        display.clear()
        print("Матрица остановлена!")


def glitch_effect(duration=10):
    """
    Эффект глитча - случайные мигания и искажения
    """
    display = Display()
    width, height = display.get_terminal_size()
    
    glitch_chars = '█▓▒░▀▄▌▐│─┼╬═║╔╗╚╝'
    
    display.clear()
    display.hide_cursor()
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Случайные блоки глитча
            for _ in range(random.randint(5, 20)):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                length = random.randint(1, 10)
                
                glitch_str = ''.join(random.choice(glitch_chars) for _ in range(length))
                display.print_at(x, y, glitch_str[:width - x])
            
            time.sleep(random.uniform(0.01, 0.1))
            
            # Иногда очищаем экран
            if random.random() < 0.1:
                display.clear()
            
            # Проверка на прерывание
            key = display.get_key()
            if key and key.lower() == 'q':
                break
    
    finally:
        display.show_cursor()
        display.clear()
        print("Глитч завершен!")


def screen_shake(duration=5):
    """
    Эффект тряски экрана - быстрая смена содержимого
    """
    display = Display()
    width, height = display.get_terminal_size()
    
    display.hide_cursor()
    
    start_time = time.time()
    
    try:
        while time.time() - start_time < duration:
            # Заполняем экран случайными символами
            display.clear()
            for y in range(height):
                line = ''.join(random.choice(' ░▒▓█') for _ in range(width))
                sys.stdout.write(line)
            sys.stdout.flush()
            
            time.sleep(0.05)
            
            # Проверка на прерывание
            key = display.get_key()
            if key and key.lower() == 'q':
                break
    
    finally:
        display.show_cursor()
        display.clear()
        print("Тряска остановлена!")


def interactive_menu():
    """Интерактивное меню выбора пранка"""
    display = Display()
    
    while True:
        display.clear()
        print("=== ПРАНКИ С ЭКРАНОМ ===\n")
        print("1. Заливка символами (10 сек)")
        print("2. Матрица (15 сек)")
        print("3. Глитч эффект (10 сек)")
        print("4. Тряска экрана (5 сек)")
        print("5. Кастомная заливка")
        print("0. Выход")
        print("\nНажми 'q' во время пранка для остановки")
        print()
        
        choice = input("Выбери пранк: ").strip()
        
        if choice == '1':
            print("\nЗапуск заливки...")
            time.sleep(1)
            screen_flood(duration=10, speed='fast')
        elif choice == '2':
            print("\nЗапуск матрицы...")
            time.sleep(1)
            matrix_rain(duration=15)
        elif choice == '3':
            print("\nЗапуск глитча...")
            time.sleep(1)
            glitch_effect(duration=10)
        elif choice == '4':
            print("\nЗапуск тряски...")
            time.sleep(1)
            screen_shake(duration=5)
        elif choice == '5':
            char = input("Символ для заливки (Enter = случайные): ").strip()
            dur = input("Длительность в секундах (10): ").strip()
            speed = input("Скорость (slow/medium/fast/insane): ").strip()
            
            duration = int(dur) if dur.isdigit() else 10
            char = char if char else None
            speed = speed if speed in ['slow', 'medium', 'fast', 'insane'] else 'fast'
            
            print("\nЗапуск...")
            time.sleep(1)
            screen_flood(duration=duration, char=char, speed=speed)
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
