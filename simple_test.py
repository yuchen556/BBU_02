import re

SN = '123456cb89121'
pattern = re.compile(r'[a-z]')

a = pattern.findall(SN)
print (a)

if ((len(SN) != 13) or a):
    print('test fail')
else:
    print('test pass')