#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
МАКСИМАЛЬНО КРАСИВАЯ китайская атака для HID
Полноэкранное окно с анимированными китайскими символами
"""
import subprocess

def ultimate_chinese_attack(duration=15):
    """Самая красивая версия китайской атаки"""
    
    ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$f = New-Object System.Windows.Forms.Form
$f.BackColor = [System.Drawing.Color]::Black
$f.WindowState = 'Maximized'
$f.FormBorderStyle = 'None'
$f.TopMost = $true
$f.Cursor = [System.Windows.Forms.Cursors]::None

$panel = New-Object System.Windows.Forms.Panel
$panel.Dock = 'Fill'
$panel.BackColor = [System.Drawing.Color]::Black
$f.Controls.Add($panel)

$chinese = @("警告", "危险", "病毒", "入侵", "黑客", "攻击", "系统", "错误", "崩溃", "删除", "破坏", "感染", "数据", "丢失", "警报", "威胁", "恶意", "代码")
$labels = @()
$random = New-Object System.Random

# Создаем 100 меток для максимального эффекта
for ($i = 0; $i -lt 100; $i++) {{
    $l = New-Object System.Windows.Forms.Label
    $l.Text = $chinese[$random.Next(0, $chinese.Count)]
    $l.Font = New-Object System.Drawing.Font('SimSun', $random.Next(20, 120), [System.Drawing.FontStyle]::Bold)
    $l.ForeColor = [System.Drawing.Color]::Lime
    $l.BackColor = [System.Drawing.Color]::Black
    $l.AutoSize = $true
    $l.Left = $random.Next(-200, 2000)
    $l.Top = $random.Next(-200, 1200)
    $panel.Controls.Add($l)
    $labels += $l
}}

# Быстрая анимация (50ms)
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 50
$timer.Add_Tick({{
    foreach ($l in $labels) {{
        # Случайный китайский символ
        $l.Text = $chinese[$random.Next(0, $chinese.Count)]
        
        # Яркие красно-зеленые цвета
        $r = $random.Next(150, 255)
        $g = $random.Next(0, 100)
        $b = $random.Next(0, 50)
        $l.ForeColor = [System.Drawing.Color]::FromArgb($r, $g, $b)
        
        # Случайная позиция
        $l.Left = $random.Next(-200, [Math]::Max(1, $panel.Width - 100))
        $l.Top = $random.Next(-200, [Math]::Max(1, $panel.Height - 100))
        
        # Случайный размер шрифта
        $l.Font = New-Object System.Drawing.Font('SimSun', $random.Next(20, 120), [System.Drawing.FontStyle]::Bold)
    }}
}})
$timer.Start()

# Таймер закрытия
$closeTimer = New-Object System.Windows.Forms.Timer
$closeTimer.Interval = {duration * 1000}
$closeTimer.Add_Tick({{
    $timer.Stop()
    $f.Close()
}})
$closeTimer.Start()

# Закрытие по ESC или Q
$f.Add_KeyDown({{ 
    if ($_.KeyCode -eq 'Escape' -or $_.KeyCode -eq 'Q') {{ 
        $timer.Stop()
        $closeTimer.Stop()
        $f.Close() 
    }} 
}})

# Звуковой сигнал для эффекта
[console]::beep(800, 200)

[System.Windows.Forms.Application]::Run($f)
'''
    
    subprocess.run(['powershell', '-Command', ps_script])

if __name__ == "__main__":
    import sys
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print(f"Launching ULTIMATE Chinese Attack for {duration} seconds...")
    ultimate_chinese_attack(duration)
