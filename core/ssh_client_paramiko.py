#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой SSH клиент через paramiko
"""

import sys
import os

try:
    import paramiko
except ImportError:
    print("Устанавливаю paramiko...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "paramiko"])
    import paramiko

class SSHClientSimple:
    """Простой SSH клиент через paramiko"""
    
    def __init__(self, host, port=22, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.client = None
        self.connected = False
    
    def connect(self):
        """Подключение к SSH"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            print(f"Подключаюсь к {self.user}@{self.host}:{self.port}...")
            self.client.connect(
                hostname=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                timeout=10,
                allow_agent=False,
                look_for_keys=False
            )
            
            self.connected = True
            return True, "Подключено успешно"
        except paramiko.AuthenticationException:
            return False, "Ошибка аутентификации (неверный пароль)"
        except paramiko.SSHException as e:
            return False, f"SSH ошибка: {str(e)}"
        except Exception as e:
            return False, f"Ошибка подключения: {str(e)}"
    
    def detect_remote_os(self):
        """Определить ОС на удаленной машине"""
        if not self.connected:
            return "unknown"
        
        try:
            success, output = self.execute_command("uname -s 2>/dev/null || echo Windows")
            if success and output:
                os_name = output.strip().lower()
                if "linux" in os_name:
                    return "linux"
                elif "darwin" in os_name:
                    return "macos"
                elif "windows" in os_name:
                    return "windows"
            return "linux"
        except:
            return "linux"
    
    def execute_command(self, command):
        """Выполнение команды на удаленном хосте"""
        if not self.connected or not self.client:
            return False, "Не подключен"
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=30)
            exit_status = stdout.channel.recv_exit_status()
            
            output = stdout.read().decode('utf-8', errors='replace')
            error = stderr.read().decode('utf-8', errors='replace')
            
            if exit_status == 0:
                return True, output
            else:
                return False, error if error else output
        except Exception as e:
            return False, f"Ошибка выполнения: {str(e)}"
    
    def upload_file(self, local_path, remote_path):
        """Загрузка файла на удаленный хост"""
        if not self.connected or not self.client:
            return False, "Не подключен"
        
        try:
            # Разворачиваем ~ в полный путь
            if remote_path.startswith('~'):
                success, home = self.execute_command("echo $HOME")
                if success:
                    remote_path = remote_path.replace('~', home.strip(), 1)
            
            sftp = self.client.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            
            return True, "Файл загружен"
        except Exception as e:
            return False, f"Ошибка загрузки: {str(e)}"
    
    def open_shell(self):
        """Открыть интерактивную shell сессию"""
        if not self.connected or not self.client:
            print("Не подключен")
            return
        
        try:
            channel = self.client.invoke_shell()
            
            import select
            import tty
            import termios
            
            oldtty = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                tty.setcbreak(sys.stdin.fileno())
                channel.settimeout(0.0)
                
                while True:
                    r, w, e = select.select([channel, sys.stdin], [], [])
                    if channel in r:
                        try:
                            x = channel.recv(1024)
                            if len(x) == 0:
                                break
                            sys.stdout.write(x.decode('utf-8', errors='replace'))
                            sys.stdout.flush()
                        except:
                            pass
                    if sys.stdin in r:
                        x = sys.stdin.read(1)
                        if len(x) == 0:
                            break
                        channel.send(x)
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        except Exception as e:
            print(f"Ошибка shell: {e}")
    
    def close(self):
        """Закрыть соединение"""
        if self.client:
            self.client.close()
            self.connected = False

def parse_ssh_string(ssh_string):
    """Парсинг строки user@host:port"""
    user = None
    host = ssh_string
    port = 22
    
    if '@' in ssh_string:
        user, host = ssh_string.split('@', 1)
    
    if ':' in host:
        host, port_str = host.rsplit(':', 1)
        try:
            port = int(port_str)
        except:
            pass
    
    return host, port, user

# Алиас для совместимости
SSHClientExpect = SSHClientSimple
