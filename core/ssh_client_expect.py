#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSH клиент с автовводом пароля через expect скрипт
БЕЗ sudo, БЕЗ sshpass, БЕЗ внешних зависимостей
"""

import subprocess
import sys
import os
import tempfile
from pathlib import Path

IS_WINDOWS = sys.platform == 'win32'

class SSHClientExpect:
    """SSH клиент с автовводом пароля через expect"""
    
    _passwords = {}
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.connected = False
        self.connection_key = f"{user}@{host}:{port}"
        
        if not self.password and self.connection_key in SSHClientExpect._passwords:
            self.password = SSHClientExpect._passwords[self.connection_key]
    
    def connect(self):
        """Проверка доступности SSH"""
        try:
            if IS_WINDOWS:
                result = subprocess.run(['where', 'ssh'], capture_output=True, text=True)
            else:
                result = subprocess.run(['which', 'ssh'], capture_output=True, text=True)
            
            if result.returncode != 0:
                return False, "SSH не найден в системе"
            
            # Пароль должен быть передан при создании объекта или уже сохранен
            if not self.password:
                return False, "Пароль не указан. Используйте ключи SSH или передайте пароль при создании клиента."
            
            self.connected = True
            return True, "SSH доступен (пароль сохранен)"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def detect_remote_os(self):
        """Определить ОС на удаленной машине"""
        if not self.connected:
            return "unknown"
        
        try:
            # Метод 1: uname (Linux/macOS)
            success, output = self.execute_command("uname -s 2>/dev/null")
            if success and output and output.strip():
                os_name = output.strip().lower()
                if "linux" in os_name:
                    return "linux"
                elif "darwin" in os_name:
                    return "macos"
            
            # Метод 2: проверка переменной окружения (Windows)
            success, output = self.execute_command("echo %OS% 2>nul")
            if success and output and "windows" in output.lower():
                return "windows"
            
            # Метод 3: PowerShell (Windows)
            success, output = self.execute_command("powershell -Command \"$PSVersionTable.PSVersion.Major\" 2>nul")
            if success and output and output.strip().isdigit():
                return "windows"
            
            # Fallback - предполагаем Linux
            return "linux"
        except:
            return "linux"
    
    def _create_expect_script(self, command_list):
        """Создать expect скрипт для автоввода пароля"""
        cmd_str = ' '.join(f'"{c}"' if ' ' in c else c for c in command_list)
        
        expect_script = f'''#!/usr/bin/expect -f
set timeout 60
spawn {cmd_str}
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
        return expect_script
    
    def _run_with_expect(self, command_list):
        """Запустить команду с expect для автоввода пароля"""
        # Создаем временный expect скрипт
        with tempfile.NamedTemporaryFile(mode='w', suffix='.exp', delete=False) as f:
            f.write(self._create_expect_script(command_list))
            expect_file = f.name
        
        try:
            os.chmod(expect_file, 0o755)
            
            # Запускаем expect скрипт
            result = subprocess.run(
                ['expect', expect_file],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )
            
            return result
        finally:
            try:
                os.unlink(expect_file)
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
                '-o', 'LogLevel=ERROR'
            ])
            
            if self.user:
                ssh_cmd.append(f"{self.user}@{self.host}")
            else:
                ssh_cmd.append(self.host)
            
            ssh_cmd.append(command)
            
            # Запускаем с expect
            result = self._run_with_expect(ssh_cmd)
            
            return True, result.stdout if result.returncode == 0 else result.stderr
        
        except subprocess.TimeoutExpired:
            return False, "Таймаут выполнения команды"
        except FileNotFoundError:
            # expect не установлен - используем обычный способ
            return self._fallback_execute(ssh_cmd)
        except Exception as e:
            return False, f"Ошибка: {str(e)}"
    
    def _fallback_execute(self, ssh_cmd):
        """Запасной вариант без expect"""
        try:
            result = subprocess.run(
                ssh_cmd,
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace'
            )
            return True, result.stdout if result.returncode == 0 else result.stderr
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
            
            # Для Windows используем обычный SCP (будет спрашивать пароль)
            # Для Linux используем expect
            if IS_WINDOWS:
                result = subprocess.run(scp_cmd, capture_output=True, text=True)
                return result.returncode == 0, "Файл загружен" if result.returncode == 0 else f"Ошибка: {result.stderr}"
            else:
                # Запускаем с expect на Linux
                result = self._run_with_expect(scp_cmd)
                return result.returncode == 0, "Файл загружен" if result.returncode == 0 else f"Ошибка: {result.stderr}"
        
        except FileNotFoundError:
            # expect не установлен - используем обычный способ
            result = subprocess.run(scp_cmd, capture_output=True, text=True)
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
