import xbmc, xbmcaddon
import logging
import time
import re
from settings import *
from camDriver import *
import socket
import httplib
from xml.dom.minidom import parseString

#cameras parameters

#camera with id 0 is DCS-5222L
CONST_CAM0_NAME = "DCS-5222L"
CONST_CAM0_XML = "/webs/description.xml"
CONST_CAM0_URL = "rtsp://*/play1.sdp"
CONST_CAM0_ISCONTROLLABLE = True

#camera 1 is DCS-932L
CONST_CAM1_NAME = "DCS-932L"
CONST_CAM1_XML = "/rootdesc.xml"
CONST_CAM1_URL = "http://*/video.cgi"
CONST_CAM1_ISCONTROLLABLE = False


class Camera:
	
	camera_name = None
	camera_ip = None
	camera_xml = None
	camera_url = None
	camera_isControllable = None
	
	def __init__(self, settings):
		self.addon = xbmcaddon.Addon(id='script.DLinkCameraXBMCAddon')
		self.settings = settings
		
		self.cameraChosen();
		
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
				exit(1)
		else: 
			self.camera_ip = settings.camera_ip
			notify("Camera network address", "Camera IP has been set : %s" %self.camera_ip)
			logger.debug("Camera IP has been set : %s" %self.camera_ip)
		
		
	def cameraChosen(self):
	
		if self.settings.camera_id == 0 :
			
			self.camera_name = CONST_CAM0_NAME
			self.camera_xml =  CONST_CAM0_XML
			self.camera_url = CONST_CAM0_URL
			self.camera_isControllable = CONST_CAM0_ISCONTROLLABLE
		
		else :
		
			self.camera_name = CONST_CAM1_NAME
			self.camera_xml =  CONST_CAM1_XML
			self.camera_url = CONST_CAM1_URL
			self.camera_isControllable = CONST_CAM1_ISCONTROLLABLE
			
		logger.debug("Camera chosen : %s" %self.camera_name)
	
	def start_autodiscover(self):
		notify("Searching camera in the network", "Starting")
		#we will use the principle of uPnP
		port = 1900
		ip = "239.255.255.250"

		address = (ip, port)
		data = """M-SEARCH * HTTP/1.1\r\nST: ssdp:all\r\nMX: 10\r\nMAN: "ssdp:discover"\r\nHOST: %s:%s\r\n\r\n""" % (ip, port)
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		num_retransmits = 1
		num_max_retransmits = 10
		blacklist = ""
	  
		logger.debug("Starting %s camera discover in the network." %num_max_retransmits)
		#we will attempt num_max_retransmissions of the paquet
		while(num_retransmits <= num_max_retransmits) and self.camera_ip == None:
			
			logger.debug("Attempt number %s" %num_retransmits)
			
			try :
				client_socket.sendto(data, address)
				recv_data, addr = client_socket.recvfrom(2048)
				
				logger.debug("addr %s" %addr)
				
			except :
				logger.warning("Network problem. Please verify you are connected in the same network of your camera.")
				exit(1)
				
			logger.debug("A response has been received. Its content : %s" %recv_data)
			
			if str(addr) in blacklist :
				continue
				
			else :
				if self.camera_xml in recv_data:
					
					#we now read the xml file in order to check if it is the requested Camera
					ip = recv_data.split("LOCATION: http://")[1].split(":")[0]
					port = recv_data.split("LOCATION: http://")[1].split(":")[1].split("/")[0]
					logger.debug("IP address/port of the answering device : %s:%s" %(addr, port))   
					
					self.camera_url = self.camera_url.replace('*', ip)
					logger.debug("Attempting to connect to the camera stream : %s" %(self.camera_url))
					
					try :
						connection = httplib.HTTPConnection(ip,port)
						connection.request("GET", self.camera_url, None)
						result = connection.getresponse()
						response = result.read()
					except :
						logger.warning("Network problem. Please verify you are connected in the same network of your camera.")
						exit(1)
						
					loggin.debug("Response received : %s" %response)
					connection.close()
					
					parse = parseString(response)
					modelName = parse.getElementsByTagName('modelName')[0].toxml()
					modelName = modelName.replace('<modelName>','').replace('</modelName>','')
					
					if modelName == self.camera_name :
						#now we are sure this is the camera model we wanted
						self.camera_ip = ip
						break
						
				#this UpNp device is not interesting for us -> blacklist :) 		
				else :
					blacklist = blacklist + " , " + ip
					num_retransmits += 1
	
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
	if camera.camera_name == CONST_CAM0_NAME :
		#this camera con be controlled, so we display buttons in overlay in order to do it
		win = buttonWindow("playerButtons.xml",camera.addon.getAddonInfo('path'),"Default","720p")
		player.setWindow(win)
		player = streamPlayer()
		player.play(camera.camera_url)
		win.doModal()
		del win
		
	else :
		player = streamPlayer()
		player.play(camera.camera_url)
		
		#player.play('rtsp://'+str(camera.camera_ip)+'/play1.sdp')
		#xbmc.Player().play('http://192.168.0.21/video.cgi')
		#xbmc.Player().play('rtsp://'+str(camera.camera_ip)+'/play1.sdp')

		
if ( __name__ == "__main__" ):
	settings = settings()
	logger = logging.getLogger()
	steam_handler = logging.StreamHandler()
	debug = None	
	
	#addon activity is logged only if the user check the option in the settings
	if settings.debug_enabled == True:
		logger.setLevel(logging.DEBUG)
		steam_handler.setLevel(logging.DEBUG)
		logger.addHandler(steam_handler)
		debug = True
		logger.debug("Starting logging the plugin with level DEBUG")
	else:	
		logger.setLevel(logging.WARNING)
		steam_handler.setLevel(logging.WARNING)
		logger.addHandler(steam_handler)
		debug = False
		logger.debug("Starting logging the plugin with level WARNING")
	
	camera = Camera(settings)
	
	if len(sys.argv) == 1 :
		runvideo(camera)
	else :
		cam = cameraInterraction(camera.camera_ip, debug)
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
		elif sys.argv[1] == 'patrol':
			cam.checkroom()