#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HID-эмуляция через SSH - запускает GUI локально на Windows
Эмулирует действия USB Rubber Ducky: открывает PowerShell и запускает GUI
"""
import subprocess
import time

def hid_emulation_chinese_attack(duration=15):
    """Эмулирует HID атаку - открывает PowerShell и запускает GUI"""
    
    # PowerShell команда для создания полноэкранного GUI с китайскими символами
    ps_command = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$f = New-Object System.Windows.Forms.Form
$f.BackColor = [System.Drawing.Color]::Black
$f.WindowState = 'Maximized'
$f.FormBorderStyle = 'None'
$f.TopMost = $true

$panel = New-Object System.Windows.Forms.Panel
$panel.Dock = 'Fill'
$panel.BackColor = [System.Drawing.Color]::Black
$f.Controls.Add($panel)

$chinese = @("警告", "危险", "病毒", "入侵", "黑客", "攻击", "系统", "错误", "崩溃", "删除", "破坏", "感染")
$labels = @()
$random = New-Object System.Random

for ($i = 0; $i -lt 80; $i++) {{
    $l = New-Object System.Windows.Forms.Label
    $l.Text = $chinese[$random.Next(0, $chinese.Count)]
    $l.Font = New-Object System.Drawing.Font('SimSun', $random.Next(30, 100), [System.Drawing.FontStyle]::Bold)
    $l.ForeColor = [System.Drawing.Color]::Lime
    $l.BackColor = [System.Drawing.Color]::Black
    $l.AutoSize = $true
    $l.Left = $random.Next(0, 1800)
    $l.Top = $random.Next(0, 1000)
    $panel.Controls.Add($l)
    $labels += $l
}}

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 80
$timer.Add_Tick({{
    foreach ($l in $labels) {{
        $l.Text = $chinese[$random.Next(0, $chinese.Count)]
        $l.ForeColor = [System.Drawing.Color]::FromArgb($random.Next(150, 255), $random.Next(0, 50), $random.Next(0, 50))
        $l.Left = $random.Next(0, [Math]::Max(1, $panel.Width - 200))
        $l.Top = $random.Next(0, [Math]::Max(1, $panel.Height - 200))
    }}
}})
$timer.Start()

$closeTimer = New-Object System.Windows.Forms.Timer
$closeTimer.Interval = {duration * 1000}
$closeTimer.Add_Tick({{
    $timer.Stop()
    $f.Close()
}})
$closeTimer.Start()

$f.Add_KeyDown({{ 
    if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{ 
        $timer.Stop()
        $closeTimer.Stop()
        $f.Close() 
    }} 
}})

[System.Windows.Forms.Application]::Run($f)
'''
    
    # Эмулируем HID: открываем PowerShell через Win+R и запускаем команду
    # Используем WScript.Shell для эмуляции нажатий клавиш
    vbs_script = f'''
Set WshShell = CreateObject("WScript.Shell")

' Эмулируем Win+R
WshShell.SendKeys "^{{ESC}}"
WScript.Sleep 500
WshShell.SendKeys "powershell{{ENTER}}"
WScript.Sleep 2000

' Отправляем PowerShell команду
WshShell.SendKeys "{ps_command.replace('"', '""').replace(chr(10), '')}"
WshShell.SendKeys "{{ENTER}}"
'''
    
    # Сохраняем VBS скрипт и запускаем
    import os
    vbs_path = os.path.expanduser("~/.hid_attack.vbs")
    
    with open(vbs_path, 'w', encoding='utf-8') as f:
        f.write(vbs_script)
    
    # Запускаем VBS скрипт
    subprocess.Popen(['cscript', '//nologo', vbs_path])
    
    # Удаляем VBS через несколько секунд
    time.sleep(5)
    try:
        os.remove(vbs_path)
    except:
        pass

if __name__ == "__main__":
    import sys
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print(f"Launching HID emulation attack for {duration} seconds...")
    hid_emulation_chinese_attack(duration)
