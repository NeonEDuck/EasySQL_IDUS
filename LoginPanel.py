import wx
import wx.grid as wxGrid
import saveAndLoad

class LoginPanel(wx.Panel):

    textCrtlList = {}
    
    def __init__(self, parent, **kwargs):

        setting = saveAndLoad.load()

        wx.Panel.__init__(self, parent=parent)
        vboxMain = wx.BoxSizer(wx.VERTICAL)

        # StaticText
        st = wx.StaticText(self, label='DATABASE CONNECTION SETTING')
        font = st.GetFont()
        font.PointSize = 15
        font = font.Bold()
        st.SetFont(font)
        
        vboxMain.Add(st, flag=wx.CENTER|wx.TOP, border=20)

        vboxMain.Add( self.createTextField(label='host',text=setting.get('host','')), flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.CENTER, border=20 )
        vboxMain.Add( self.createTextField(label='port',text=setting.get('port','5432')), flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.CENTER, border=20 )
        vboxMain.Add( self.createTextField(label='user',text=setting.get('user','')), flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.CENTER, border=20 )
        vboxMain.Add( self.createTextField(label='password',text=setting.get('password','')), flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.CENTER, border=20 )
        vboxMain.Add( self.createTextField(label='database',text=setting.get('database','')), flag=wx.RIGHT|wx.LEFT|wx.TOP|wx.CENTER, border=20 )

        # Buttons
        hboxBtns = wx.BoxSizer(wx.HORIZONTAL)

        self.buttons = []
        self.buttons.append(wx.Button(self, label='Connect',size=(120, 30)))

        for btn in self.buttons:
            hboxBtns.Add(btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10 )

        vboxMain.Add(hboxBtns, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER, border=10)

        self.SetSizer(vboxMain)

    def createTextField(self, label, text):
        hbox = wx.BoxSizer(wx.HORIZONTAL)


        # StaticText
        st = wx.StaticText(self, label=label.title(), size=(100,-1), style=wx.ALIGN_RIGHT)
        font = st.GetFont()
        font.PointSize = 12
        st.SetFont(font)
        hbox.Add( st )
        # TextCtrl
        if label=='password':
            tc = wx.TextCtrl( self, size=(400,-1), value=text, style=wx.TE_PASSWORD )
        else:
            tc = wx.TextCtrl( self, size=(400,-1), value=text )
        tc.SetFont(font)
        hbox.Add( tc, flag=wx.LEFT, border=20 )
        self.textCrtlList[label] = tc
        return hbox