#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль автообновления main.py из GitHub
"""

import urllib.request
import hashlib
import os
from pathlib import Path

GITHUB_RAW_URL = "https://raw.githubusercontent.com/bfffff22/hamster_prank/master/main.py"

def get_file_hash(filepath):
    """Получить MD5 хеш файла"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def check_and_update():
    """Проверить и обновить main.py если нужно"""
    try:
        main_path = Path(__file__).parent.parent / "main.py"
        
        # Получаем текущий хеш
        current_hash = get_file_hash(main_path)
        
        # Скачиваем новую версию
        print("Проверка обновлений...")
        req = urllib.request.Request(GITHUB_RAW_URL)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            new_content = response.read()
        
        # Проверяем хеш новой версии
        new_hash = hashlib.md5(new_content).hexdigest()
        
        if current_hash != new_hash:
            print("✓ Найдено обновление! Обновляю main.py...")
            
            # Создаем бэкап
            backup_path = main_path.with_suffix('.py.bak')
            if main_path.exists():
                with open(main_path, 'rb') as f:
                    with open(backup_path, 'wb') as bf:
                        bf.write(f.read())
            
            # Записываем новую версию
            with open(main_path, 'wb') as f:
                f.write(new_content)
            
            print("✓ main.py обновлен! Перезапустите программу.")
            return True
        else:
            print("✓ У вас последняя версия")
            return False
            
    except Exception as e:
        print(f"Не удалось проверить обновления: {e}")
        return False

if __name__ == "__main__":
    check_and_update()
