from System.Diagnostics import Process
from System.IO import Path, Directory

def transcode(mkvFile, movieName):
	p = Process()
	p.StartInfo.UseShellExecute = False
	#p.StartInfo.RedirectStandardOutput = True
	p.StartInfo.FileName = "HandBrakeCLI"
	p.StartInfo.Arguments = "-i %s -o %s.mp4 -f mp4 -e x264" % (mkvFile, movieName)
	if p.Start():
		print("Transcoding")
		p.WaitForExit()
		if p.ExitCode == 0:
			print("Successfully transcoded %s" % movieName)
		else:
			print("Error: %d" % p.ExitCode)
	else:
		print("Error transcoding, quitting")

def rip(driveLetter, movieName):
	out = Path.Combine(Path.GetTempPath(), movieName)
	p = Process()
	p.StartInfo.UseShellExecute = False
	#p.StartInfo.RedirectStandardOutput = True
	p.StartInfo.FileName = "makemkvcon"
	p.StartInfo.Arguments = "--minlength=300 mkv disc:0 all %s" % out
	print("Saving to:", out)
	print(p.StartInfo.Arguments)
	if p.Start():
		print("Ripping")
		p.WaitForExit()
		if p.ExitCode == 0:
			print("Successfully ripped %s" % movieName)

			return Directory.GetFiles(out)[0]
		else:
			print("Error: %d" % p.ExitCode)
	else:
		print("Error ripping, quitting")
