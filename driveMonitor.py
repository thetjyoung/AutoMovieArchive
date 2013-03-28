import clr
clr.AddReference("System.Management")
from System.Management import *
from System import Console, TimeSpan
from MetaData.TitleRetriever import TitleRetriever
import ripper


#This is the call back when detecting a new drive
def CDREventArrived(sender, e):
    ##Get the Event object and display it
    pd = e.NewEvent.Properties["TargetInstance"]
    mbo = pd.Value
    if (mbo.Properties["VolumeName"].Value is not None):
        titleRetriever = TitleRetriever(mbo.Properties["DeviceID"].Value[0:1]);
        movieName = titleRetriever.getMovieName();
        Console.WriteLine("Found: "+movieName)
        
        mkvFile = ripper.rip(titleRetriever.driveLetter, movieName)
		ripper.transcode(mkvFile, movieName)
    else:
        Console.WriteLine("CD has been ejected")


##Set up drive observer
observer = ManagementOperationObserver()
opt = ConnectionOptions()
opt.EnablePrivileges = 1
scope = ManagementScope("root\\CIMV2",opt)
q = WqlEventQuery()
q.EventClassName = "__InstanceModificationEvent"
q.WithinInterval = TimeSpan( 0, 0, 1 )
q.Condition = "TargetInstance ISA 'Win32_LogicalDisk' and TargetInstance.DriveType = 5"
w = ManagementEventWatcher( scope, q )

#Add event handler and use Console.ReadLine() to hold the thread
try:
    w.EventArrived += EventArrivedEventHandler( CDREventArrived )
    w.Start()
    Console.ReadLine()
    w.Stop()
except:
    print "There was an error detecting the cd drive"
finally:
    w.Dispose()
