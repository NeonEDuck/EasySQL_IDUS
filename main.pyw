#!/usr/bin/env python3

import wx
from SQLFrame import SQLFrame

if __name__ == '__main__':

    app = wx.App()
    frm = SQLFrame(None, title='LiteSQL IDUS', size=(800,500))
    frm.version = '1.0.0'
    frm.Show() 
    app.MainLoop()