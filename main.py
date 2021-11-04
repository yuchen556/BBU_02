#!/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------
import time
import wx
import subprocess
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
from switch_keycode import switch_keycode
from Verify_SN import Verify_SN
from Search_SN_Maxwell import fetch_MAC
from Write_MAC import write_Mac
from Write_FRU import write_FRU

HOSTPORT = '10.168.1.124'  # This PC port IP
buildoption_type = 'Intel(R) Xeon(R) D-2177NT CPU @ 1.90GHz'
logname = 'ft_test_log.txt'
ETHPORT = 'enp3s0'  # BBU Ethernet port name
hostname = '10.168.1.213'  # BBU USB port IP
IPMIPORT = '10.168.1.214'  # BBU IPMI port IP
DEFGW = '10.168.1.1'
ETHPORT_IP = '10.168.1.215'  # BBU ETH port IP
port = 22
username = 'root'  # BBU login user
password = '1'  # BBU login password
SFPPORT1 = 'enp184s0f0'  # BBU SFP port1 name
SFPPORT2 = 'enp184s0f1'  # BBU SFP port2 name
SFPPORT3 = 'enp184s0f2'  # BBU SFP port3 name
SFPPORT4 = 'enp184s0f3'  # BBU SFP port4 name
value2 = ''
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'joinus123'
mysql_database = 'ftdb'
BMD = '2021-11-03'  # mfgDate
BMT = '11:11:11'  # mfgTime
# BSN = '1234567899876'  # Board Serial number
BPN = '0206-00003-0005'  # Board Part number
# PSN = '1234567899876'  # Product Serial number
PPN = '0211-00001-0000'  # Product Part number
ProductN = 'BBU'  # Product Name
ProductV = 'Rev-1'  # Product Version

subprocess.getoutput("rm -f %s" % logname)


