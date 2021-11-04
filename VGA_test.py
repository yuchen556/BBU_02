import paramiko
import easygui as gui


class VGA_test:
    def __init__(self,logname):
        self.logname = logname

    def test_content(self):
        with open(self.logname, 'a+') as f:
            f.write("\r\rVGA test start \r")
        VGA_result=gui.ccbox(msg='please check the vga screen display is light', title='VGA_check', choices=(['light', 'not light']))
        if (VGA_result):
            VGA_result= 'PASS'
            # print('The user choose light, VGA Test Pass')
            with open(self.logname, 'a+') as f:
                f.write("The user choose light, VGA Test Pass\r")
            return VGA_result
        else:
            VGA_result= 'FAIL'
            # print('The user choose not light, VGA Test failed, error code is 08001')
            with open(self.logname, 'a+') as f:
                f.write("The user choose not light, VGA Test failed, error code is 08001\r")
        return VGA_result