#!/usr/bin/env python
import subprocess
import sys
import re

def parseMetadata(devicePath):
	args = ['HandBrakeCLI', '-i', devicePath, '-t', '0']
	print("Running:" + ' '.join(args))
	p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#	p = subprocess.Popen(['HandBrakeCLI', '-i', '/dev/sr0', '-o', 'strange--brew.mp4', '-f', 'mp4', '-e', 'x264'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	def byline():
		while p.poll() is None:
			yield p.stdout.readline().decode('utf-8')

	redvdtitle = re.compile('DVD Title: ([A-Z_]+)')
	retitle = re.compile('^\+ title (\d+):')
	reduration = re.compile('^\s+\+ duration: (\d+):(\d+):(\d+)')


	dvdtitle = None
	for line in byline():
		m = redvdtitle.search(line)
		if m:
			dvdtitle = m.group(1)
			break

	titles = list()
	tTitle = None
	for line in byline():
		if lookingForTitle:
			m = retitle.search(line)
			if m:
				tTitle = {'title': m.group(1)}
				lookingForTitle = False
				lookingForDuration = True
			continue

		if lookingForDuration:
			m = reduration.search(line)
			if m:
				hours, minutes, seconds = [int(x, 10) for x in m.group(1, 2, 3)]
				tTitle['duration'] = hours*3600 + minutes*60 + seconds
				titles.append(tTitle)
				lookingForDuration = False
				lookingForTitle = True
			continue

	feature = max(titles, key=lambda x: x['duration'])

	return dvdtitle, feature['title']

def rip(out, src, track=1):
	ret = subprocess.call(['HandBrakeCLI', '-i', src, '-o', out, '-f', 'mp4', '-e', 'x264', '-t', str(track)], stdout=sys.stdout, stderr=sys.stderr)
	if ret != 0:
		print("Error ripping DVD")
	else:
		print("Done!")

print('Getting info from disk')
title, track = parseMetadata('/dev/sr0')

title = title.replace("_", " ").title()
print("Ripping %s. This may take a while:" % title)
rip(title+".mp4", '/dev/sr0', track)
