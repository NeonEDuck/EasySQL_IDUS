#!/usr/bin/env python3

import wx
import wx.grid as wxGrid
from SQLConnect import SQLConnect
import saveAndLoad
from MainPanel import MainPanel
from LoginPanel import LoginPanel
from functools import partial
import timeit
import psycopg2


def status_to_processing(function):
    def wrapper(self, *args, **kwargs):
        self.SetStatusText("Processing...")
        tic = timeit.default_timer() # timer start
        Fail = function(self, *args, **kwargs)
        if Fail == None or Fail == False:
            toc = timeit.default_timer() # timer end
            self.SetStatusText(f"Done! Time tooks: {round(toc - tic, 5)}s")

    return wrapper

class SQLFrame(wx.Frame):

    version = '1.0.0'
    SQLConnect = None

    laststmt = ''

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(SQLFrame, self).__init__(*args, **kw)

        # create a panel in the frame
        self.loginPnl = LoginPanel( self )
        self.loginPnl.buttons[0].Bind(wx.EVT_BUTTON, self.connectToDatabase)

        self.mainPnl = wx.Panel( self )
        self.mainPnl.Hide()

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.loginPnl, 1, wx.EXPAND)
        self.sizer.Add(self.mainPnl, 1, wx.EXPAND)
        self.Centre()
        self.SetSizer(self.sizer)


        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("")


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        loginItem = fileMenu.Append(-1, "&Back to Login",
                "Back to Login")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        tipsItem = helpMenu.Append(wx.ID_ANY, 'Tips')

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnBackOnLogin, loginItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        self.Bind(wx.EVT_MENU, self.OnTips, tipsItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


    def OnBackOnLogin(self, event):
        """Say hello to the user."""
        self.openPanel( [self.loginPnl] )


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox(f"This is LiteSQL IDUS,\nLimited but good enough for basic SQL needs.\n\nversion: {self.version}",
                      "About LiteSQL IDUS",
                      wx.OK|wx.ICON_INFORMATION)

                      
    def OnTips(self, event):
        """Display an Tips Dialog"""
        wx.MessageBox(f"Tips:\nDouble click a cell to copy it's value,\nDouble click the row/col label to copy the whole row/col\n",
                      "About LiteSQL IDUS",
                      wx.OK|wx.ICON_QUESTION)
        
    
    def mainPnlInit(self):
        self.mainPnl.Destroy()
        self.mainPnl = MainPanel( self, table_list=self.SQLConnect.table_list )
        self.sizer.Add(self.mainPnl, 1, wx.EXPAND)

    @status_to_processing
    def connectToDatabase(self, event):
        btn = event.GetEventObject().GetLabel()
        setting = {}
        for k, tc in self.loginPnl.textCrtlList.items():
            setting[k] = tc.GetValue()
        self.SQLConnect = SQLConnect(setting)
        if self.SQLConnect.status_code == 'OK':
            self.mainPnlInit()
            self.loginPnl.Hide()
            self.mainPnl.Show()
            self.Layout()
            saveAndLoad.save(setting)
        else:
            self.SetStatusText(self.SQLConnect.status_code)

    @status_to_processing
    def onTableCalledButton(self, event):
        btn = event.GetEventObject().GetLabel()
        print(btn)
        self.executeSql(statment=f"SELECT * FROM {btn}")

    def btnOnPressTriggerExecuteSql(self,event):
        self.executeSql()

    @status_to_processing
    def executeSql(self, **kwargs):
        stmt = kwargs.get('statment', self.mainPnl.textCtrl.GetValue())
        print(stmt)
        if stmt != '':
            try:
                with self.SQLConnect.connect() as (conn, cursor):
                    query = stmt
                    cursor.execute(query)
                    if cursor.description != None:
                        table_data = cursor.fetchall()
                        # print(table_data)
                        self.mainPnl.grid.DeleteRows(numRows=self.mainPnl.grid.GetNumberRows())
                        self.mainPnl.grid.DeleteCols(numCols=self.mainPnl.grid.GetNumberCols())
                        # self.mainPnl.grid.ClearGrid()
                        # self.mainPnl.grid.SetCellTextColour()

                        maxRows = max(len(table_data),1)
                        maxCols = len(cursor.description)

                        self.mainPnl.grid.AppendRows(numRows=maxRows)
                        self.mainPnl.grid.AppendCols(numCols=maxCols)

                        self.mainPnl.grid.SetRowLabelValue(0, '1')
                        for i, entry in enumerate(table_data):
                            self.mainPnl.grid.SetRowLabelValue(i, str(i+1))
                            # print(entry)
                            for j, e in enumerate(entry):
                                self.mainPnl.grid.SetCellValue( i, j, '\u200B(null)' if e == None else e )
                                if e == None:
                                    self.mainPnl.grid.SetCellTextColour(i,j,wx.Colour(200,200,200))

                        for i, desc in enumerate(cursor.description):
                            self.mainPnl.grid.SetColLabelValue(i, desc.name)

                        self.mainPnl.grid.AutoSizeColumns()
                        for i in range(maxCols):
                            if self.mainPnl.grid.GetColSize(i)>200:
                                self.mainPnl.grid.SetColSize(i, 200)
                        self.Layout()
                    else:
                        conn.commit()
            except psycopg2.DatabaseError as err:
                self.SetStatusText(err.args[0])
                return True

    def openPanel(self, pnl):
        self.loginPnl.Hide()
        self.mainPnl.Hide()
        pnl[0].Show()
        self.Layout()