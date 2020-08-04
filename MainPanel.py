import wx
import wx.grid as wxGrid
import pyperclip


class MainPanel(wx.Panel):

    def __init__(self, parent, **kwargs):

        table_list = kwargs.get( 'table_list', {} )

        wx.Panel.__init__(self, parent=parent)

        vboxMain = wx.BoxSizer(wx.VERTICAL)

        # StaticText
        st = wx.StaticText(self, label="SELECT VIEW OR TYPE IN SQL")
        font = st.GetFont()
        font.PointSize = 15
        font = font.Bold()
        st.SetFont(font)
        
        vboxMain.Add(st, flag=wx.CENTER|wx.TOP, border=20)

        # Buttons
        hboxBtns = wx.BoxSizer(wx.HORIZONTAL)

        self.buttons = []
        for k in table_list.keys():
            self.buttons.append(wx.Button(self, label=k,size=(80, 50)))
        for btn in self.buttons:
            hboxBtns.Add(btn, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=10 )
            
        for btn in self.buttons: 
            btn.Bind(wx.EVT_BUTTON, self.GetParent().onTableCalledButton)

        vboxMain.Add(hboxBtns, flag=wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER, border=10)


        # Grid
        self.grid = wxGrid.Grid( self )

        maxRows = len(table_list)
        maxCols = len(table_list[max(table_list.keys(), key=lambda x:len(table_list[x]))])
        self.grid.CreateGrid( numRows=maxRows, numCols=maxCols )
        self.grid.EnableEditing(False)
        self.grid.DisableDragGridSize()
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()

        i = 0
        for k, v in table_list.items():
            self.grid.SetRowLabelValue( i, k )
            for j, s in enumerate(v):
                self.grid.SetCellValue( i, j, str(s[0]) )
            i+=1
            

        self.grid.AutoSizeColumns()

        self.grid.Bind( wxGrid.EVT_GRID_CELL_LEFT_DCLICK, self.pasteValue)
        self.grid.Bind( wxGrid.EVT_GRID_LABEL_LEFT_DCLICK, self.pasteValue)

        vboxMain.Add(self.grid, flag=wx.CENTER|wx.TOP, border=10)

        # TextCtrl
        self.textCtrl = wx.TextCtrl( self, -1, size=(-1,120), style = wx.TE_MULTILINE|wx.TE_DONTWRAP )
        font.PointSize = 12
        self.textCtrl.SetFont(font)
        vboxMain.Add( self.textCtrl, flag=wx.EXPAND|wx.RIGHT|wx.LEFT|wx.TOP, border=20 )

        self.buttons.append( wx.Button( self, label='Execute', size=(80, 30) ) )
        vboxMain.Add(self.buttons[-1], flag=wx.TOP|wx.CENTER, border=10 )
        self.buttons[-1].Bind(wx.EVT_BUTTON, self.GetParent().btnOnPressTriggerExecuteSql)

        self.vboxMain = vboxMain
        self.SetSizer(self.vboxMain)

    def pasteValue(self, event):
        row = event.GetRow()
        col = event.GetCol()
        print(row, col)
        items = []
        if (row, col) == (-1, -1):
            for i in range(self.grid.GetNumberRows()):
                entry = []
                for j in range(self.grid.GetNumberCols()):
                    entry.append(self.grid.GetCellValue(i, j))
                items.append(entry)

        elif row == -1:
            for i in range(self.grid.GetNumberRows()):
                items.append(self.grid.GetCellValue(i,col))
        elif col == -1:
            for i in range(self.grid.GetNumberCols()):
                items.append(self.grid.GetCellValue(row,i))
        else:
            items.append(self.grid.GetCellValue(row,col))
        print(items)

        text = ''
        if type(items[0]) == list:
            text = '\n'.join([','.join(entry) for entry in items])
        else:
            text = ','.join(items)

        text = text.replace('\u200B(null)', 'null')
        
        pyperclip.copy( text )
        self.GetParent().SetStatusText("Copy to Clipboard! " + (f'{text[:20]}...' if len(text)>20 else text) )