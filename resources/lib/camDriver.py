import httplib
import xbmc, xbmcgui
import sys
import time
import logging

class cameraInteraction:

	logger = logging.getLogger()
	steam_handler = logging.StreamHandler()

	#init the camera interaction, with the pan
	def __init__(self, ip_camera, debug):
		
		#addon activity is logged only if the user check the option in the settings
		if  debug == True:
			self.logger.setLevel(logging.DEBUG)
			self.steam_handler.setLevel(logging.DEBUG)
			self.logger.addHandler(self.steam_handler)
		else:	
			self.logger.setLevel(logging.WARNING)
			self.steam_handler.setLevel(logging.WARNING)
			self.logger.addHandler(steam_handler)
			
		self.ip = ip_camera
		self.panX = 15
		self.panY = 15
		self.cmdAddress = '/cgi/ptdc.cgi'
	
	#set the new relative position
	def buildSetRelativePosCmdRequest(self, deltaX,deltaY):
		cmd = self.cmdAddress + '?command=set_relative_pos' + '&posX=' + str(deltaX) + '&posY=' + str(deltaY)
		self.logger.debug("Requesting the camera to set a relative position. X = %s , Y = %s" %(str(deltaX), str(deltaY)))
		return cmd
	
	#get back to the initial position
	def buildHomeCmdRequest(self):
		cmd = self.cmdAddress + '?command=go_home'
		self.logger.debug("Requesting the camera to go to the initial position.")
		return cmd
		
	#set the new absolute position 
	def buildSetAbsolutePosCmdRequest(self, deltaX,deltaY):
		cmd = self.cmdAddress + '?command=set_pos' + '&posX=' + str(deltaX) + '&posY=' + str(deltaY)
		self.logger.debug("Requesting the camera to set a relative position. X = %s , Y = %s" %(str(deltaX), str(deltaY)))
		return cmd
	
	#ask the camera to control the room
	def buildPatrolCmdRequest(self):
		cmd = self.cmdAddress + '?command=pan_patrol'
		self.logger.debug("Requesting the camera to go to check the room.")
		return cmd
	

	def request(self, mode='GET', address=None, data=None):
		connection = httplib.HTTPConnection(self.ip)
		if mode == 'GET' or mode == 'DELETE':
			connection.request(mode, address)
			self.logger.debug("Request sent to %s in mode %s." %(mode, address))
		if mode == 'PUT' or mode == 'POST':
			connection.request(mode, address, data)
			self.logger.debug("Request sent to %s in mode %s with data %s." %(mode, address,data))
		
		try :
			result = connection.getresponse()
			response = result.read()
			connection.close()
		except :
			logger.warning("Network problem. Please verify you are connected in the same network of your camera.")
			exit(1)


	def up(self):
		self.logger.debug("Request the camera to go UP")
		self.request('GET',self.buildCmdRequest(0,self.panY))
		
	def down(self):
		self.logger.debug("Request the camera to go DOWN")
		self.request('GET',self.buildCmdRequest(0,-self.panY))
		
	def right(self):
		self.logger.debug("Request the camera to go the RIGHT")
		self.request('GET',self.buildCmdRequest(-self.panX,0))
		
	def left(self):
		self.logger.debug("Request the camera to go to the LEFT")
		self.request('GET',self.buildCmdRequest(self.panX,0))

	def upright(self):
		self.logger.debug("Request the camera to go UP RIGHT")
		self.request('GET',self.buildCmdRequest(-self.panX,self.panY))

	def upleft(self):
		self.logger.debug("Request the camera to go UP LEFT")
		self.request('GET',self.buildCmdRequest(self.panX,self.panY))
		
	def downright(self):
		self.logger.debug("Request the camera to go DOWN RIGHT")
		self.request('GET',self.buildCmdRequest(-self.panX,-self.panY))
		
	def downleft(self):
		self.logger.debug("Request the camera to go DOWN LEFT")
		self.request('GET',self.buildCmdRequest(self.panX,-self.panY))
		
	def checkRoom(self):
		self.logger.debug("Request the camera to do a patrol")
		self.request('GET',self.buildPatrolCmdRequest)
		
	def home(self):
		self.logger.debug("Request the camera to go to the initial position")
		self.request('GET',self.buildHomeCmdRequest())
	
	



