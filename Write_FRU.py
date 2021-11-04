import paramiko
import re


class write_FRU:
    def __init__(self, logname, BMD, BMT, BSN, BPN, PSN, PPN, ProductN, ProductV, hostname, port, username, password):
        self.logname = logname
        self.BMD = BMD
        self.BMT = BMT
        self.BSN = BSN
        self.BPN = BPN
        self.PSN = PSN
        self.PPN = PPN
        self.ProductN = ProductN
        self.ProductV = ProductV
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def write_content(self):

        # create SSH item
        ssh = paramiko.SSHClient()
        # permit connect to remote host
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # connect
        ssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)

        with open(self.logname, 'a+') as f:
            f.write("\r\rstart write fru message\r")

        write_result = 'FAIL'
        stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x02 0x00")
        stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x03 0x00")
        stdin, stdout, stderr = ssh.exec_command("ipmitool fru write 0 /root/projects/bbu_server01/fru_test.bin")
        write_fru = stdout.read()
        if 'Size to Write    : 432 bytes'.encode() not in write_fru:
            stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x02 0x01")
            stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x03 0x01")
            with open(self.logname, 'a+') as f:
                f.write("write fru_test.bin failed\r")
        else:
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh BMD %s %s"
                                                     % (self.BMD, self.BMT))
            write_BMD = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh BSN %s" % self.BSN)
            write_BSN = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh BPN %s" % self.BPN)
            write_BPN = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh PSN %s" % self.PSN)
            write_PSN = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh PPN %s" % self.PPN)
            write_PPN = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh PN %s" % self.ProductN)
            write_PN = stdout.read()
            stdin, stdout, stderr = ssh.exec_command("sh /root/projects/bbu_server01/fru.sh PV %s" % self.ProductV)
            write_PV = stdout.read()
            with open(self.logname, 'a+') as f:
                f.write("Write Board Mfg Date result is %s\r" % write_BMD)
                f.write("Write Board Serial result is %s\r" % write_BMD)
                f.write("Write Board Part number result is %s\r" % write_BMD)
                f.write("Write Product Serial result is %s\r" % write_BMD)
                f.write("Write Product Part number result is %s\r" % write_BMD)
                f.write("Write Product Name result is %s\r" % write_BMD)
                f.write("Write Product Version result is %s\r" % write_BMD)

            stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x02 0x01")
            stdin, stdout, stderr = ssh.exec_command("ipmitool raw 0x2e 0x49 0xa 0x40 0x00 0x00 0x03 0x01")

            stdin, stdout, stderr = ssh.exec_command("ipmitool fru")
            fru_info = stdout.read()
            with open(self.logname, 'a+') as f:
                f.write("Read FRU info is:\r %s\r" % fru_info.decode())
            message = re.split('\n'.encode(), fru_info)

            def search_fru(str):
                for line in message:
                    content = line.split(':'.encode(), 1)
                    # print('%s in board is %s' % (content[0], content[1].strip()))
                    if str.encode() in content[0]:
                        return content[1]

            BMD_read = search_fru('Board Mfg Date').decode().strip()
            BSN_read = search_fru('Board Serial').decode().strip()
            BPN_read = search_fru('Board Part Number').decode().strip()
            PSN_read = search_fru('Product Serial').decode().strip()
            PPN_read = search_fru('Product Part Number').decode().strip()
            PN_read = search_fru('Product Name').decode().strip()
            PV_read = search_fru('Product Version').decode().strip()

            if 'fail'.encode() in write_BMD or 'error'.encode() in write_BMD or 'fail'.encode() in write_BSN or \
                    'fail'.encode() in write_BPN or 'fail'.encode() in write_PSN or 'fail'.encode() in write_PPN or \
                    'fail'.encode() in write_PN or 'fail'.encode() in write_PV or 'error'.encode() in write_PV:
                with open(self.logname, 'a+') as f:
                    f.write("Fru info writen to board failed\r")
            elif BSN_read != self.BSN:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Board Serial number check failed\r")
            elif BPN_read != self.BPN:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Board Part number check failed\r")
            elif PSN_read != self.PSN:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Product Serial number check failed\r")
            elif PPN_read != self.PPN:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Product Part number check failed\r")
            elif PN_read != self.ProductN:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Product name check failed\r")
            elif PV_read != self.ProductV:
                with open(self.logname, 'a+') as f:
                    f.write("Error, Product version check failed\r")
            else:
                write_result = 'PASS'
                with open(self.logname, 'a+') as f:
                    f.write("Write fru info successfully\r")

        return write_result
