import paramiko

class SSD_test:
    def __init__(self, logname, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def test_content(self):
        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rM.2 test start \r")
        SSD_result = 'FAIL'

        stdin, stdout, stderr = ssh.exec_command("fdisk -l")
        disk_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("The disk info is:\r  '%s'\r" % disk_info.decode())
        stdin, stdout, stderr = ssh.exec_command("fdisk -l | grep '512.1 GB' | wc -l")
        disk_number1 = int(stdout.read())
        stdin, stdout, stderr = ssh.exec_command("fdisk -l | grep '1024.2 GB' | wc -l")
        disk_number2 = int(stdout.read())
        disk_number = disk_number1 + disk_number2
        if disk_number != 2:
            # print("M.2 disk number detect failed, the number should be 2 while only '%d' detected"%(disk_number))
            with open(self.logname, 'a+') as f:
                f.write("M.2 disk number detect failed, the number should be 2 while only '%d' detected, "
                        "error code 20001\r" % disk_number)
        else:
            SSD_result = 'PASS'
            # print('M.2 test Pass')
            with open(self.logname, 'a+') as f:
                f.write("M.2 test Pass\r")

        # close connect
        ssh.close()
        return SSD_result
