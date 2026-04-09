#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент с автоматическим вводом пароля
Использует subprocess.Popen с stdin для автоматического ввода
"""

import subprocess
import sys
import os
import getpass
import time
import threading
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClientSimple:
    """SSH клиент с автоматическим вводом пароля через stdin"""
    
    _passwords = {}
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.connection_key = f"{user}@{host}:{port}"
        
        if not self.password and self.connection_key in SSHClientSimple._passwords:
            self.password = SSHClientSimple._passwords[self.connection_key]
    
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
                SSHClientSimple._passwords[self.connection_key] = self.password
            
            self.connected = True
            return True, "SSH доступен (пароль сохранен)"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def _auto_input_password(self, process):
        """Автоматически вводить пароль когда запрашивается"""
        try:
            password_sent = 0
            max_attempts = 5
            
            while password_sent < max_attempts:
                # Ждем немного
                time.sleep(0.3)
                
                # Отправляем пароль
                try:
                    process.stdin.write(self.password + '\n')
                    process.stdin.flush()
                    password_sent += 1
                except:
                    break
                
                # Проверяем завершился ли процесс
                if process.poll() is not None:
                    break
        except:
            pass
    
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
                '-o', 'LogLevel=ERROR',
                '-o', 'BatchMode=no'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            ssh_cmd.append(command)
            
            # Запускаем процесс с PIPE для stdin
            process = subprocess.Popen(
                ssh_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Запускаем поток для автоматического ввода пароля
            password_thread = threading.Thread(target=self._auto_input_password, args=(process,))
            password_thread.daemon = True
            password_thread.start()
            
            # Ждем завершения
            stdout, stderr = process.communicate(timeout=30)
            
            return True, stdout if process.returncode == 0 else stderr
        
        except subprocess.TimeoutExpired:
            process.kill()
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
                '-o', 'LogLevel=ERROR',
                '-o', 'BatchMode=no'
            ])
            
            scp_cmd.append(local_path)
            
            if self.user:
                scp_cmd.append(f"{self.user}@{self.host}:{remote_path}")
            else:
                scp_cmd.append(f"{self.host}:{remote_path}")
            
            # Запускаем процесс с PIPE для stdin
            process = subprocess.Popen(
                scp_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Запускаем поток для автоматического ввода пароля
            password_thread = threading.Thread(target=self._auto_input_password, args=(process,))
            password_thread.daemon = True
            password_thread.start()
            
            # Ждем завершения
            stdout, stderr = process.communicate(timeout=30)
            
            return process.returncode == 0, "Файл загружен" if process.returncode == 0 else f"Ошибка: {stderr}"
        
        except subprocess.TimeoutExpired:
            process.kill()
            return False, "Таймаут загрузки"
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
