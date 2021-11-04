import paramiko
import re

# create SSH item
ssh = paramiko.SSHClient()
# permit connect to remote host
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect
ssh.connect(hostname='10.168.1.213', port=22, username='root', password='1')

stdin, stdout, stderr = ssh.exec_command("ipmitool fru")
fru_info = stdout.read()
message = re.split('\n'.encode(), fru_info)

def search_fru(str):
    for line in message:
        content = line.split(':'.encode(), 1)
        # print('%s in board is %s' % (content[0], content[1].strip()))
        if str.encode() in content[0]:
            return content[1]

BMD_read = search_fru('Board Mfg Date').strip()