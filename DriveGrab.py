import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
import string
from ctypes import windll

class DriveGrab(Form):
    def __init__(self):
        self.Text = 'Select default drive'
        self.Height = 225
        self.Width = 250
        self.PATH = "C:/Movies"

        self.label = Label()
        self.label.Text = "Default Save Directory: C:\Movies"
        self.label.Location = Point(50, 20)
        self.label.Height = 30
        self.label.Width = 200

        self.drives = self.get_drives()

        #combo box
        cb = ComboBox()
        cb.Parent = self
        cb.Location = Point(50, 50)
        cb.SelectionChangeCommitted += self.OnChanged

        for drive in self.drives:
            cb.Items.Add(drive)
        
        #browse button
        browse = Button()
        browse.Text = "Browse for Directory"
        browse.Location = Point(50,80)
        browse.Click += self.browsePressed
        browse.AutoSize = True

        #OK button
        okbutton = Button()
        okbutton.Text = "OK"
        okbutton.Location = Point(150,150)
        okbutton.Click += self.okPressed
        
        self.Controls.Add(self.label)
        self.Controls.Add(browse)
        self.Controls.Add(okbutton)

    def OnChanged(self, sender, args):
        self.PATH = "%s:\Movies" % sender.SelectedItem
        self.label.Text = "Default Save Directory: %s" % self.PATH

    def browsePressed(self, sender, args):
        dialogf = FolderBrowserDialog()
        if dialogf.ShowDialog(self) == DialogResult.OK:
            self.PATH = dialogf.SelectedPath
            self.label.Text = "Default Save Directory: %s" % self.PATH

    def okPressed(self, sender, args):
        cnfg = open("settings.conf","w")
        cnfg.write("PATH-%s" % self.PATH)
        cnfg.close()
        self.Close()
        Application.Exit()

    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1

        return drives

if __name__ == '__main__':
    Application.EnableVisualStyles()
    Application.SetCompatibleTextRenderingDefault(False)

    form = DriveGrab()
    Application.Run(form)
