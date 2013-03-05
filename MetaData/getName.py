import os
import urllib2
from xml.dom.minidom import parse, parseString

class TitleRetriever:
	
	driveLetter = "G"
	
	def __init__(self, driveLetter):
		self.driveLetter = driveLetter
	
	def parseDvdTitle(self, tree ):
		return tree.getElementsByTagName("title")[0].firstChild.nodeValue
		
	def parseDVDYear(self, tree ):
		return tree.getElementsByTagName("year")[0].firstChild.nodeValue
		
	def parseDVDPlot(self, tree ):
		return tree.getElementsByTagName("plot")[0].firstChild.nodeValue
		
	#Returns what the .mp4 and folder name should be named
	def getCorrectTitle(self, tree ):
		return self.parseDvdTitle(tree) + " (" + self.parseDVDYear( tree ) + ") "
	
	
	def getDVDId(self):
		#Calls the executable by passing in the drive which has a dvd
		
		dvdidResponse = os.popen("dvdid.exe "+self.driveLetter+"\\")
		#The dvdid is returned with a | which needs to be removed for the api call
		dvdid = dvdidResponse.readline().replace("|","")
		return dvdid
	

	#This will get the DVDid as well as call the API to get the dvd name
	def ProcessDVDIDandCallApi(self):	
		dvdid = self.getDVDId()
		username = "nyanyo";
		password = "mydvdid";
		apiHttp = "http://api.dvdxml.com/";

		
		request = """
		<dvdXml>
			<authentication>
				<user>""" + username + """</user>
				<password>""" + password + """</password>
			</authentication>
			<requests>
				<request type ="information">
					<dvdId>""" + dvdid + """</dvdId>
				</request>
			</requests>
		</dvdXml>
		"""


		req = urllib2.Request(url=apiHttp, 
							  data=request, 
							  headers={'Content-Type': 'application/xml'})
		responseOBJ = urllib2.urlopen(req)
		xmlReponse = responseOBJ.read()
		

		tree = parseString(xmlReponse)
		
		return self.getCorrectTitle(tree)




