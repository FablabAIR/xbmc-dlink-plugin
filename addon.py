import xbmc, xbmcaddon
import logging
import time
import socket
import re
from settings import *
from camDriver import *

from Zeroconf import *
#from MyListener import *
import socket

import httplib

from xml.dom.minidom import parseString




class Camera:
	connected = False
	camera_ip = None
	
	def __init__(self, settings):
		self.addon = xbmcaddon.Addon(id='script.DLinkCameraXBMCAddon')
		self.settings = settings
		
		pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
		
		if ( (settings.camera_ip == 'X.X.X.X') or (not(pattern.match(settings.camera_ip))) ):
			logger.warning("Camera IP is not set.")
			self.start_autodiscover()
			if (self.camera_ip != None):
				notify("Camera discovery", "Found Camera at : %s" %self.camera_ip)
				logger.debug("Camera discovered. Address IP is : %s" %self.camera_ip)
				self.addon.setSetting(id='camera_ip',value=self.camera_ip)
			else:
				notify("Camera discovery", "Failed. Could not find Camera.")
				logger.warning("Camera discovery Failed. Could not find Camera. Camera_ip == None")
		else: 
			self.camera_ip = settings.camera_ip
			notify("Camera network address", "Camera IP has been set : %s" %self.camera_ip)
			logger.debug("Camera IP has been set : %s" %self.camera_ip)
		
	def start_autodiscover(self):
		notify("Searching camera in the network", "Starting")
		#we will use the principle of uPnP
		port = 1900
		ip = "239.255.255.250"

		address = (ip, port)
		data = """M-SEARCH * HTTP/1.1\r\nST: ssdp:all\r\nMX: 10\r\nMAN: "ssdp:discover"\r\nHOST: %s:%s\r\n\r\n""" % (ip, port)
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		num_retransmits = 0
		num_max_retransmits = 10
	  
		logger.debug("Starting %s camera discover in the network." %num_max_retransmits)
		#we will attempt num_max_retransmissions of the paquet
		while(num_retransmits < num_max_retransmits) and self.camera_ip == None:
			num_retransmits += 1
			logger.debug("Attempt number %s" %num_retransmits)
			
			client_socket.sendto(data, address)
			recv_data, addr = client_socket.recvfrom(2048)
			logger.debug("A response has been received. Its content : %s" %recv_data)
			
			if "/webs/description.xml" in recv_data:
				#we now read the xml file in order to check if it is an IP Camera
				
				#url = recv_data.split("LOCATION: http://"[1].split("SERVER")[0].split("/")[1])
				
				ip = recv_data.split("LOCATION: http://")[1].split(":")[0]
				port = recv_data.split("LOCATION: http://")[1].split(":")[1].split("/")[0]
				#logger.debug("IP address of the  
				#port: %s" %(port))
				
				#rootdesc.xml
				
				url = recv_data.split(ip)[1].split("SERVER")[0].split("/")[1]
				url = "/"+url+"/"+recv_data.split(ip)[1].split("SERVER")[0].split("/")[2]
				print("url: %s" %(url))
				connection = httplib.HTTPConnection(ip,port)
				connection.request("GET", url, None)
				result = connection.getresponse()
				response = result.read()
				print(response)
				notify("TITRE", response)
				connection.close()
				
				
				parse = parseString(response)
				modelName = parse.getElementsByTagName('modelName')[0].toxml()
				modelName = modelName.replace('<modelName>','').replace('</modelName>','')
				
				if modelName == 'DCS-5222L' :
					self.camera_ip = ip
				break
				
				
				#hue_ip = recv_data.split("LOCATION: http://")[1].split(":")[0]


	
class buttonWindow(xbmcgui.WindowXMLDialog):
		def __init__(self, strXMLname, strFallBacklPath, strDefaultName, forceFallback):
			pass
	

class streamPlayer(xbmc.Player):
	def __init__(self):
		xbmc.Player.__init__(xbmc.PLAYER_CORE_MPLAYER)
		self.win = None
		
	def setWindow(self, window):
		self.win = window	
	
	def onPlaybackStopped(self):
		if not self.win == 'None' :
			self.win.close()
			del self.win

		
	
		return camera_ip
	  
def notify(title, content):
	xbmc.executebuiltin('Notification(%s, %s), 10000' %(title, content))
  
  
def runvideo(camera):
	win = buttonWindow("playerButtons.xml",camera.addon.getAddonInfo('path'),"Default","720p")
	player = streamPlayer()
	player.setWindow(win)

	#player.play('rtsp://'+str(camera.camera_ip)+'/play1.sdp')
	xbmc.Player().play('http://192.168.0.21/video.cgi')
	win.doModal()
	del win

	#xbmc.Player().play('rtsp://'+str(camera.camera_ip)+'/play1.sdp')
	
	

	

if ( __name__ == "__main__" ):
	settings = settings()
	logger = logging.getLogger()
	steam_handler = logging.StreamHandler()
	
	#addon activity is logged only if the user check the option in the settings
	if settings.debug_enabled == "true":
		logger.setLevel(logging.DEBUG)
		steam_handler.setLevel(logging.DEBUG)
		logger.addHandler(steam_handler)
		logger.debug("Starting logging the plugin with level DEBUG")
	else:	
		logger.setLevel(logging.WARNING)
		steam_handler.setLevel(logging.WARNING)
		logger.addHandler(steam_handler)
		logger.debug("Starting logging the plugin with level WARNING")
	
	camera = Camera(settings)
	
	
	if len(sys.argv) == 1 :
		runvideo(camera)
	else :
		#len(sys.argv>1)
		cam = cameraInterraction(camera.camera_ip)
		if sys.argv[1] == 'up':
			cam.up()
		elif sys.argv[1] == 'down':
			cam.down()
		elif sys.argv[1] == 'left':
			cam.left()
		elif sys.argv[1] == 'right':
			cam.right()
		elif sys.argv[1] == 'home':
			cam.home()
		elif sys.argv[1] == 'upleft':
			cam.upleft()
		elif sys.argv[1] == 'downleft':
			cam.downleft()
		elif sys.argv[1] == 'downright':
			cam.downright()
		elif sys.argv[1] == 'upright':
			cam.upright()
