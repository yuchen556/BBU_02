import paramiko
import re

class write_Mac:
    def __init__(self, logname, hostname, port, username, password, mac_address):
        self.logname = logname
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.mac_address = (mac_address[0][1], mac_address[1][1], mac_address[2][1], mac_address[3][1],
                            mac_address[4][1], mac_address[5][1], mac_address[6][1],)

    def test_content(self):
        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rstart write mac address \r")

        MAC_number = ['', '', '', '', '']
        write_result = 'FAIL'

        # 将MAC地址分割成两个一组
        def mysplit(str):
            t = str.upper()
            p = re.compile('.{1,2}')
            return ' '.join(p.findall(str))

        a1 = mysplit(self.mac_address[5]).strip()
        b1 = a1.split()
        a2 = mysplit(self.mac_address[6]).strip()
        b2 = a2.split()
        # print(a1)
        # print(a2)
        # print(b1[0], b2[0])
        i = 0
        j = 0


        # 获取现有MAC地址
        stdin, stdout, stderr = ssh.exec_command("projects/bbu_server01/LAN_BBU/eeupdate64e /ALL /MAC_DUMP | grep MAC")
        mac_info = stdout.read().decode()
        with open(self.logname, 'a+') as f:
            f.write("MAC info before write is:\r %s\r" % mac_info)
        # print("MAC info before write is:\r %s" % mac_info)

        # 依次写入MAC地址
        while (i < 5):
            stdin, stdout, stderr = ssh.exec_command(
                "/root/projects/bbu_server01/LAN_BBU/eeupdate64e /NIC=%d /MAC=%s " % (i + 1, self.mac_address[i]))
            write_info = stdout.read().decode()
            with open(self.logname, 'a+') as f:
                f.write("The %d channel write result is %s\r" % (i+1, write_info))
            # print(write_info)
            i += 1

        # 获取写入后的MAC地址
        while (j < 5):
            stdin2, stdout, stderr2 = ssh.exec_command(
                "/root/projects/bbu_server01/LAN_BBU/eeupdate64e /NIC=%d /MAC_DUMP | grep MAC" % (j + 1))
            mac_info_later = stdout.read().decode().strip()
            with open(self.logname, 'a+') as f:
                f.write("MAC info after write is:\r %s\r" % mac_info_later)
            # print("MAC info after write is:\r %s" % mac_info_later)
            MAC_number[j] = mac_info_later[-13:-1]
            with open(self.logname, 'a+') as f:
                f.write("Get MAC number %d is: \r%s\r" % (j + 1, MAC_number[j]))
            # print('Get MAC number %d is: %s' % (j + 1, MAC_number[j]))
            j += 1


        # 获取现有BMC MAC地址
        stdin3, stdout, stderr3 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x00")
        mac_info_ipmi_lan1 = stdout.read().decode().strip()
        # print("BMC LAN1 initial MAC address is: %s" % mac_info_ipmi_lan1)
        with open(self.logname, 'a+') as f:
            f.write("BMC LAN1 initial MAC address is:\r %s\r" % mac_info_ipmi_lan1)
        stdin4, stdout, stderr4 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x08")
        mac_info_ipmi_lan8 = stdout.read().decode().strip()
        # print("BMC LAN8 initial MAC address is: %s" % mac_info_ipmi_lan8)
        with open(self.logname, 'a+') as f:
            f.write("BMC LAN8 initial MAC address is:\r %s\r" % mac_info_ipmi_lan8)


        # 依次写入BMC MAC地址
        stdin5, stdout, stderr5 = ssh.exec_command(
            "ipmitool i2c bus=0 0xa0 0x0 0x1c 0x00 0x%s 0x%s 0x%s 0x%s 0x%s 0x%s"
            % (b1[0], b1[1], b1[2], b1[3], b1[4], b1[5]))
        write_bmc_lan1_info = stdout.read()
        stdin6, stdout, stderr6 = ssh.exec_command(
            "ipmitool i2c bus=0 0xa0 0x0 0x1c 0x08 0x%s 0x%s 0x%s 0x%s 0x%s 0x%s"
            % (b2[0], b2[1], b2[2], b2[3], b2[4], b2[5]))
        write_bmc_lan8_info = stdout.read()

        # 读取写完后的BMC MAC地址
        stdin7, stdout, stderr7 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x00")
        mac_info_ipmi_lan1_later = stdout.read().decode().strip().upper()
        # print("BMC LAN1 final MAC address is: %s" % mac_info_ipmi_lan1_later)
        with open(self.logname, 'a+') as f:
            f.write("BMC LAN1 final MAC address is:\r %s\r" % mac_info_ipmi_lan1_later)
        stdin8, stdout, stderr8 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x08")
        mac_info_ipmi_lan8_later = stdout.read().decode().strip().upper()
        # print("BMC LAN8 final MAC address is: %s" % mac_info_ipmi_lan8_later)
        with open(self.logname, 'a+') as f:
            f.write("BMC LAN8 final MAC address is:\r %s\r" % mac_info_ipmi_lan8_later)

        # 判断MAC地址是否正确
        if mac_info_ipmi_lan1_later != a1:
            with open(self.logname, 'a+') as f:
                f.write('write bmc lan1 failed\r')
        elif mac_info_ipmi_lan8_later != a2:
            with open(self.logname, 'a+') as f:
                f.write('write bmc lan 8 failed\r')
        elif MAC_number[0] != self.mac_address[0]:
            with open(self.logname, 'a+') as f:
                f.write('first ETH MAC_address write failed\r')
        elif MAC_number[1] != self.mac_address[1]:
            with open(self.logname, 'a+') as f:
                f.write('second ETH MAC_address write failed\r')
        elif MAC_number[2] != self.mac_address[2]:
            with open(self.logname, 'a+') as f:
                f.write('third ETH MAC_address write failed\r')
        elif MAC_number[3] != self.mac_address[3]:
            with open(self.logname, 'a+') as f:
                f.write('fourth ETH MAC_address write failed\r')
        elif MAC_number[4] != self.mac_address[4]:
            with open(self.logname, 'a+') as f:
                f.write('fifth ETH MAC_address write failed\r')
        else:
            with open(self.logname, 'a+') as f:
                f.write('write bmc lan success\r')
                f.write('write ETH MAC address success\r')
            write_result = 'PASS'

        # close connect
        ssh.close()
        return write_result
