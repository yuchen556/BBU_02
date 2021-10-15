import paramiko


class SFP_test:
    def __init__(self,logname,hostname,port,username,password,SFPPORT1,SFPPORT2,SFPPORT3,SFPPORT4):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.SFPPORT1 = SFPPORT1
        self.SFPPORT2 = SFPPORT2
        self.SFPPORT3 = SFPPORT3
        self.SFPPORT4 = SFPPORT4

    def test_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rSFP test start \r")
        SFP_result = 'FAIL'
        ssh.exec_command("ip netns delete net1")
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (self.SFPPORT1))
        SFPPORT1_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("\r\rSFP port1 info is: \r  '%s'\r"%(SFPPORT1_info))
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (self.SFPPORT2))
        SFPPORT2_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("\r\rSFP port2 info is: \r  '%s'\r"%(SFPPORT2_info))
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (self.SFPPORT3))
        SFPPORT3_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("\r\rSFP port3 info is: \r  '%s'\r"%(SFPPORT3_info))
        stdin, stdout, stderr = ssh.exec_command("ethtool '%s'" % (self.SFPPORT4))
        SFPPORT4_info = stdout.read()
        with open(self.logname, 'a+') as f:
            f.write("\r\rSFP port4 info is: \r  '%s'\r"%(SFPPORT4_info))

        if (not('Speed: 10000Mb/s'.encode() in SFPPORT1_info) or not('Link detected: yes'.encode() in SFPPORT1_info)):
            # print('SFP port1 Test fail, speed detect failed, error code 21001')
            with open(self.logname, 'a+') as f:
                f.write("SFP port1 Test fail, speed detect failed, error code 21001\r")
        elif (not('Speed: 10000Mb/s'.encode() in SFPPORT2_info) or not('Link detected: yes'.encode() in SFPPORT2_info)):
            # print('SFP port2 Test fail, speed detect failed, error code 21002')
            with open(self.logname, 'a+') as f:
                f.write("SFP port2 Test fail, speed detect failed, error code 21002\r")
        elif (not('Speed: 10000Mb/s'.encode() in SFPPORT3_info) or not('Link detected: yes'.encode() in SFPPORT3_info)):
            # print('SFP port3 Test fail, speed detect failed, error code 21003')
            with open(self.logname, 'a+') as f:
                f.write("SFP port3 Test fail, speed detect failed, error code 21003\r")
        elif (not('Speed: 10000Mb/s'.encode() in SFPPORT4_info) or not('Link detected: yes'.encode() in SFPPORT4_info)):
            # print('SFP port4 Test fail, speed detect failed, error code 21004')
            with open(self.logname, 'a+') as f:
                f.write("SFP port4 Test fail, speed detect failed, error code 21004\r")

        else:
            ping_port1 = '192.168.1.30'
            ping_port2 = '192.168.2.30'
            ping_port3 = '192.168.1.31'
            ping_port4 = '192.168.2.31'
            fail_cnt=0
            cnt=0
            ssh.exec_command("ip netns add net1")
            ssh.exec_command("ip link set '%s' netns net1"%(self.SFPPORT1))
            ssh.exec_command("ip link set '%s' netns net1"%(self.SFPPORT2))
            ssh.exec_command("ip netns exec net1 ifconfig '%s' 192.168.1.30/24 up"%(self.SFPPORT1))
            ssh.exec_command("ip netns exec net1 ifconfig '%s' 192.168.2.30/24 up"%(self.SFPPORT2))
            ssh.exec_command("ifconfig '%s' 192.168.1.31/24 up"%(self.SFPPORT3))
            ssh.exec_command("ifconfig '%s' 192.168.2.31/24 up"%(self.SFPPORT4))
            while (cnt<6):
                stdin, stdout, stderr = ssh.exec_command("ping -c 15 -I '%s' '%s'" % (ping_port3,ping_port1))
                upper_ping_info = stdout.read()
                with open(self.logname, 'a+') as f:
                    f.write("\r\rthe '%d' upper SFP ping info is: \r  '%s'\r"%(cnt+1,upper_ping_info))
                stdin, stdout, stderr = ssh.exec_command("ping -c 15 -I '%s' '%s'" % (ping_port4,ping_port2))
                under_ping_info = stdout.read()
                with open(self.logname, 'a+') as f:
                    f.write("\r\rthe '%d' under SFP ping info is: \r  '%s'\r"%(cnt+1,under_ping_info))
                if (not('0% packet loss'.encode() in under_ping_info) or
                        ('10% packet loss'.encode() in under_ping_info) or ('100% packet loss'.encode() in under_ping_info)):
                    fail_cnt+=1
                    cnt+=1
                elif(not('0% packet loss'.encode() in under_ping_info) or
                        ('10% packet loss'.encode() in under_ping_info) or ('100% packet loss'.encode() in under_ping_info)):
                    fail_cnt+=1
                    cnt+=1
                else:
                    # print('Test Pass')
                    cnt+=1
            if (fail_cnt < 3):
                SFP_result='PASS'
                # print('SFP Test Pass')
                with open(self.logname, 'a+') as f:
                    f.write("SFP Test Pass\r")
            else:
                # print('SFP Test fail, error code 21005')
                with open(self.logname, 'a+') as f:
                    f.write("SFP Test fail, error code 21005\r")
        # close connect
        ssh.close()
        return SFP_result