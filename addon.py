import xbmc
import logging
import time
import socket
from settings import *

class Camera:
	connected = False

	def __init__(self, settings):
		
		#self.settings = settings

		logger.debug("Starting camera discovery in the network")
		notify("Searching camera in the network", "Starting")
		camera_ip = self.start_autodiscover()

		if (camera_ip != None):
			notify("Bridge discovery", "Found bridge at: %s" % hue_ip)
		else:
			notify("Bridge discovery", "Failed. Could not find bridge.")

		
	def start_autodiscover(self):
	
		#we will use the principle of uPnP
		port = 1900
		ip = "239.255.255.250"

		address = (ip, port)
		data = """M-SEARCH * HTTP/1.1
		HOST: %s:%s
		MAN: ssdp:discover
		MX: 3
		ST: upnp:rootdevice""" % (ip, port)
	  
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
			if "IpBridge" in recv_data and "description.xml" in recv_data:
				hue_ip = recv_data.split("LOCATION: http://")[1].split(":")[0]
			time.sleep(1)
	  
		return camera_ip
	  
def notify(title, content):
	xbmc.executebuiltin('Notification(%s, %s), 1000' %(title, content))
  
  
def run():
	playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
	playlist.clear()
	playlist.add('rtsp://192.168.0.20:554/play1.sdp')
	xbmc.Player().play(playlist)

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
	#while not camera.connected:
	#	logger.debuglog("Camera is not connected")
	#	time.sleep(1)
	#run()