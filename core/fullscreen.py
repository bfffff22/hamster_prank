#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для полноэкранных окон
Создает реальные GUI окна на весь экран, а не только в консоли
"""

import sys
import os
import time
import random
import subprocess
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')

class FullscreenWindow:
    """Класс для создания полноэкранных окон"""
    
    @staticmethod
    def create_fullscreen_text(text, duration=5, bg_color="black", fg_color="red"):
        """
        Создать полноэкранное окно с текстом
        
        Args:
            text: Текст для показа
            duration: Длительность в секундах
            bg_color: Цвет фона
            fg_color: Цвет текста
        """
        if IS_WINDOWS:
            return FullscreenWindow._windows_fullscreen_text(text, duration, bg_color, fg_color)
        elif IS_LINUX:
            return FullscreenWindow._linux_fullscreen_text(text, duration, bg_color, fg_color)
    
    @staticmethod
    def _windows_fullscreen_text(text, duration, bg_color, fg_color):
        """Windows: Полноэкранное окно через PowerShell"""
        
        # Экранируем текст для PowerShell
        text_escaped = text.replace('"', '`"').replace("'", "''")
        
        ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.FormBorderStyle = 'None'
$form.WindowState = 'Maximized'
$form.TopMost = $true
$form.BackColor = [System.Drawing.Color]::{bg_color}

$label = New-Object System.Windows.Forms.Label
$label.Text = "{text_escaped}"
$label.Font = New-Object System.Drawing.Font("Arial", 72, [System.Drawing.FontStyle]::Bold)
$label.ForeColor = [System.Drawing.Color]::{fg_color}
$label.AutoSize = $false
$label.Dock = 'Fill'
$label.TextAlign = 'MiddleCenter'

$form.Controls.Add($label)

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = {duration * 1000}
$timer.Add_Tick({{
    $form.Close()
}})
$timer.Start()

$form.Add_KeyDown({{
    if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{
        $form.Close()
    }}
}})

$form.ShowDialog()
'''
        
        try:
            subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script])
            return True, "Окно запущено"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    @staticmethod
    def _linux_fullscreen_text(text, duration, bg_color, fg_color):
        """Linux: Полноэкранное окно через zenity или xmessage"""
        
        # Пробуем zenity
        try:
            cmd = [
                'zenity', '--info',
                '--text', text,
                '--width', '800',
                '--height', '600',
                '--timeout', str(duration)
            ]
            subprocess.Popen(cmd)
            return True, "Окно запущено (zenity)"
        except FileNotFoundError:
            pass
        
        # Пробуем xmessage
        try:
            cmd = ['xmessage', '-center', '-timeout', str(duration), text]
            subprocess.Popen(cmd)
            return True, "Окно запущено (xmessage)"
        except FileNotFoundError:
            pass
        
        # Fallback: терминал на весь экран
        try:
            terminal_cmd = None
            if os.path.exists('/usr/bin/gnome-terminal'):
                terminal_cmd = ['gnome-terminal', '--full-screen', '--', 'bash', '-c', 
                               f'echo "{text}"; sleep {duration}']
            elif os.path.exists('/usr/bin/xterm'):
                terminal_cmd = ['xterm', '-fullscreen', '-e', 
                               f'echo "{text}"; sleep {duration}']
            
            if terminal_cmd:
                subprocess.Popen(terminal_cmd)
                return True, "Окно запущено (terminal)"
        except:
            pass
        
        return False, "Не удалось создать окно"
    
    @staticmethod
    def create_fullscreen_flood(duration=10, char=None):
        """Полноэкранная заливка символами"""
        
        if IS_WINDOWS:
            chars = char if char else '█▓▒░'
            flood_text = chars * 1000
            
            ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.FormBorderStyle = 'None'
$form.WindowState = 'Maximized'
$form.TopMost = $true
$form.BackColor = [System.Drawing.Color]::Black

$textBox = New-Object System.Windows.Forms.TextBox
$textBox.Multiline = $true
$textBox.Dock = 'Fill'
$textBox.BackColor = [System.Drawing.Color]::Black
$textBox.ForeColor = [System.Drawing.Color]::Lime
$textBox.Font = New-Object System.Drawing.Font("Consolas", 12)
$textBox.ReadOnly = $true

$form.Controls.Add($textBox)

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 100
$timer.Add_Tick({{
    $chars = "█▓▒░!@#$%^&*()"
    $random = Get-Random -Minimum 0 -Maximum $chars.Length
    $textBox.AppendText($chars[$random])
    if ($textBox.Text.Length -gt 10000) {{
        $textBox.Clear()
    }}
}})
$timer.Start()

$closeTimer = New-Object System.Windows.Forms.Timer
$closeTimer.Interval = {duration * 1000}
$closeTimer.Add_Tick({{
    $form.Close()
}})
$closeTimer.Start()

$form.Add_KeyDown({{
    if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{
        $form.Close()
    }}
}})

$form.ShowDialog()
'''
            
            try:
                subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script])
                return True, "Заливка запущена"
            except Exception as e:
                return False, f"Ошибка: {str(e)}"
        
        elif IS_LINUX:
            # Для Linux используем терминал на весь экран
            try:
                script_path = Path(__file__).parent.parent / "pranks" / "screen_flood.py"
                cmd = ['gnome-terminal', '--full-screen', '--', 'python3', str(script_path)]
                subprocess.Popen(cmd)
                return True, "Заливка запущена"
            except:
                return False, "Не удалось запустить"
    
    @staticmethod
    def create_image_fullscreen(image_path, duration=5):
        """Показать картинку на весь экран"""
        
        if IS_WINDOWS:
            ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.FormBorderStyle = 'None'
$form.WindowState = 'Maximized'
$form.TopMost = $true
$form.BackColor = [System.Drawing.Color]::Black

$pictureBox = New-Object System.Windows.Forms.PictureBox
$pictureBox.Dock = 'Fill'
$pictureBox.SizeMode = 'Zoom'
$pictureBox.Image = [System.Drawing.Image]::FromFile("{image_path}")

$form.Controls.Add($pictureBox)

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = {duration * 1000}
$timer.Add_Tick({{
    $form.Close()
}})
$timer.Start()

$form.Add_KeyDown({{
    if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{
        $form.Close()
    }}
}})

$form.ShowDialog()
'''
            
            try:
                subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script])
                return True, "Картинка показана"
            except Exception as e:
                return False, f"Ошибка: {str(e)}"
        
        elif IS_LINUX:
            try:
                subprocess.Popen(['feh', '--fullscreen', '--auto-zoom', image_path])
                time.sleep(duration)
                subprocess.run(['pkill', 'feh'])
                return True, "Картинка показана"
            except:
                return False, "Не удалось показать (установи feh)"


if __name__ == "__main__":
    # Тест
    print("Тест полноэкранного окна...")
    FullscreenWindow.create_fullscreen_text("ТЕСТОВОЕ СООБЩЕНИЕ!", duration=3)
