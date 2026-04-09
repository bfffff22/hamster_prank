#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент без внешних зависимостей
Использует subprocess для вызова системного SSH
"""

import subprocess
import sys
import os
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClient:
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        
    def connect(self):
        """Проверка доступности SSH"""
        try:
            # Проверяем наличие ssh команды
            if IS_WINDOWS:
                result = subprocess.run(['where', 'ssh'], 
                                      capture_output=True, 
                                      text=True)
            else:
                result = subprocess.run(['which', 'ssh'], 
                                      capture_output=True, 
                                      text=True)
            
            if result.returncode != 0:
                return False, "SSH не найден в системе"
            
            self.connected = True
            return True, "SSH доступен"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def execute_command(self, command):
        """Выполнение команды на удаленном хосте"""
        if not self.connected:
            return False, "Не подключен"
        
        try:
            # Формируем SSH команду
            ssh_cmd = ['ssh']
            
            if self.port != 22:
                ssh_cmd.extend(['-p', str(self.port)])
            
            # Отключаем проверку ключа для быстрого подключения
            ssh_cmd.extend([
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null'
            ])
            
            # Добавляем user@host
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            # Добавляем команду
            ssh_cmd.append(command)
            
            # Выполняем
            result = subprocess.run(ssh_cmd, 
                                  capture_output=True, 
                                  text=True,
                                  timeout=30)
            
            return True, result.stdout if result.returncode == 0 else result.stderr
        
        except subprocess.TimeoutExpired:
            return False, "Таймаут выполнения команды"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def execute_interactive(self, command):
        """Интерактивное выполнение команды (с вводом пароля)"""
        try:
            ssh_cmd = ['ssh']
            
            if self.port != 22:
                ssh_cmd.extend(['-p', str(self.port)])
            
            ssh_cmd.extend([
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            ssh_cmd.append(command)
            
            # Запускаем интерактивно
            result = subprocess.run(ssh_cmd)
            
            return result.returncode == 0, "Выполнено"
        
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def upload_file(self, local_path, remote_path):
        """Загрузка файла на удаленный хост через SCP"""
        try:
            scp_cmd = ['scp']
            
            if self.port != 22:
                scp_cmd.extend(['-P', str(self.port)])
            
            scp_cmd.extend([
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null'
            ])
            
            scp_cmd.append(local_path)
            
            if self.user:
                scp_cmd.append(f"{self.user}@{self.host}:{remote_path}")
            else:
                scp_cmd.append(f"{self.host}:{remote_path}")
            
            result = subprocess.run(scp_cmd)
            
            return result.returncode == 0, "Файл загружен" if result.returncode == 0 else "Ошибка загрузки"
        
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def open_shell(self):
        """Открыть интерактивную SSH сессию"""
        try:
            ssh_cmd = ['ssh']
            
            if self.port != 22:
                ssh_cmd.extend(['-p', str(self.port)])
            
            ssh_cmd.extend([
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            # Открываем интерактивную сессию
            subprocess.run(ssh_cmd)
            
            return True, "Сессия завершена"
        
        except Exception as e:
            return False, f"Ошибка: {str(e)}"


def parse_ssh_string(ssh_string):
    """
    Парсинг SSH строки формата: user@host:port или host:port
    Возвращает: (host, port, user)
    """
    user = None
    port = 22
    
    # Проверяем наличие user@
    if '@' in ssh_string:
        user, ssh_string = ssh_string.split('@', 1)
    
    # Проверяем наличие :port
    if ':' in ssh_string:
        host, port_str = ssh_string.rsplit(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            host = ssh_string
    else:
        host = ssh_string
    
    return host, port, user
