#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Китайская атака - Windows РАБОТАЮЩАЯ версия
Использует msg.exe + PowerShell для гарантированного показа
"""
import subprocess
import sys
import os

def chinese_attack_windows_working(duration=15):
    """Работающая версия для Windows - комбинация msg.exe + попытка GUI"""
    
    # Вариант 1: Показываем msg.exe (ГАРАНТИРОВАННО РАБОТАЕТ)
    msg_text = "WARNING! CHINESE ATTACK! 警告 危险 病毒 入侵 黑客 攻击"
    try:
        subprocess.run(['msg', '*', msg_text], check=False, timeout=5)
        print("OK: Message shown via msg.exe")
    except:
        pass
    
    # Вариант 2: Пробуем PowerShell GUI (может не сработать через SSH)
    ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$f = New-Object System.Windows.Forms.Form
$f.BackColor = [System.Drawing.Color]::Black
$f.WindowState = 'Maximized'
$f.FormBorderStyle = 'None'
$f.TopMost = $true

$label = New-Object System.Windows.Forms.Label
$label.Text = "警告! 危险 病毒 入侵`n`nCHINESE ATTACK!`nSYSTEM COMPROMISED!"
$label.Font = New-Object System.Drawing.Font('Arial', 72, [System.Drawing.FontStyle]::Bold)
$label.ForeColor = [System.Drawing.Color]::Red
$label.BackColor = [System.Drawing.Color]::Black
$label.AutoSize = $true
$label.Left = 200
$label.Top = 300
$f.Controls.Add($label)

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = {duration * 1000}
$timer.Add_Tick({{
    $f.Close()
}})
$timer.Start()

$f.Add_KeyDown({{ 
    if ($_.KeyCode -eq 'Escape') {{ 
        $f.Close() 
    }} 
}})

[System.Windows.Forms.Application]::Run($f)
'''
    
    try:
        subprocess.Popen(['powershell', '-Command', ps_script])
        print("OK: GUI launched via PowerShell")
    except Exception as e:
        print(f"ERROR: GUI failed: {e}")
    
    return True

if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print(f"Запуск китайской атаки на {duration} секунд...")
    chinese_attack_windows_working(duration)
