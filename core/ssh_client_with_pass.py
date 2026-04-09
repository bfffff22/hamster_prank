#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент с сохранением пароля
Использует sshpass для автоматического ввода пароля
"""

import subprocess
import sys
import os
import getpass
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClientWithPassword:
    """SSH клиент с автоматическим вводом пароля"""
    
    # Глобальное хранилище паролей (в памяти на время сессии)
    _passwords = {}
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.connection_key = f"{user}@{host}:{port}"
        
        # Проверяем есть ли сохраненный пароль
        if not self.password and self.connection_key in SSHClientWithPassword._passwords:
            self.password = SSHClientWithPassword._passwords[self.connection_key]
    
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
            
            # Запрашиваем пароль если нет
            if not self.password:
                self.password = getpass.getpass(f"Пароль для {self.user}@{self.host}: ")
                # Сохраняем в памяти
                SSHClientWithPassword._passwords[self.connection_key] = self.password
            
            self.connected = True
            return True, "SSH доступен (пароль сохранен в памяти)"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def _build_ssh_command(self, command=None):
        """Построить SSH команду с паролем"""
        ssh_cmd = []
        
        # Используем sshpass если доступен (Linux)
        if not IS_WINDOWS:
            # Проверяем наличие sshpass
            result = subprocess.run(['which', 'sshpass'], 
                                  capture_output=True, 
                                  text=True)
            if result.returncode == 0:
                ssh_cmd = ['sshpass', '-p', self.password]
        
        ssh_cmd.append('ssh')
        
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
        
        if command:
            ssh_cmd.append(command)
        
        return ssh_cmd
    
    def execute_command(self, command):
        """Выполнение команды на удаленном хосте"""
        if not self.connected:
            return False, "Не подключен"
        
        try:
            ssh_cmd = self._build_ssh_command(command)
            
            # Для Windows используем интерактивный режим
            if IS_WINDOWS:
                # Создаем временный файл с паролем
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                    f.write(self.password + '\n')
                    pass_file = f.name
                
                try:
                    # Запускаем с перенаправлением stdin
                    with open(pass_file, 'r') as pf:
                        result = subprocess.run(ssh_cmd, 
                                              stdin=pf,
                                              capture_output=True, 
                                              text=True,
                                              timeout=30)
                finally:
                    try:
                        os.unlink(pass_file)
                    except:
                        pass
            else:
                result = subprocess.run(ssh_cmd, 
                                      capture_output=True, 
                                      text=True,
                                      timeout=30)
            
            return True, result.stdout if result.returncode == 0 else result.stderr
        
        except subprocess.TimeoutExpired:
            return False, "Таймаут выполнения команды"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def upload_file(self, local_path, remote_path):
        """Загрузка файла на удаленный хост через SCP"""
        try:
            scp_cmd = []
            
            # Используем sshpass если доступен (Linux)
            if not IS_WINDOWS:
                result = subprocess.run(['which', 'sshpass'], 
                                      capture_output=True, 
                                      text=True)
                if result.returncode == 0:
                    scp_cmd = ['sshpass', '-p', self.password]
            
            scp_cmd.append('scp')
            
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
            
            # Для Windows используем интерактивный режим
            if IS_WINDOWS:
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                    f.write(self.password + '\n')
                    pass_file = f.name
                
                try:
                    with open(pass_file, 'r') as pf:
                        result = subprocess.run(scp_cmd, stdin=pf)
                finally:
                    try:
                        os.unlink(pass_file)
                    except:
                        pass
            else:
                result = subprocess.run(scp_cmd)
            
            return result.returncode == 0, "Файл загружен" if result.returncode == 0 else "Ошибка загрузки"
        
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def open_shell(self):
        """Открыть интерактивную SSH сессию"""
        try:
            ssh_cmd = self._build_ssh_command()
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
