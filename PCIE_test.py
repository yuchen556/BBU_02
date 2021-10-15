import paramiko

class PCIE_test:
    def __init__(self,logname,hostname,port,username,password):
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
            f.write("\r\rPCIE test start \r")
        PCIE_result='FAIL'
        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep I210")
        pcie_Ethernet_info=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep AST1150")
        pcie_chip_info=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep AMD")
        pcie_external_graphic_card=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci | grep AMD | wc -l")
        pcie_external_graphic_card_num=int(stdout.read())

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 02:00.0 -vvv | grep Width")
        pcie_Ethernet_value=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 03:00.0 -vvv | grep Width")
        pcie_chip_value=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 17:00.0 -vvv | grep Width")
        pcie_1st_external_card_value=stdout.read()

        stdin, stdout, stderr = ssh.exec_command("/sbin/lspci -s 65:00.0 -vvv | grep Width")
        pcie_2nd_external_card_value=stdout.read()

        # print('pcie_num is:',pcie_num)
        # print('pcieX1Seepvalue is:',pcieX1SeepValue)
        # print('pcieX4Seepvalue is:', pcieX4SeepValue)
        with open(self.logname, 'a+') as f:
            f.write("PCIE Ethernet info is:\r  '%s'\rPCIE chip info is:\r  '%s'\rpcie external graphic card is:\r  '%s'\rPCIEX Ethernet Value is:\r  '%s'\rPCIE chip value is:\r"
                    "  '%s'\rpcie 1st external card value is:\r  '%s'\rpcie 2nd external card value is:\r  '%s'\r"
                    %(pcie_Ethernet_info,pcie_chip_info,pcie_external_graphic_card,pcie_Ethernet_value,pcie_chip_value,pcie_1st_external_card_value,pcie_2nd_external_card_value))
        if ('I210'.encode() not in pcie_Ethernet_info):
            # print('Pcie Test failed, detected no Ethernet devices, error coed is 13001')
            with open(self.logname, 'a+') as f:
                f.write("Pcie Test failed, detected no Ethernet devices, error coed is 13001\r")
        elif ('AST1150'.encode() not in pcie_chip_info):
            # print('Pcie Test failed, detect no chip device, error coed is 13002')
            with open(self.logname, 'a+') as f:
                f.write("Pcie Test failed, detect no chip device, error coed is 13002\r")
        elif ('AMD'.encode() not in pcie_external_graphic_card):
            # print('Pcie Test failed, detect external graphic card failed, error coed is 13003')
            with open(self.logname, 'a+') as f:
                f.write("Pcie Test failed, detect no external graphic card failed, error coed is 13003\r")
        elif (pcie_external_graphic_card_num != 4):
            with open(self.logname, 'a+') as f:
                f.write("Pcie Test failed, external graphic card number wrong, error coed is 13003\r")
        else:
            PCIE_result='PASS'
            # print('Pcie Test Pass')
            with open(self.logname, 'a+') as f:
                f.write("Pcie Test Pass\r")

        # close connect
        ssh.close()
        return PCIE_result