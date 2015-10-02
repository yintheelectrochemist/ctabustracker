import requests
import xml.etree.ElementTree as ET

baseUrl = 'http://www.ctabustracker.com/bustime/api/v1/'
key = 'xt8WAkzJmvbUWNh5WdivFD6jX'

class bustracker():
#===================================================================	
	def _init_(self):
		pass
#===================================================================			
	def getCurrentTime(self):
		getTimeUrl = baseUrl + 'gettime?key=' + key
		try:	
			r = requests.get(getTimeUrl)
			if r.status_code == 200:
				root = ET.fromstring(r.text)
				for child in root:
					if child.tag == 'tm':
						return child.text
					else:
						return 'Unable to return current time!'
			else:
				return 'Service Unavailabe!'
		except:
			return 'Service Unavailabe!'
#===================================================================	
	def getPredTm(self, arg_stpid):
		getPredUrl = baseUrl + 'getpredictions?key=' + key + '&stpid=' + arg_stpid
		rt = []
		prdtm = []
		vid = []
		rtdir = []
		rtdst = []
		stopName = ''
		
		try:
			r = requests.get(getPredUrl)
			if r.status_code == 200:
				root = ET.fromstring(r.text)
				for child in root:
					
					currTime = ''
					
					for grandchild in child:
						if grandchild.tag == 'rt':
							rt.append(grandchild.text)
						elif grandchild.tag == 'prdtm':
							currTime = self.getCurrentTime()
							predTime = grandchild.text
							ETA = self.procTime(currTime, predTime)
							prdtm.append(ETA)
						elif grandchild.tag == 'stpnm':
							stopName = grandchild.text
						elif grandchild.tag == 'vid':
							vid.append(grandchild.text)				
						elif grandchild.tag == 'rtdir':
							rtdir.append(grandchild.text)	
						elif grandchild.tag == 'rtdst':
							rtdst.append(grandchild.text)
			return stopName, rt, prdtm, vid, rtdir																			
		except:		
			return 'Service Unavailabe!'
			
#===================================================================
	def procTime(self, arg_currentTime, arg_predTime):
		
		if len(arg_predTime) == 14 and len(arg_currentTime) == 17:
			predSec = int(arg_predTime[9:11])*3600 + int(arg_predTime[12:14])*60
			currSec = int(arg_currentTime[9:11])*3600 + int(arg_currentTime[12:14])*60
			ETA = predSec - currSec
			if ETA > 120:
				return str(ETA / 60) + ' min'
			elif ETA <= 120 and ETA > 60:
				return '<2 min'
			elif ETA >=60 and ETA > 20:
				return '<1 min'
			else:
				return 'approaching'
		else:
			return 'No Time Information!'
