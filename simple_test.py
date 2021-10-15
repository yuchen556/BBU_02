import subprocess

a = subprocess.getoutput('ls -l /dev/ttyUSB*')
print(a)