import subprocess
import os
from ETH_test import ETH_test
from VGA_test import VGA_test
from USB_test import USB_test
from SATA_test import SATA_test
from CPU_test import CPU_test
from Memory_test import Memory_test
from CONSOLE_test import CONSOLE_test
from PCIE_test import PCIE_test
from SSD_test import SSD_test
from SFP_test import SFP_test

HOSTPORT = '10.168.1.124'
buildoption_type='Intel(R) Xeon(R) D-2177NT CPU @ 1.90GHz'
logname = 'ft_test_log.txt'
ETHPORT = 'enp3s0'
hostname = '10.168.1.213'
IPMIPORT = '10.168.1.214'
DEFGW = '10.168.1.1'
ETHPORT_IP = '10.168.1.215'
port = 22
username = 'root'
password = '1'
SFPPORT1 = 'enp184s0f0'
SFPPORT2 = 'enp184s0f1'
SFPPORT3 = 'enp184s0f2'
SFPPORT4 = 'enp184s0f3'

# # create SSH item
# ssh = paramiko.SSHClient()
# # permit connect to remote host
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # connect
# ssh.connect(hostname='10.168.1.198', port=22, username='root', password='111111')

subprocess.getoutput("rm -f %s"%(logname))

testitem=['USB_BBU']

# testitem=['VGA_BBU','ETH_BBU','USB_BBU','SATA_BBU','M.2_BBU',
#           'SFP_BBU','CPU_BBU','MEMORY_BBU','CONSOLE_BBU','PCIE_BBU']
for item in testitem:
    if (item=='VGA_BBU'):
        VGA_result=VGA_test(logname).test_content()
        print('VGA result is %s'%(VGA_result))
    if (item=='ETH_BBU'):
        ETH_result=ETH_test(logname, ETHPORT, HOSTPORT, IPMIPORT, DEFGW, ETHPORT_IP, hostname, port, username, password).test_content()
        print('ETH result is %s'%(ETH_result))
    if (item=='USB_BBU'):
        USB_result=USB_test(logname,hostname,port,username,password).test_content()
        print('USB result is %s' % (USB_result))
    if (item=='SATA_BBU'):
        SATA_result=SATA_test(logname,hostname,port,username,password).test_content()
        print('SATA result is %s' % (SATA_result))
    if (item=='CPU_BBU'):
        CPU_result=CPU_test(logname,buildoption_type,hostname,port,username,password).test_content()
        print('CPU result is %s' % (CPU_result))
    if (item=='MEMORY_BBU'):
        Memory_result=Memory_test(logname,hostname,port,username,password).test_content()
        print('Memory result is %s' % (Memory_result))
    if (item=='CONSOLE_BBU'):
        CONSOLE_result=CONSOLE_test(logname,hostname,port,username,password).test_content()
        print('CONSOLE result is %s' % (CONSOLE_result))
    if (item=='PCIE_BBU'):
        PCIE_result=PCIE_test(logname,hostname,port,username,password).test_content()
        print('PCIE result is %s' % (PCIE_result))
    if (item=='M.2_BBU'):
        SSD_result=SSD_test(logname,hostname,port,username,password).test_content()
        print('M.2 result is %s' % (SSD_result))
        # print(SSD_result)
    if (item=='SFP_BBU'):
        SFP_result=SFP_test(logname,hostname,port,username,password,SFPPORT1,SFPPORT2,SFPPORT3,SFPPORT4).test_content()
        print('SFP result is %s' % (SFP_result))
        # print(SFP_result)

print('test finish')