#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Китайская атака - Windows standalone версия
Запускается локально на целевой машине через HID атаку
"""
import subprocess
import sys

def chinese_attack_windows(duration=15):
    """Полноэкранная атака китайскими символами на Windows"""
    
    chinese_chars = ['警告', '危险', '病毒', '入侵', '黑客', '攻击', '系统', '错误', '崩溃', '删除', '破坏', '感染']
    
    ps_script = f'''
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

$chinese = @({', '.join(f'"{c}"' for c in chinese_chars)})
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
    
    try:
        subprocess.run(['powershell', '-Command', ps_script], check=False)
        return True
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print(f"Запуск китайской атаки на {duration} секунд...")
    chinese_attack_windows(duration)
