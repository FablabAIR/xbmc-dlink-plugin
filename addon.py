import xbmc, xbmcaddon
import logging
import time
import socket
from settings import *
from camDriver import *





class Camera:
	connected = False

	def __init__(self, settings):
		self.addon = xbmcaddon.Addon(id='script.surveillanceCameraXBMCAddon')
		self.settings = settings

		
		if settings.camera_ip == 'X.X.X.X':
			logger.debug("Starting camera discovery in the network")
			notify("Searching camera in the network", "Starting")
			
			self.camera_ip = self.start_autodiscover()
			if (self.camera_ip != None):
				notify("Camera discovery", "Found Camera at: %s" % self.camera_ip)
				self.addon.setSetting(id='camera_ip',value=self.camera_ip)
			else:
				notify("Camera discovery", "Failed. Could not find Camera.")
				
			
		else: 
			self.camera_ip = settings.camera_ip

		

		
	def start_autodiscover(self):
	#we will use the principle of uPnP
	  port = 1900
	  ip = "239.255.255.250"

	  address = (ip, port)
	  data = """M-SEARCH * HTTP/1.1
	  HOST: %s:%s
	  MAN: ssdp:discover
	  MX: 5
	  ST: upnp:rootdevice""" % (ip, port)
	  #ST : ssdp:all"""
	  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	  camera_ip = None
	  num_retransmits = 0
	  num_max_retransmits = 10
	  
	  #we will attempt num_max_retransmissions of the paquet
	  while(num_retransmits < num_max_retransmits) and camera_ip == None:
		  num_retransmits += 1
		  client_socket.sendto(data, address)
		  recv_data, addr = client_socket.recvfrom(2048)
		  notify("Camera discovery", recv_data )
		  
	  return camera_ip
	  
def notify(title, content):
	xbmc.executebuiltin('Notification(%s, %s)' %(title, content))
  
  
def runvideo(camera):
	xbmc.Player().play('rtsp://'+str(camera.camera_ip)+'/play1.sdp')

if ( __name__ == "__main__" ):
	settings = settings()
	logger = logging.getLogger()
	steam_handler = logging.StreamHandler()
	
	#addon activity is logged only if the user check the option in the settings
	if settings.debug_enabled == True:
		logger.setLevel(logging.DEBUG)
		steam_handler.setLevel(logging.DEBUG)
	else:	
		logger.setLevel(logging.WARNING)
		steam_handler.setLevel(logging.WARNING)
		
	logger.addHandler(steam_handler)
	
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
	