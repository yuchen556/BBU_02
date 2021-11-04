import paramiko

class SATA_test:
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
            f.write("\r\rSATA test start \r")
        SATA_result = 'FAIL'
        stdin, stdout, stderr = ssh.exec_command("fdisk -l")
        disk_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("The disk info is:\r  '%s'\r" % disk_info.decode())
        stdin, stdout, stderr = ssh.exec_command("fdisk -l | grep '120.0 GB' | wc -l")
        SATA_number = int(stdout.read())
        if SATA_number != 2:
            # print("SATA number detect failed, the number should be 2 while only '%d' detected" % (SATA_number))
            with open(self.logname, 'a+') as f:
                f.write(
                    "SATA number detect failed, the number should be 2 while only '%d' detected, error code 03001\r"
                    % SATA_number)
        else:
            SATA_result = 'PASS'
            # print('SATA test Pass')
            with open(self.logname, 'a+') as f:
                f.write("SATA test Pass\r")

        # close connect
        ssh.close()
        return SATA_result
