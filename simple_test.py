import paramiko
import re
import time

# create SSH item
ssh = paramiko.SSHClient()
# permit connect to remote host
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# connect
ssh.connect(hostname='10.168.1.213', port=22, username='root', password='1')


MAC_address = ['E4956E2F222A','E4956E2F222B','E4956E2F222C','E4956E2F222D','E4956E2F222E','E4956E2F2228','E4956E2F2229']
# MAC_address2 = ['E4956E2F2001','E4956E2F2002']
MAC_number = ['', '', '', '', '']

def mysplit(str):
    t = str.upper()
    p = re.compile('.{1,2}')
    return ' '.join(p.findall(t))
a1 = mysplit(MAC_address[5]).strip()
b1 = a1.split()
a2 = mysplit(MAC_address[6]).strip()
b2 = a2.split()
# print(a1)
# print(a2)
# print(b1[0], b2[0])
i = 0
j = 0

stdin, stdout, stderr = ssh.exec_command("projects/bbu_server01/LAN_BBU/eeupdate64e /ALL /MAC_DUMP | grep MAC")
mac_info = stdout.read().decode()
print("MAC info before write is:\r %s" % mac_info)

while (i < 5):
    stdin, stdout, stderr = ssh.exec_command("projects/bbu_server01/LAN_BBU/eeupdate64e /NIC=%d /MAC=%s " % (i+1, MAC_address[i]) )
    write_info = stdout.read().decode()
    # print(write_info)
    i += 1
while (j < 5):

    stdin2, stdout, stderr2 = ssh.exec_command("projects/bbu_server01/LAN_BBU/eeupdate64e /NIC=%d /MAC_DUMP | grep MAC" % (j+1))
    mac_info_later = stdout.read().decode().strip()
    print("MAC info after write is:\r %s" % mac_info_later)
    MAC_number[j] = mac_info_later[-13:-1]
    print('Get MAC number %d is: %s' % (j+1,MAC_number[j]))
    j +=1

stdin3, stdout, stderr3 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x00")
mac_info_ipmi_lan1 = stdout.read().decode().strip()
print("BMC LAN1 initial MAC address is: %s" % mac_info_ipmi_lan1)
stdin4, stdout, stderr4 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x08")
mac_info_ipmi_lan8 = stdout.read().decode().strip()
print("BMC LAN8 initial MAC address is: %s" % mac_info_ipmi_lan8)

stdin5, stdout, stderr5 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x0 0x1c 0x00 0x%s 0x%s 0x%s 0x%s 0x%s 0x%s" %(b1[0], b1[1], b1[2], b1[3], b1[4], b1[5]))
write_bmc_lan1_info = stdout
stdin6, stdout, stderr6 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x0 0x1c 0x08 0x%s 0x%s 0x%s 0x%s 0x%s 0x%s" %(b2[0], b2[1], b2[2], b2[3], b2[4], b2[5]))
write_bmc_lan8_info = stdout

stdin7, stdout, stderr7 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x00")
mac_info_ipmi_lan1_later = stdout.read().decode().strip().upper()
print("BMC LAN1 final MAC address is: %s" % mac_info_ipmi_lan1_later)
stdin8, stdout, stderr8 = ssh.exec_command("ipmitool i2c bus=0 0xa0 0x06 0x1c 0x08")
mac_info_ipmi_lan8_later = stdout.read().decode().strip().upper()
print("BMC LAN8 final MAC address is: %s" % mac_info_ipmi_lan8_later)


if (mac_info_ipmi_lan1_later != a1):
    print('write bmc lan1 failed')
elif (mac_info_ipmi_lan8_later != a2):
    print('write bmc lan 8 failed')
elif (MAC_number[0] != MAC_address[0]):
    print('First ETH MAC_address write failed')
elif (MAC_number[1] != MAC_address[1]):
    print('Second ETH MAC_address write failed')
elif (MAC_number[2] != MAC_address[2]):
    print('Third ETH MAC_address write failed')
elif (MAC_number[3] != MAC_address[3]):
    print('Fouth ETH MAC_address write failed')
elif (MAC_number[4] != MAC_address[4]):
    print('Fifth ETH MAC_address write failed')
else:
    print('write bmc lan success')
    print('Write ETH MAC addrss success')

# close connect
ssh.close()


