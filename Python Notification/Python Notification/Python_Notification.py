import clr

clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System.Drawing import Icon
from System.Windows.Forms import (Application, ContextMenu, MenuItem, NotifyIcon)


class Notification(object):

    def __init__(self):
        self.initNotifyIcon()
        self.showBalloon("Saving...", "Your DVD is being archived")

    def initNotifyIcon(self):
        self.notifyIcon = NotifyIcon()
        self.notifyIcon.Icon = Icon("dvd.ico")
        self.notifyIcon.Visible = True
        self.notifyIcon.ContextMenu = self.initContextMenu()

    
    def showBalloon(self, title, text, duration=1000):
        self.notifyIcon.BalloonTipTitle = title
        self.notifyIcon.BalloonTipText = text
        self.notifyIcon.ShowBalloonTip(duration)

        
    def initContextMenu(self):
        contextMenu = ContextMenu()
        exitMenuItem = MenuItem("Exit")
        exitMenuItem.Click += self.onExit
        contextMenu.MenuItems.Add(exitMenuItem)
        return contextMenu
        

    def onExit(self, sender, event):
        self.notifyIcon.Visible = False
        Application.Exit()
   
        
if __name__ == "__main__":
    main = Notification()
    Application.Run()