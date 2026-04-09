#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент с автоматическим вводом пароля через pexpect
Без внешних зависимостей - используем встроенные возможности
"""

import subprocess
import sys
import os
import getpass
import tempfile
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClientAuto:
    """SSH клиент с автоматическим вводом пароля"""
    
    _passwords = {}
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.connection_key = f"{user}@{host}:{port}"
        
        if not self.password and self.connection_key in SSHClientAuto._passwords:
            self.password = SSHClientAuto._passwords[self.connection_key]
    
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
                SSHClientAuto._passwords[self.connection_key] = self.password
            
            self.connected = True
            return True, "SSH доступен (пароль сохранен)"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def _run_with_password(self, cmd_list, input_data=None):
        """Запустить команду с автоматическим вводом пароля"""
        try:
            # Создаем скрипт который будет вводить пароль
            if IS_WINDOWS:
                # Для Windows используем PowerShell скрипт
                ps_script = f'''
$password = ConvertTo-SecureString "{self.password}" -AsPlainText -Force
$process = Start-Process -FilePath "{cmd_list[0]}" -ArgumentList {','.join(f'"{arg}"' for arg in cmd_list[1:])} -NoNewWindow -PassThru -Wait
'''
                # Простой способ - используем echo для передачи пароля
                echo_cmd = f'echo {self.password}'
                full_cmd = f'{echo_cmd} | {" ".join(cmd_list)}'
                
                result = subprocess.run(
                    full_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result
            else:
                # Для Linux используем expect-подобный подход
                # Создаем временный скрипт expect
                expect_script = f'''#!/usr/bin/expect -f
set timeout 30
spawn {" ".join(cmd_list)}
expect {{
    "password:" {{
        send "{self.password}\\r"
        exp_continue
    }}
    "Password:" {{
        send "{self.password}\\r"
        exp_continue
    }}
    eof
}}
'''
                with tempfile.NamedTemporaryFile(mode='w', suffix='.exp', delete=False) as f:
                    f.write(expect_script)
                    expect_file = f.name
                
                try:
                    os.chmod(expect_file, 0o755)
                    result = subprocess.run(
                        ['expect', expect_file],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    return result
                finally:
                    try:
                        os.unlink(expect_file)
                    except:
                        pass
        except Exception as e:
            # Fallback - обычный запуск
            result = subprocess.run(cmd_list, capture_output=True, text=True, timeout=30)
            return result
    
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
                '-o', 'NumberOfPasswordPrompts=1'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            ssh_cmd.append(command)
            
            result = self._run_with_password(ssh_cmd)
            
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
                '-o', 'LogLevel=ERROR',
                '-o', 'NumberOfPasswordPrompts=1'
            ])
            
            scp_cmd.append(local_path)
            
            if self.user:
                scp_cmd.append(f"{self.user}@{self.host}:{remote_path}")
            else:
                scp_cmd.append(f"{self.host}:{remote_path}")
            
            result = self._run_with_password(scp_cmd)
            
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
