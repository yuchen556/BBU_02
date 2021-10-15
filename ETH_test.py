import paramiko


class ETH_test:
    def __init__(self, logname, ETHPORT, HOSTPORT, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ETHPORT = ETHPORT
        self.HOSTPORT = HOSTPORT

    def test_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rETH test start \r")
        ETH_result='FAIL'
        fail_cnt=0
        cnt=0
        # os.system("ifconfig '%s' 192.168.217.131/24 up"%(ETHPORT))
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (self.ETHPORT))
        ethinfo = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("The ETH info is:\r  '%s'\r" % (ethinfo))
        if (not('Speed: 1000Mb/s'.encode() in ethinfo)):
            # print('ETH Test fail, error code 05002')
            with open(self.logname, 'a+') as f:
                f.write("ETH Test fail, ethinfo check failed, error code 05002\r")
        else:
            while (cnt<6):
                # print('ethinfo is:', ethinfo)
                stdin, stdout, stderr = ssh.exec_command("ping -c 15 -I '%s' '%s'" % (self.ETHPORT, self.HOSTPORT))
                pinginfo = stdout.read()
                ping_err = stderr.read()
                # print('pinginfo is:', pinginfo)
                # print(pinginfo)
                with open(self.logname, 'a+') as f:
                    f.write("The '%d' ping info is:\r  '%s'\r" % (cnt+1,pinginfo))
                if (not('Link detected: yes'.encode() in ethinfo) or not('0% packet loss'.encode() in pinginfo) or
                        ('10% packet loss'.encode() in pinginfo) or ('100% packet loss'.encode() in pinginfo)):
                    fail_cnt += 1
                    cnt += 1
                else:
                    # print('Test Pass')
                    cnt += 1
            if (fail_cnt < 3):
                ETH_result='PASS'
                # print('ETH Test Pass')
                with open(self.logname, 'a+') as f:
                    f.write("ETH Test Pass\r")
            else:
                # print('ETH Test fail, error code 05001')
                with open(self.logname, 'a+') as f:
                    f.write("ETH Test fail, error code 05001\r")

        # close connect
        ssh.close()
        return ETH_result