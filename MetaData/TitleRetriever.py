import os
import urllib2
import StringIO
import re

class TitleRetriever:
	
    driveLetter = "G"
    dvdTitle = ""
    dvdYear = ""
    dvdPlot = ""


    def __init__(self, driveLetter):
        self.driveLetter = driveLetter

    #Returns what the .mp4 and folder name should be named
    def getCorrectTitle(self):
        title = self.dvdTitle+ " (" + self.dvdYear + ") "
        return title

    def getDVDId(self):
        #Calls the executable by passing in the drive which has a dvd
        full_path = os.path.realpath(__file__)

        #TODO: this fails if there is a space in the path
        #print os.path.dirname(full_path)+ "\dvdid.exe "+self.driveLetter+":\\";
        dvdidResponse = os.popen(os.path.dirname(full_path)+ "\dvdid.exe "+self.driveLetter+":\\")
        #The dvdid is returned with a | which needs to be removed for the api call
        dvdid = dvdidResponse.readline().replace("|","")
        return dvdid

    def parseXMLResponse(self, response):

        #line by line parsing is done here because iron python has issues with some xml parsers
        s = StringIO.StringIO(response)
        for line in s:
            titleObj  = re.search(r'title>(.*)<',line);
            yearObj  = re.search(r"year>(.*)<",line);
            plotObj  = re.search(r"plot>(.*)<",line);
            if titleObj:
                self.dvdTitle = titleObj.group(1)
            if yearObj:
                self.dvdYear = yearObj.group(1)
            if plotObj:
                self.dvdPlot = plotObj.group(1)
        return response;

    #This will get the DVDid as well as call the API to get the dvd name
    def getMovieName(self):	
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
        
        
        success = self.parseXMLResponse(xmlReponse)
        
        newTitle = self.getCorrectTitle()
        return newTitle
