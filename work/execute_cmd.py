import threading
import paramiko
import sys


class Execute_cmd(object):

    def __init__(self, ip, port, username, password):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def ssh_conn(self, cmd):
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)

        if not stdout:
            result = stderr.read().decode()
        else:
            result = stdout.read().decode() + stderr.read().decode()
        result_json = {"ip": self.ip, "result": result}
        ssh.close()
        return result_json


class Command_Run(object):

    def cmd_run(self, cmd, ip, port, username, password):
        client = Execute_cmd(ip, port, username, password)
        result = client.ssh_conn(cmd)
        return result

    def config_file(self, filename):
        host_list = []
        with open(filename, 'r') as host_server:
            for line in host_server:
                line_list = line.split(' ')
                host = {"ip": line_list[0], "port": int(line_list[1]), "username": line_list[2], "password": line_list[3]}
                host_list.append(host)
        return host_list
