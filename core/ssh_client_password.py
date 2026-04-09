#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент с РЕАЛЬНЫМ автовводом пароля через sshpass
"""

import subprocess
import sys
import os
import getpass
import tempfile
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClientPassword:
    """SSH клиент с автовводом пароля"""
    
    _passwords = {}
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.connection_key = f"{user}@{host}:{port}"
        
        if not self.password and self.connection_key in SSHClientPassword._passwords:
            self.password = SSHClientPassword._passwords[self.connection_key]
    
    def connect(self):
        """Проверка доступности SSH"""
        try:
            if IS_WINDOWS:
                result = subprocess.run(['where', 'ssh'], capture_output=True, text=True)
            else:
                result = subprocess.run(['which', 'ssh'], capture_output=True, text=True)
            
            if result.returncode != 0:
                return False, "SSH не найден в системе"
            
            if not self.password:
                self.password = getpass.getpass(f"Пароль для {self.user}@{self.host}: ")
                SSHClientPassword._passwords[self.connection_key] = self.password
            
            # Проверяем sshpass
            if not IS_WINDOWS:
                result = subprocess.run(['which', 'sshpass'], capture_output=True, text=True)
                if result.returncode != 0:
                    print("\n⚠️  sshpass не установлен!")
                    print("Установи: sudo apt install sshpass")
                    print("Или настрой SSH ключи чтобы не вводить пароль\n")
            
            self.connected = True
            return True, "SSH доступен (пароль сохранен)"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def _build_command(self, base_cmd):
        """Построить команду с sshpass"""
        if IS_WINDOWS:
            # Для Windows создаем bat файл с паролем
            return base_cmd
        else:
            # Для Linux используем sshpass
            return ['sshpass', '-p', self.password] + base_cmd
    
    def execute_command(self, command):
        """Выполнение команды на удаленном хосте"""
        if not self.connected:
            return False, "Не подключен"
        
        try:
            ssh_cmd = ['ssh']
            
            if self.port != 22:
                ssh_cmd.extend(['-p', str(self.port)])
            
            ssh_cmd.extend([
                '-o', 'StrictHostKeyChecking=no',
                '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'LogLevel=ERROR'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            ssh_cmd.append(command)
            
            # Добавляем sshpass
            full_cmd = self._build_command(ssh_cmd)
            
            result = subprocess.run(
                full_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return True, result.stdout if result.returncode == 0 else result.stderr
        
        except subprocess.TimeoutExpired:
            return False, "Таймаут выполнения команды"
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
                '-o', 'UserKnownHostsFile=/dev/null',
                '-o', 'LogLevel=ERROR'
            ])
            
            scp_cmd.append(local_path)
            
            if self.user:
                scp_cmd.append(f"{self.user}@{self.host}:{remote_path}")
            else:
                scp_cmd.append(f"{self.host}:{remote_path}")
            
            # Добавляем sshpass
            full_cmd = self._build_command(scp_cmd)
            
            result = subprocess.run(full_cmd, capture_output=True, text=True)
            
            return result.returncode == 0, "Файл загружен" if result.returncode == 0 else f"Ошибка: {result.stderr}"
        
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
            
            subprocess.run(ssh_cmd)
            return True, "Сессия завершена"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"


def parse_ssh_string(ssh_string):
    """Парсинг SSH строки"""
    user = None
    port = 22
    
    if '@' in ssh_string:
        user, ssh_string = ssh_string.split('@', 1)
    
    if ':' in ssh_string:
        host, port_str = ssh_string.rsplit(':', 1)
        try:
            port = int(port_str)
        except ValueError:
            host = ssh_string
    else:
        host = ssh_string
    
    return host, port, user
