import paramiko
import subprocess


class ETH_test:
    def __init__(self, logname, ETHPORT, HOSTPORT, IPMIPORT, DEFGW, ETHPORT_IP, hostname, port, username, password):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.ETHPORT = ETHPORT
        self.HOSTPORT = HOSTPORT
        self.IPMIPORT = IPMIPORT
        self.DEFGW = DEFGW
        self.ETHPORT_IP = ETHPORT_IP

    def test_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rETH test start \r")
        ETH_result = 'FAIL'
        fail_cnt = 0
        cnt = 0


        # os.system("ifconfig '%s' 192.168.217.131/24 up"%(ETHPORT))
        stdin, stdout, stderr = ssh.exec_command("ethtool %s" % self.ETHPORT)
        ethinfo = stdout.read()
        ssh.exec_command("ipmitool lan set 1 ipsrc static")
        ssh.exec_command("ipmitool lan set 1 ipaddr %s" % self.IPMIPORT)
        ssh.exec_command("ipmitool lan set 1 netmask 255.255.255.0" )
        ssh.exec_command("ipmitool lan set 1 defgw ipaddr %s" % self.DEFGW)
        ssh.exec_command("ifconfig %s %s/24 up" % (self.ETHPORT, self.ETHPORT_IP))
        with open(self.logname, 'a+') as f:
            f.write("The ETH info is:\r '%s'\r" % ethinfo.decode())
            f.write("set ipmi lan 1 ipaddr is: %s \r" % self.IPMIPORT)
            f.write("set ipmi lan 1 netmask is: 255.255.255.0 \r")
            f.write("set ipmi lan 1 defgw ipaddr is: %s \r" % self.DEFGW)
            f.write("set %s ipaddr is: %s \r" % (self.ETHPORT, self.ETHPORT_IP))

        IPMI_Info = subprocess.getoutput("ipmitool -H %s -U aaa -P joinus123 -I lanplus lan print 1" % self.IPMIPORT)
        with open(self.logname, 'a+') as f:
            f.write("The IPMI info get is:\r  '%s'\r" % IPMI_Info)

        if 'Speed: 1000Mb/s'.encode() not in ethinfo:
            # print('ETH Test fail, error code 05002')
            with open(self.logname, 'a+') as f:
                f.write("ETH Test fail, ethinfo check failed, error code 05002\r")

        elif self.IPMIPORT not in IPMI_Info:
            with open(self.logname, 'a+') as f:
                f.write("ETH Test fail, IPMI info check failed, error code 05003\r")


        else:
            while cnt< 3:
                # print('ethinfo is:', ethinfo)
                pinginfo = subprocess.getoutput("ping -c 15 %s" % self.ETHPORT_IP)
                # print('pinginfo is:', pinginfo)
                # print(pinginfo)
                with open(self.logname, 'a+') as f:
                    f.write("The '%d' ping info is:\r  '%s'\r" % (cnt+1, pinginfo))
                if (not('Link detected: yes'.encode() in ethinfo) or not('0% packet loss' in pinginfo) or
                        ('10% packet loss' in pinginfo) or ('100% packet loss' in pinginfo)):
                    fail_cnt += 1
                    cnt += 1
                else:
                    # print('Test Pass')
                    cnt += 1
            if fail_cnt < 2:
                ETH_result = 'PASS'
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
