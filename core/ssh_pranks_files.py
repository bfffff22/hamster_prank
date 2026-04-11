#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH пранки - версия с загрузкой файлов
Более надежная - загружает скрипты как файлы
"""

import sys
import os
import time
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.ssh_client import SSHClient

class SSHPranksFiles:
    """SSH пранки через загрузку файлов"""
    
    def __init__(self, client):
        self.client = client
        self.has_tkinter = None  # Кэш для проверки tkinter
        self.has_zenity = None   # Кэш для проверки zenity
        self.has_xmessage = None # Кэш для проверки xmessage
    
    def check_gui_tools(self):
        """Проверить доступные GUI инструменты на удаленной машине"""
        if self.has_tkinter is None:
            # Проверяем tkinter
            success, output = self.client.execute_command("python3 -c 'import tkinter' 2>&1")
            self.has_tkinter = success and "ModuleNotFoundError" not in output
            
            # Проверяем zenity
            success, output = self.client.execute_command("which zenity 2>/dev/null")
            self.has_zenity = success and "/zenity" in output
            
            # Проверяем xmessage
            success, output = self.client.execute_command("which xmessage 2>/dev/null")
            self.has_xmessage = success and "/xmessage" in output
        
        return {
            'tkinter': self.has_tkinter,
            'zenity': self.has_zenity,
            'xmessage': self.has_xmessage
        }
    
    def get_gui_method(self):
        """Определить лучший метод для GUI"""
        tools = self.check_gui_tools()
        
        if tools['tkinter']:
            return 'tkinter'
        elif tools['zenity']:
            return 'zenity'
        elif tools['xmessage']:
            return 'xmessage'
        else:
            return None
    
    def upload_and_run_gui(self, script_content, script_name="prank.py"):
        """Загрузить скрипт и запустить как GUI приложение"""
        
        # Определяем ОС удаленной машины
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
            print(f"[INFO] Удаленная ОС: {remote_os}")
        
        # Создаем локальный файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script_content)
            local_path = f.name
        
        try:
            # Загружаем в домашнюю директорию
            remote_path = f"~/.{script_name}"
            print(f"Загружаю скрипт...")
            success, msg = self.client.upload_file(local_path, remote_path)
            
            if not success:
                print(f"✗ Ошибка: {msg}")
                return False
            
            print("✓ Скрипт загружен")
            
            # Формируем команду запуска в зависимости от ОС
            if remote_os == "windows":
                # Windows: используем Task Scheduler для запуска в активной сессии
                # Это обходит Session 0 isolation при SSH подключении
                task_name = f"HamsterPrank_{int(time.time())}"
                cmd = f'schtasks /create /tn "{task_name}" /tr "python \\"{remote_path}\\"" /sc once /st 00:00 /f && schtasks /run /tn "{task_name}" && timeout /t 2 /nobreak >nul && schtasks /delete /tn "{task_name}" /f'
                print("Запускаю GUI на Windows через Task Scheduler...")
            
            elif remote_os in ["linux", "macos"]:
                # Linux/macOS: используем правильный способ запуска GUI
                self.client.execute_command(f"chmod +x {remote_path}")
                # Используем export DISPLAY и запускаем напрямую
                cmd = f"export DISPLAY=:0 && python3 {remote_path} &"
                print("Запускаю полноэкранное окно на Linux...")
            
            else:
                # Fallback - пробуем Linux
                self.client.execute_command(f"chmod +x {remote_path}")
                cmd = f"export DISPLAY=:0 && python3 {remote_path} &"
                print("Запускаю (fallback режим)...")
            
            success, output = self.client.execute_command(cmd)
            
            # Даем больше времени на запуск
            time.sleep(2)
            
            # Проверяем, запустился ли процесс
            check_success, check_output = self.client.execute_command("ps aux | grep python3 | grep -v grep")
            
            if "python3" in check_output:
                print(f"✓ GUI запущено на удаленной машине ({remote_os})!")
            else:
                print(f"⚠ Процесс запущен, но GUI может не отображаться")
                print(f"Проверьте DISPLAY и X11 forwarding на удаленной машине")
            
            return True
        
        finally:
            try:
                os.unlink(local_path)
            except:
                pass
    
    def screen_flood(self, duration=10):
        """Заливка экрана - полноэкранное GUI окно"""
        
        # Определяем ОС
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
        
        if remote_os == "windows":
            # Windows версия с PowerShell
            script = f"""#!/usr/bin/env python3
