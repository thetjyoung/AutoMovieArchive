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
        self.Height = 500

        self.label = Label()
        self.label.Text = "Default Save Directory: C:\Movies"
        self.label.Location = Point(50, 50)
        self.label.Height = 30
        self.label.Width = 200

        self.drives = self.get_drives()
        self.start_loc = 100

        for drive in self.drives:
            button = Button()
            button.Text = drive
            button.Location = Point(50, self.start_loc)
            self.start_loc += 50
            button.Click += self.buttonPressed
            self.Controls.Add(self.label)
            self.Controls.Add(button)

    def buttonPressed(self, sender, args):
        self.label.Text = "Default Save Directory: %s:\Movies" % sender.Text

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
