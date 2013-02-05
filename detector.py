import wmi
import signal

# fixes problems with Ctrl+C on Windows
signal.signal(signal.SIGINT, signal.SIG_DFL)

c = wmi.WMI()
w = c.Win32_CDROMDrive.watch_for()
while True:
	e = w()
	if e.MediaLoaded:
		print("CD inserted: %s, %s" % (e.Drive, e.VolumeName))
	else:
		print("CD removed: %s" % e.Drive)