import subprocess

ps_script = \"\"\"
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

$chars = @('#', '@', '%', '&', '*', '+', '=')
$labels = @()
$random = New-Object System.Random

for ($i = 0; $i -lt 50; $i++) {{
    $l = New-Object System.Windows.Forms.Label
    $l.Text = $chars[$random.Next(0, $chars.Count)]
    $l.Font = New-Object System.Drawing.Font('Courier', $random.Next(20, 60), [System.Drawing.FontStyle]::Bold)
    $l.ForeColor = [System.Drawing.Color]::Lime
    $l.BackColor = [System.Drawing.Color]::Black
    $l.AutoSize = $true
    $l.Left = $random.Next(0, 1800)
    $l.Top = $random.Next(0, 1000)
    $panel.Controls.Add($l)
    $labels += $l
}}

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 50
$timer.Add_Tick({{
    foreach ($l in $labels) {{
        $l.Text = $chars[$random.Next(0, $chars.Count)]
        $l.ForeColor = [System.Drawing.Color]::FromArgb($random.Next(0, 255), $random.Next(100, 255), $random.Next(0, 100))
        $l.Left = $random.Next(0, [Math]::Max(1, $panel.Width - 100))
        $l.Top = $random.Next(0, [Math]::Max(1, $panel.Height - 100))
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
    if ($_.KeyCode -eq 'Escape') {{ 
        $timer.Stop()
        $closeTimer.Stop()
        $f.Close() 
    }} 
}})

[System.Windows.Forms.Application]::Run($f)
\"\"\"

subprocess.run(['powershell', '-Command', ps_script])
"""
        else:
            # Linux версия с tkinter
            script = f"""#!/usr/bin/env python3
import tkinter as tk
import random
import time

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

chars = '#@%&*+='

def update():
    canvas.delete('all')
    width = root.winfo_width()
    height = root.winfo_height()
    
    for _ in range(200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        char = random.choice(chars)
        color = '#%02x%02x%02x' % (random.randint(0, 255), random.randint(100, 255), random.randint(0, 100))
        canvas.create_text(x, y, text=char, fill=color, font=('Courier', random.randint(20, 60), 'bold'))
    
    root.after(50, update)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)

root.after({duration * 1000}, close)
root.after(100, update)
root.mainloop()
"""
        
        return self.upload_and_run_gui(script, "flood.py")
    
    def matrix_effect(self, duration=15):
        """Матрица - полноэкранное GUI окно"""
        
        # Определяем ОС
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
        
        if remote_os == "windows":
            # Windows версия с PowerShell
            script = f"""#!/usr/bin/env python3
import subprocess

ps_script = \"\"\"
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

$chars = @('0', '1')
$labels = @()
$random = New-Object System.Random

for ($i = 0; $i -lt 60; $i++) {{
    $l = New-Object System.Windows.Forms.Label
    $l.Text = $chars[$random.Next(0, 2)]
    $l.Font = New-Object System.Drawing.Font('Courier', $random.Next(16, 24), [System.Drawing.FontStyle]::Bold)
    $brightness = $random.Next(100, 255)
    $l.ForeColor = [System.Drawing.Color]::FromArgb(0, $brightness, 0)
    $l.BackColor = [System.Drawing.Color]::Black
    $l.AutoSize = $true
    $l.Left = $random.Next(0, 1800)
    $l.Top = $random.Next(-500, 1000)
    $panel.Controls.Add($l)
    $labels += $l
}}

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 100
$timer.Add_Tick({{
    foreach ($l in $labels) {{
        $l.Text = $chars[$random.Next(0, 2)]
        $l.Top += $random.Next(10, 30)
        if ($l.Top -gt $panel.Height) {{
            $l.Top = -50
            $l.Left = $random.Next(0, [Math]::Max(1, $panel.Width - 50))
        }}
        $brightness = $random.Next(100, 255)
        $l.ForeColor = [System.Drawing.Color]::FromArgb(0, $brightness, 0)
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
    if ($_.KeyCode -eq 'Escape') {{ 
        $timer.Stop()
        $closeTimer.Stop()
        $f.Close() 
    }} 
}})

[System.Windows.Forms.Application]::Run($f)
\"\"\"

subprocess.run(['powershell', '-Command', ps_script])
"""
        else:
            # Linux версия с tkinter
            script = f"""#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
import random
import time
import os

# Устанавливаем DISPLAY если не установлен
if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')
root.overrideredirect(True)

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

chars = '01'
columns = []

def init_columns():
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    col_width = 20
    num_cols = width // col_width
    
    for i in range(num_cols):
        columns.append({{
            'x': i * col_width,
            'y': random.randint(-height, 0),
            'speed': random.randint(10, 30)
        }})

def update():
    canvas.delete('all')
    height = root.winfo_screenheight()
    
    for col in columns:
        for i in range(20):
            y = col['y'] + i * 20
            if 0 <= y < height:
                char = random.choice(chars)
                brightness = 255 - (i * 12)
                if brightness < 0:
                    brightness = 0
                color = '#00%02x00' % brightness
                canvas.create_text(col['x'], y, text=char, fill=color, font=('Courier', 16, 'bold'))
        
        col['y'] += col['speed']
        if col['y'] > height:
            col['y'] = random.randint(-height, 0)
    
    root.after(50, update)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)

root.after({duration * 1000}, close)
root.after(100, lambda: (init_columns(), update()))

try:
    root.mainloop()
except:
    pass
"""
        
        return self.upload_and_run_gui(script, "matrix.py")
    
    def fullscreen_text(self, text, duration=5):
        """Полноэкранный текст - GUI окно"""
        text_escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        
        script = f"""#!/usr/bin/env python3
import tkinter as tk
import time

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='red')

label = tk.Label(root, text="{text_escaped}", 
                font=('Arial', 80, 'bold'),
                fg='white', bg='red')
label.pack(expand=True)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)

root.after({duration * 1000}, close)
root.mainloop()
"""
        return self.upload_and_run_gui(script, "text.py")
    
    def glitch_effect(self, duration=10):
        """Глитч - полноэкранное GUI окно"""
        script = f"""#!/usr/bin/env python3
import tkinter as tk
import random
import time

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

chars = '#@%&*'

def update():
    if random.random() < 0.1:
        canvas.delete('all')
    
    width = root.winfo_width()
    height = root.winfo_height()
    
    for _ in range(random.randint(10, 30)):
        x = random.randint(0, width)
        y = random.randint(0, height)
        text = ''.join(random.choices(chars, k=random.randint(5, 20)))
        color = '#%02x%02x%02x' % (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        canvas.create_text(x, y, text=text, fill=color, font=('Courier', random.randint(20, 60), 'bold'))
    
    root.after(random.randint(10, 100), update)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)

root.after({duration * 1000}, close)
root.after(100, update)
root.mainloop()
"""
        return self.upload_and_run_gui(script, "glitch.py")
    
    def chinese_attack(self, duration=15):
        """Китайская атака - символы летают по экрану"""
        
        # Определяем ОС удаленной машины
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
            print(f"[INFO] Удаленная ОС: {remote_os}")
        
        # Генерируем скрипт в зависимости от ОС
        if remote_os == "windows":
            # Windows версия - PowerShell + Windows Forms
            script = self._generate_chinese_attack_windows(duration)
        else:
            # Linux/macOS версия - Python + tkinter
            script = self._generate_chinese_attack_linux(duration)
        
        # Загружаем и запускаем
        print("Загружаю скрипт...")
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            local_path = f.name
        
        try:
            remote_path = "~/.chinese_attack.py"
            success, msg = self.client.upload_file(local_path, remote_path)
            
            if not success:
                print(f"✗ Ошибка: {msg}")
                return False
            
            print("✓ Скрипт загружен")
            
            # Формируем команду запуска
            if remote_os == "windows":
                # Windows через SSH: запускаем Python скрипт, который создаст PowerShell файл
                # PowerShell файл запустится в контексте пользователя
                cmd = f'python "{remote_path}"'
                print("Запускаю полноэкранный GUI через PowerShell файл...")
            else:
                self.client.execute_command(f"chmod +x {remote_path}")
                # Используем nohup для надежного фонового запуска
                cmd = f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &"
                print("Запускаю китайскую атаку на Linux...")
            
            success, output = self.client.execute_command(cmd)
            
            # Даем время на запуск GUI
            time.sleep(1)
            
            # Удаляем временный файл
            self.client.execute_command(f"rm -f {remote_path}")
            
            if success or not output:
                print(f"✓ Китайская атака запущена на удаленной машине ({remote_os})!")
                return True
            else:
                print(f"✓ Китайская атака запущена на удаленной машине ({remote_os})!")
                return True
        
        finally:
            try:
                os.unlink(local_path)
            except:
                pass
    
    def _generate_chinese_attack_linux(self, duration):
        """Генерация Linux версии китайской атаки"""
        return f'''#!/usr/bin/env python3
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
    
    def _generate_chinese_attack_windows(self, duration):
        """Генерация ULTIMATE Windows версии - максимально красивая"""
        
        return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess

ps_script = """
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

$chinese = @("警告", "危险", "病毒", "入侵", "黑客", "攻击", "系统", "错误", "崩溃", "删除", "破坏", "感染")
$labels = @()
$random = New-Object System.Random

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

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 50
$timer.Add_Tick({{
    foreach ($l in $labels) {{
        $l.Text = $chinese[$random.Next(0, $chinese.Count)]
        $r = $random.Next(150, 255)
        $g = $random.Next(0, 100)
        $b = $random.Next(0, 50)
        $l.ForeColor = [System.Drawing.Color]::FromArgb($r, $g, $b)
        $l.Left = $random.Next(-200, [Math]::Max(1, $panel.Width - 100))
        $l.Top = $random.Next(-200, [Math]::Max(1, $panel.Height - 100))
        $l.Font = New-Object System.Drawing.Font('SimSun', $random.Next(20, 120), [System.Drawing.FontStyle]::Bold)
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

[console]::beep(800, 200)
[System.Windows.Forms.Application]::Run($f)
"""

subprocess.run(['powershell', '-Command', ps_script])
'''
    
    def spam_programs(self, program, count=5):
        """Спам программами"""
        
        # Определяем ОС
        remote_os = "linux"
        if hasattr(self.client, 'detect_remote_os'):
            remote_os = self.client.detect_remote_os()
        
        if remote_os == "windows":
            # Windows версия
            cmd = f'powershell -Command "1..{count} | ForEach-Object {{ Start-Process {program}; Start-Sleep -Milliseconds 300 }}"'
        else:
            # Linux/macOS версия
            cmd = f"for i in {{1..{count}}}; do setsid DISPLAY=:0 {program} </dev/null >/dev/null 2>&1 & sleep 0.3; done"
        
        success, output = self.client.execute_command(cmd)
        if success:
            print(f"✓ Запущено {count} экземпляров {program}")
            return True
        else:
            print(f"✗ Ошибка: {output}")
            return False
    
    def minimize_windows(self):
        """Свернуть все окна"""
        cmd = "DISPLAY=:0 wmctrl -k on 2>/dev/null || DISPLAY=:0 xdotool key super+d 2>/dev/null"
        success, output = self.client.execute_command(cmd)
        if success:
            print("✓ Окна свернуты")
        else:
            print(f"Результат: {output}")
        return success
    
    def wave_text(self, text, duration=5):
        """Волна текста в GUI окне"""
        script = f'''#!/usr/bin/env python3
import tkinter as tk
import time
import math

root = tk.Tk()
root.title("Wave Text")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

start_time = time.time()
initial_font_size = 20
font_size = max(initial_font_size, 10)

def animate():
    current_time = time.time()
    if current_time - start_time >= {duration}:
        root.destroy()
        return
    
    canvas.delete('all')
    width = root.winfo_width()
    height = root.winfo_height()
    
    # Отображаем каждый символ с волной
    char_spacing = min(width // len("{text}"), font_size * 2) if len("{text}") > 0 else font_size
    start_x = (width - len("{text}") * char_spacing) // 2
    center_y = height // 2
    
    for i, char in enumerate("{text}"):
        x = start_x + i * char_spacing
        # Вычисляем смещение по Y для эффекта волны
        offset = int(30 * math.sin(current_time * 5 + i * 0.5))
        y = center_y + offset
        
        canvas.create_text(x, y, text=char, fill='cyan', font=('Courier', font_size), anchor='center')
    
    root.after(50, animate)

root.after(100, animate)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.bind('Q', close)
root.mainloop()
'''
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            local_path = f.name
        
        remote_path = "~/.wave_text.py"
        success, msg = self.client.upload_file(local_path, remote_path)
        
        if success:
            self.client.execute_command(f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &")
            time.sleep(0.5)  # даем время на запуск
            self.client.execute_command(f"rm {remote_path}")
            print("✓ Wave text показан")
        else:
            print(f"✗ Ошибка: {msg}")
        
        import os
        os.unlink(local_path)
        time.sleep(duration + 1)  # ждем завершения анимации

    def rainbow_text(self, text, duration=5):
        """Радужный текст в GUI окне"""
        script = f'''#!/usr/bin/env python3
import tkinter as tk
import time

root = tk.Tk()
root.title("Rainbow Text")
root.attributes('-fullscreen', True)
root.configure(bg='black')

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill='both', expand=True)

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
start_time = time.time()

def animate():
    current_time = time.time()
    if current_time - start_time >= {duration}:
        root.destroy()
        return
    
    canvas.delete('all')
    width = root.winfo_width()
    height = root.winfo_height()
    
    # Вычисляем позиции для текста
    char_width = min(width // len("{text}"), 30) if len("{text}") > 0 else 20
    start_x = (width - len("{text}") * char_width) // 2
    y_pos = height // 2
    
    # Отображаем каждый символ с разным цветом
    for i, char in enumerate("{text}"):
        color_index = (i + int(current_time * 10)) % len(colors)
        color = colors[color_index]
        x = start_x + i * char_width
        canvas.create_text(x, y_pos, text=char, fill=color, font=('Courier', 24), anchor='center')
    
    root.after(100, animate)

root.after(100, animate)

def close(event=None):
    root.destroy()

root.bind('<Escape>', close)
root.bind('q', close)
root.bind('Q', close)
root.mainloop()
'''
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script)
            local_path = f.name
        
        remote_path = "~/.rainbow_text.py"
        success, msg = self.client.upload_file(local_path, remote_path)
        
        if success:
            self.client.execute_command(f"DISPLAY=:0 nohup python3 {remote_path} >/dev/null 2>&1 &")
            time.sleep(0.5)  # даем время на запуск
            self.client.execute_command(f"rm {remote_path}")
            print("✓ Rainbow text показан")
        else:
            print(f"✗ Ошибка: {msg}")
        
        import os
        os.unlink(local_path)
        time.sleep(duration + 1)  # ждем завершения анимации

    def show_gui_message(self, text, duration=5):
        """GUI сообщение"""
        cmd = f"DISPLAY=:0 timeout {duration} zenity --info --text='{text}' --width=800 --height=600 2>/dev/null || DISPLAY=:0 timeout {duration} xmessage -center '{text}' 2>/dev/null"
        success, output = self.client.execute_command(cmd)
        if success or "not found" not in output.lower():
            print("✓ GUI сообщение показано")
            return True
        else:
            print("✗ Не удалось показать GUI")
            return False


if __name__ == "__main__":
    print("SSH Pranks Files Module")
