#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Китайская атака - Linux standalone версия
Запускается локально на целевой машине через HID атаку
"""
import tkinter as tk
import random
import sys

def chinese_attack_linux(duration=15):
    """Полноэкранная атака китайскими символами на Linux"""
    
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
    
    root.after(duration * 1000, close)
    update()
    root.mainloop()

if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    print(f"Запуск китайской атаки на {duration} секунд...")
    chinese_attack_linux(duration)