class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(720, 50), size=(1080, 720))
        self.Bind(wx.EVT_CLOSE, self.close_frame)
        # self.Bind(wx.EVT_KEY_DOWN, self.on_key_press)
        # self.Bind(wx.EVT_KEY_UP, self.on_key_release)

        global panel,hbox
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Font configuration
        self.font_00 = wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font_01 = wx.Font(14, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        # Text for window title
        self.m_text = wx.StaticText(panel, -1, "Maxwell Function Test!")
        self.m_text.SetFont(self.font_00)
        self.m_text.SetSize(self.m_text.GetBestSize())
        vbox.Add(self.m_text, 0, wx.ALIGN_CENTER | wx.TOP | wx.LEFT | wx.RIGHT |wx.BOTTOM, 20)

        # Test button
        self.test_bt = wx.Button(panel, wx.ID_CLOSE, "Start Test", size=(200, 30))
        self.test_bt.SetFont(self.font_01)
        self.test_bt.Bind(wx.EVT_BUTTON, self.start_test)
        vbox.Add(self.test_bt, 0, wx.ALIGN_LEFT | wx.ALL, 6)

        # Serial number
        self.m_text_SN = wx.StaticText(panel, 1, "Scan SN:")
        self.m_text_SN.SetFont(self.font_01)
        self.m_text_SN.SetSize(self.m_text_SN.GetBestSize())
        hbox.Add(self.m_text_SN, 1, flag=wx.ALL, border=6)

        # Serial number Text entry 02CB091800002
        self.m_serial = wx.TextCtrl(panel, 1,)
        hbox.Add(self.m_serial, 2, flag=wx.ALL, border=6)

        self.T_01_VGA = wx.CheckBox(panel, 1, '01-VGA Test')
        self.T_01_VGA.SetValue(True)
        self.T_02_Write_MAC = wx.CheckBox(panel, 2, '02-Write_MAC')
        self.T_02_Write_MAC.SetValue(True)
        self.T_03_Write_FRU = wx.CheckBox(panel, 3, '03-Write_FRU')
        self.T_03_Write_FRU.SetValue(True)

        self.T_04_ETH = wx.CheckBox(panel, 4, '04-ETH_Test')
        self.T_04_ETH.SetValue(True)
        self.T_05_SFP = wx.CheckBox(panel, 5, '05-SFP_Test')
        self.T_05_SFP.SetValue(True)
        self.T_06_CPU = wx.CheckBox(panel, 6, '06-CPU_Test')
        self.T_06_CPU.SetValue(True)

        self.T_07_Memory = wx.CheckBox(panel, 7, '07-Memory_Test')
        self.T_07_Memory.SetValue(True)
        self.T_08_Console = wx.CheckBox(panel, 8, '08-Console_Test')
        self.T_08_Console.SetValue(True)
        self.T_09_USB = wx.CheckBox(panel, 9, '09-USB_Test')
        self.T_09_USB.SetValue(True)

        self.T_10_PCI_E = wx.CheckBox(panel, 10, '10-PCI-E_Test')
        self.T_10_PCI_E.SetValue(True)
        self.T_11_SATA = wx.CheckBox(panel, 11, '11-SATA_Test')
        self.T_11_SATA.SetValue(True)
        self.T_12_M_2 = wx.CheckBox(panel, 12, '12-M.2_Test')
        self.T_12_M_2.SetValue(True)

        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1, id2=3)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=1)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=2)
        # self.Bind(wx.EVT_CHECKBOX, self.on_checkbox_click, id=3)
        vbox.Add(hbox, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_01_VGA, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_02_Write_MAC, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_03_Write_FRU, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_04_ETH, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_05_SFP, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_06_CPU, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_07_Memory, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_08_Console, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_09_USB, 0, flag=wx.ALL, border=6)

        vbox.Add(self.T_10_PCI_E, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_11_SATA, 0, flag=wx.ALL, border=6)
        vbox.Add(self.T_12_M_2, 0, flag=wx.ALL, border=6)

        panel.SetSizer(vbox)
        panel.Layout()

    # def on_key_press(self, event):
    #     # print('key press')
    #     global Key_Code,value,value2,t_press
    #     t_press = time.time()
    #     Key_Code = event.GetKeyCode()
    #     if (48 <= Key_Code <= 90):
    #         value = switch_keycode(Key_Code).switch_content()
    #         value2 = str(value2) + str(value)
    #         # print(value)
    #         # print(value2)
    #     # event.Skip()
    #
    # def on_key_release(self, event):
    #     # print('key release')
    #     t_realease = time.time()
    #     duration = t_realease - t_press
    #     # print(duration)
    #     global value2
    #     if duration > 0.04:
    #         warning_message = wx.MessageDialog(None, "please do not input manually", "warning", wx.OK | wx.ICON_INFORMATION)
    #         value2 = ''
    #         self.m_serial.Clear()
    #         if warning_message.ShowModal() == wx.ID_OK:
    #             warning_message.Destroy()
    #     elif Key_Code == 13:
    #         # print('press enter')
    #         self.m_serial.SetValue(value2)
    #     # event.Skip()

    def start_test(self, event):

        self.start_dialog = wx.MessageDialog(None, "要进行测试吗？ Do You Want To Test?", "测试", wx.YES_NO | wx.ICON_QUESTION)
        self.start_result = self.start_dialog.ShowModal()
        self.start_dialog.Destroy()

        if self.start_result == wx.ID_YES:
            # self.start_dialog.Destroy()
            Serial_number = self.m_serial.GetValue()
            SN_check = Verify_SN(Serial_number).test_content()
            connect = subprocess.getoutput("ping -c 2 %s" % hostname)
            if SN_check == 'FAIL':
                warning_message = wx.MessageDialog(None, "Wrong serial or serial number has lower case", "warning", wx.OK | wx.ICON_INFORMATION)
                if warning_message.ShowModal() == wx.ID_OK:
                    warning_message.Destroy()

            elif '100% packet loss' in connect:
                warning_message = wx.MessageDialog(None, "Connect to BBU failed, test stop", "warning", wx.OK | wx.ICON_INFORMATION)
                if warning_message.ShowModal() == wx.ID_OK:
                    warning_message.Destroy()

            else:
                T_101_VGA = self.T_01_VGA.GetValue()
                T_102_Write_MAC = self.T_02_Write_MAC.GetValue()
                T_103_Write_FRU = self.T_03_Write_FRU.GetValue()

                T_104_ETH = self.T_04_ETH.GetValue()
                T_105_SFP = self.T_05_SFP.GetValue()
                T_106_CPU = self.T_06_CPU.GetValue()

                T_107_Memort = self.T_07_Memory.GetValue()
                T_108_Console = self.T_08_Console.GetValue()
                T_109_USB = self.T_09_USB.GetValue()

                T_110_PCI_E = self.T_10_PCI_E.GetValue()
                T_111_SATA = self.T_11_SATA.GetValue()
                T_112_M_2 = self.T_12_M_2.GetValue()

                self.m_serial.Enable(False)
                self.test_bt.Disable()
                self.test_bt.SetBackgroundColour((0, 220, 18))
                self.test_bt.SetFont(self.font_01)
                self.test_bt.SetLabelText("Testing")

                sn = self.m_serial.GetValue()
                # print(sn)

                if T_101_VGA:
                    global VGA_result
                    VGA_result = VGA_test(logname).test_content()
                    print('VGA test result is %s' % VGA_result)
                else:
                    VGA_result = 'not test'

                if T_102_Write_MAC:
                    global Write_MAC_result
                    Mac_address = fetch_MAC(logname, sn, mysql_host, mysql_user, mysql_password,
                                            mysql_database).search_db_sn()
                    free_mac = fetch_MAC(logname, sn, mysql_host, mysql_user, mysql_password,
                                            mysql_database).search_free_mac()
                    if free_mac < 200:
                        warning = wx.MessageBox('MAC地址不足，请联系上海众新补充MAC地址', 'info', wx.OK | wx.ICON_INFORMATION)
                        if warning.ShowModal() == wx.ID_OK:
                            warning.Destroy()
                    # print('fetch MAC address : ', Mac_address)
                    if Mac_address == 'No need to fetch MAC':
                        Write_MAC_result = 'the board is tested board, skip this step'
                        Write_MAC_result = 'no write'
                    elif Mac_address == 'FAIL':
                        # print("Operate mysql db error")
                        Write_MAC_result = 'FAIL'
                    else:
                        Write_MAC_result = write_Mac(logname, hostname, port, username, password,
                                                     Mac_address).test_content()
                        print('Write MAC result is %s' % Write_MAC_result)
                else:
                    Write_MAC_result = 'no write'

                if T_103_Write_FRU:
                    global Write_FRU_result
                    BSN = Serial_number
                    PSN = Serial_number
                    Write_FRU_result = write_FRU(logname, BMD, BMT, BSN, BPN, PSN, PPN, ProductN, ProductV, hostname,
                                                 port, username, password).write_content()
                    print('Write fru info result is %s' % Write_FRU_result)
                else:
                    Write_FRU_result = 'not write'

                # print(T_101_VGA)
                # print(T_102_Write_MAC)
                # print(T_103_Write_FRU)
                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 30%")

                if T_104_ETH:
                    global ETH_result
                    ETH_result = ETH_test(logname, ETHPORT, HOSTPORT, IPMIPORT, DEFGW, ETHPORT_IP, hostname, port,
                                          username, password).test_content()
                    print('ETH test result is %s' % ETH_result)
                else:
                    ETH_result = 'not test'

                if T_105_SFP:
                    global SFP_result
                    SFP_result = SFP_test(logname, hostname, port, username, password, SFPPORT1, SFPPORT2, SFPPORT3,
                                          SFPPORT4).test_content()
                    print('SFP test result is %s' % SFP_result)
                else:
                    SFP_result = 'not test'

                if T_106_CPU:
                    global CPU_result
                    CPU_result = CPU_test(logname, buildoption_type, hostname, port, username, password).test_content()
                    print('CPU test result is %s' % CPU_result)
                else:
                    CPU_result = 'not test'
                # print(T_104_ETH)
                # print(T_105_SFP)
                # print(T_106_CPU)

                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 60%")

                if T_107_Memort:
                    global Memory_result
                    Memory_result = Memory_test(logname, hostname, port, username, password).test_content()
                    print('Memory test result is %s' % Memory_result)
                else:
                    Memory_result = 'not test'

                if T_108_Console:
                    global CONSOLE_result
                    CONSOLE_result = CONSOLE_test(logname, hostname, port, username, password).test_content()
                    print('CONSOLE test result is %s' % CONSOLE_result)
                else:
                    CONSOLE_result = 'not test'

                if T_109_USB:
                    global USB_result
                    USB_result = USB_test(logname, hostname, port, username, password).test_content()
                    print('USB test result is %s' % USB_result)
                else:
                    USB_result = 'not test'
                # print(T_107_Memort)
                # print(T_108_Console)
                # print(T_109_USB)

                # time.sleep(3)
                self.test_bt.SetLabelText("Testing 90%")

                if T_110_PCI_E:
                    global PCIE_result
                    PCIE_result = PCIE_test(logname, hostname, port, username, password).test_content()
                    print('PCIE test result is %s' % PCIE_result)
                else:
                    PCIE_result = 'not test'

                if T_111_SATA:
                    global SATA_result
                    SATA_result = SATA_test(logname, hostname, port, username, password).test_content()
                    print('SATA test result is %s' % SATA_result)
                else:
                    SATA_result = 'not test'

                if T_112_M_2:
                    global SSD_result
                    SSD_result = SSD_test(logname, hostname, port, username, password).test_content()
                    print('M.2 test result is %s' % SSD_result)
                else:
                    SSD_result = 'not test'
                # print(T_110_PCI_E)
                # print(T_111_SATA)
                # print(T_112_M_2)

                # time.sleep(2)
                self.test_bt.SetLabelText("Testing 100%")
                # print("Yes")

                test_result = 'MAC: %s \rFRU: %s \rVGA: %s \rETH: %s \rSFP: %s \rCPU: %s\r' \
                              'Memory: %s\rCONSOLE: %s\rUSB: %s\rPCIE: %s\r SATA: %s\rM.2: %s\r' \
                              % (Write_MAC_result, Write_FRU_result, VGA_result, ETH_result, SFP_result, CPU_result,
                                 Memory_result, CONSOLE_result, USB_result, PCIE_result, SATA_result, SSD_result)

                self.summary_dialog = wx.MessageDialog(None, "测试结果如下：", test_result, wx.OK | wx.ICON_INFORMATION)
                self.summary_result = self.summary_dialog.ShowModal()
                self.summary_dialog.Destroy()

                self.Destroy()

        else:
            print("No")
            print("No")
            print("No")
            print("No")
            print("No")
            print("No")
            self.Destroy()

    def close_frame(self, event):
        dialog = wx.MessageDialog(None, "Do You Want To Exit?", "Close", wx.YES_NO | wx.ICON_QUESTION)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_YES:
            self.Destroy()


class MyApp(wx.App):
    def OnInit(self):
        self.frame = Frame("Function Test Platform V1.0")
        # self.Bind(wx.EVT_KEY_DOWN, self.frame.on_key_press)
        # self.Bind(wx.EVT_KEY_UP, self.frame.on_key_release)
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
