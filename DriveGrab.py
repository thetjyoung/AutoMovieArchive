import clr
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

from System.Drawing import *
from System.Windows.Forms import *
import string
from ctypes import windll

class MyForm(Form):
    def __init__(self):
        self.Text = 'Hello World'
        self.Height = 375
        self.PATH = "C:/Movies"

        self.label = Label()
        self.label.Text = "Default Save Directory:\n C:\Movies"
        self.label.Location = Point(50, 50)
        self.label.Height = 30
        self.label.Width = 200

        self.drives = self.get_drives()
        self.start_locy = 100
        self.start_locx = 0
        #directories buttons
        for drive in self.drives:
            button = Button()
            button.Text = drive
            if(self.start_locx == 40):
                self.start_locx = 140
                button.Location = Point(140, self.start_locy)
                self.start_locy += 50
            else:
                self.start_locx = 40
                button.Location = Point(40, self.start_locy)
            button.Click += self.buttonPressed
            self.Controls.Add(button)
        #browse button
        browse = Button()
        browse.Text = "Browse for Directory"
        browse.Location = Point(90,self.start_locy)
        browse.Click += self.browsePressed

        #OK button
        okbutton = Button()
        okbutton.Text = "OK"
        okbutton.Location = Point(200,300)
        okbutton.Click += self.okPressed
        
        self.Controls.Add(self.label)
        self.Controls.Add(browse)
        self.Controls.Add(okbutton)


    def buttonPressed(self, sender, args):
        self.PATH = "%s:\Movies"%sender.Text
        self.label.Text = "Default Save Directory:\n %s" % self.PATH

    def browsePressed(self, sender, args):
        dialogf = FolderBrowserDialog()
        if dialogf.ShowDialog(self) == DialogResult.OK:
            self.PATH = dialogf.SelectedPath
            self.label.Text = "Default Save Directory:\n %s" % self.PATH

    def okPressed(self, sender, args):
        cnfg = open("settings.conf","w")
        cnfg.write("PATH-%s" % self.PATH)
        cnfg.close()
        self.Close()

    def get_drives(self):
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1

        return drives


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
Application.Run(form)
