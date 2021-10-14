#!/usr/bin/python
# -*- coding: <<encoding>> -*-
# -------------------------------------------------------------------------------
#   <<project>>
#
# -------------------------------------------------------------------------------
import time

import wx
import ETH_Test
import this


class Frame(wx.Frame):
    def __init__(self, title):
        wx.Frame.__init__(self, None, title=title, pos=(150, 150), size=(500, 600))
        self.Bind(wx.EVT_CLOSE, self.close_frame)

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
        self.m_serial = wx.TextCtrl(panel, 1)
        hbox.Add(self.m_serial, 1, flag=wx.ALL, border=6)

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

    def start_test(self, event):

        self.start_dialog = wx.MessageDialog(None, "要进行测试吗？ Do You Want To Test?", "测试", wx.YES_NO | wx.ICON_QUESTION)
        self.start_result = self.start_dialog.ShowModal()
        self.start_dialog.Destroy()

        if self.start_result == wx.ID_YES:

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
            print(sn)
            ETH_Test.ethernet(T_104_ETH, T_105_SFP)
            print(T_101_VGA)
            print(T_102_Write_MAC)
            print(T_103_Write_FRU)
            # time.sleep(3)
            self.test_bt.SetLabelText("Testing 30%")

            print(T_104_ETH)
            print(T_105_SFP)
            print(T_106_CPU)

            # time.sleep(3)
            self.test_bt.SetLabelText("Testing 60%")

            print(T_107_Memort)
            print(T_108_Console)
            print(T_109_USB)

            # time.sleep(3)
            self.test_bt.SetLabelText("Testing 90%")

            print(T_110_PCI_E)
            print(T_111_SATA)
            print(T_112_M_2)

            # time.sleep(2)
            self.test_bt.SetLabelText("Testing 90%")
            print("Yes")

            self.summary_dialog = wx.MessageDialog(None, "测试结果如下：", "测试结果", wx.YES_NO | wx.ICON_QUESTION)
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
        self.frame = Frame("Function Test Platform V0.9")
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()