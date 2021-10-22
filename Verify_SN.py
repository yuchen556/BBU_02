import re

class Verify_SN:
    def __init__(self, Serial_number):
        self.SN = Serial_number

    def test_content(self):
        Verify_SN_Result = 'PASS'
        pattern = re.compile(r'[a-z]')
        a = pattern.findall(self.SN)
        if ((len(self.SN) != 13) or a):
            Verify_SN_Result = 'FAIL'

        return Verify_SN_Result

class Verify_MAC:
    def __init__(self,MAC_address):
        self.MAC = MAC_address

    def test_content(self):
        Verify_MAC_Result = 'PASS'
        pattern = re.compile(r'[0-9a-fA-F]')
        a = pattern.findall(self.MAC)
        if (len(self.MAC) != 12 and a):
            Verify_MAC_Result = 'FAIL'

        return Verify_MAC_Result