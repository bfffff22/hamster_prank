#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для работы с терминалом и экраном
Кроссплатформенный вывод текста, очистка, управление курсором
"""

import sys
import os
import time
import shutil

IS_WINDOWS = sys.platform == 'win32'

if IS_WINDOWS:
    try:
        import ctypes
        from ctypes import wintypes
        import msvcrt
        WINDOWS_CONSOLE = True
    except ImportError:
        WINDOWS_CONSOLE = False
else:
    import termios
    import tty
    import select

class Display:
    """Класс для работы с терминалом"""
    
    def __init__(self):
        self.width, self.height = self.get_terminal_size()
    
    @staticmethod
    def get_terminal_size():
        """Получить размер терминала"""
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except:
            return 80, 24
    
    @staticmethod
    def clear():
        """Очистить экран"""
        os.system('cls' if IS_WINDOWS else 'clear')
    
    @staticmethod
    def hide_cursor():
        """Скрыть курсор"""
        if IS_WINDOWS:
            if WINDOWS_CONSOLE:
                try:
                    class CONSOLE_CURSOR_INFO(ctypes.Structure):
                        _fields_ = [("dwSize", wintypes.DWORD),
                                    ("bVisible", wintypes.BOOL)]
                    
                    ci = CONSOLE_CURSOR_INFO()
                    handle = ctypes.windll.kernel32.GetStdHandle(-11)
                    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
                    ci.bVisible = False
                    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
                except:
                    pass
        else:
            sys.stdout.write('\033[?25l')
            sys.stdout.flush()
    
    @staticmethod
    def show_cursor():
        """Показать курсор"""
        if IS_WINDOWS:
            if WINDOWS_CONSOLE:
                try:
                    class CONSOLE_CURSOR_INFO(ctypes.Structure):
                        _fields_ = [("dwSize", wintypes.DWORD),
                                    ("bVisible", wintypes.BOOL)]
                    
                    ci = CONSOLE_CURSOR_INFO()
                    handle = ctypes.windll.kernel32.GetStdHandle(-11)
                    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
                    ci.bVisible = True
                    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))
                except:
                    pass
        else:
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()
    
    @staticmethod
    def move_cursor(x, y):
        """Переместить курсор в позицию (x, y)"""
        if IS_WINDOWS:
            if WINDOWS_CONSOLE:
                try:
                    class COORD(ctypes.Structure):
                        _fields_ = [("X", ctypes.c_short),
                                    ("Y", ctypes.c_short)]
                    
                    handle = ctypes.windll.kernel32.GetStdHandle(-11)
                    coord = COORD(x, y)
                    ctypes.windll.kernel32.SetConsoleCursorPosition(handle, coord)
                except:
                    # Fallback to ANSI escape codes
                    sys.stdout.write(f'\033[{y};{x}H')
                    sys.stdout.flush()
        else:
            sys.stdout.write(f'\033[{y};{x}H')
            sys.stdout.flush()
    
    @staticmethod
    def print_at(x, y, text):
        """Вывести текст в позиции (x, y)"""
        Display.move_cursor(x, y)
        sys.stdout.write(text)
        sys.stdout.flush()
    
    @staticmethod
    def fill_screen(char=' ', color=None):
        """Заполнить экран символом"""
        width, height = Display.get_terminal_size()
        Display.clear()
        
        for y in range(height):
            sys.stdout.write(char * width)
        
        sys.stdout.flush()
    
    @staticmethod
    def print_centered(text, y=None):
        """Вывести текст по центру экрана"""
        width, height = Display.get_terminal_size()
        
        if y is None:
            y = height // 2
        
        x = (width - len(text)) // 2
        Display.print_at(x, y, text)
    
    @staticmethod
    def print_box(text, padding=2):
        """Вывести текст в рамке по центру"""
        width, height = Display.get_terminal_size()
        
        lines = text.split('\n')
        max_len = max(len(line) for line in lines)
        
        box_width = max_len + padding * 2 + 2
        box_height = len(lines) + padding * 2 + 2
        
        start_x = (width - box_width) // 2
        start_y = (height - box_height) // 2
        
        # Верхняя граница
        Display.print_at(start_x, start_y, '╔' + '═' * (box_width - 2) + '╗')
        
        # Пустые строки сверху
        for i in range(padding):
            Display.print_at(start_x, start_y + 1 + i, '║' + ' ' * (box_width - 2) + '║')
        
        # Текст
        for i, line in enumerate(lines):
            content = ' ' * padding + line.ljust(max_len) + ' ' * padding
            Display.print_at(start_x, start_y + padding + 1 + i, '║' + content + '║')
        
        # Пустые строки снизу
        for i in range(padding):
            Display.print_at(start_x, start_y + padding + len(lines) + 1 + i, '║' + ' ' * (box_width - 2) + '║')
        
        # Нижняя граница
        Display.print_at(start_x, start_y + box_height - 1, '╚' + '═' * (box_width - 2) + '╝')
        
        sys.stdout.flush()
    
    @staticmethod
    def animate_text(text, delay=0.05):
        """Анимированный вывод текста"""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
    
    @staticmethod
    def get_key():
        """Получить нажатую клавишу (неблокирующий ввод)"""
        if IS_WINDOWS:
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8', errors='ignore')
            return None
        else:
            dr, dw, de = select.select([sys.stdin], [], [], 0)
            if dr:
                return sys.stdin.read(1)
            return None
    
    @staticmethod
    def wait_key():
        """Ждать нажатия клавиши"""
        if IS_WINDOWS:
            return msvcrt.getch().decode('utf-8', errors='ignore')
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def test_display():
    """Тест функций дисплея"""
    display = Display()
    
    print(f"Размер терминала: {display.width}x{display.height}")
    time.sleep(1)
    
    display.clear()
    display.print_centered("Тест центрированного текста")
    time.sleep(2)
    
    display.clear()
    display.print_box("Привет!\nЭто текст\nв рамке")
    time.sleep(2)
    
    display.clear()
    display.animate_text("Анимированный текст...\n")
    time.sleep(1)


if __name__ == "__main__":
    test_display()
