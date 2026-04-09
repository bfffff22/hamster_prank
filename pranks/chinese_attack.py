#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пранк с китайскими символами - полноэкранная атака
Аналог PowerShell версии - символы летают по всему экрану
"""

import sys
import os
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.fullscreen import FullscreenWindow

def chinese_attack_windows(duration=15):
    """Атака китайскими символами на Windows"""
    
    # Китайские символы (опасность, вирус, хакер, атака, система, ошибка и т.д.)
    chinese_chars = [
        '警告', '危险', '病毒', '入侵', '黑客', '攻击',
        '系统', '错误', '崩溃', '删除', '破坏', '感染',
        '数据', '丢失', '警报', '威胁', '恶意', '代码'
    ]
    
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
        import subprocess
        subprocess.Popen(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script])
        return True, "Китайская атака запущена!"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"


def chinese_attack_linux(duration=15):
    """Атака китайскими символами на Linux"""
    
    script = f'''#!/usr/bin/env python3
import tkinter as tk
import random
import time

chinese = ['警告', '危险', '病毒', '入侵', '黑客', '攻击', '系统', '错误', '崩溃', '删除', '破坏', '感染']

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')

labels = []
for i in range(60):
    l = tk.Label(root, text=random.choice(chinese), 
                 font=('SimSun', random.randint(30, 80), 'bold'),
                 fg='lime', bg='black')
    l.place(x=random.randint(0, 1800), y=random.randint(0, 1000))
    labels.append(l)

def update():
    for l in labels:
        r = random.randint(150, 255)
        g = random.randint(0, 50)
        b = random.randint(0, 50)
        color = '#%02x%02x%02x' % (r, g, b)
        l.config(text=random.choice(chinese), fg=color)
        l.place(x=random.randint(0, 1800), y=random.randint(0, 1000))
    root.after(80, update)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)

root.after({duration * 1000}, close)
update()
root.mainloop()
'''
    
    # Создаем и запускаем скрипт
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(script)
        script_path = f.name
    
    try:
        import subprocess
        subprocess.Popen(['python3', script_path])
        return True, "Китайская атака запущена!"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"


def chinese_attack(duration=15):
    """Универсальная китайская атака"""
    if sys.platform == 'win32':
        return chinese_attack_windows(duration)
    else:
        return chinese_attack_linux(duration)


if __name__ == "__main__":
    print("Запуск китайской атаки...")
    success, msg = chinese_attack(10)
    print(msg)
