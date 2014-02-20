import httplib
import xbmc, xbmcgui
import sys

#to remove
import time
######

###########BOUNDARIES for dcs-5222L 
# <boundaryMaxX>174</boundaryMaxX>
# <boundaryMinX>-171</boundaryMinX>
# <boundaryMaxY>93</boundaryMaxY>
# <boundaryMinY>-29</boundaryMinY>
############


class cameraInterraction():
	def __init__(self, ip_camera):
		self.ip = ip_camera
		self.panX = 15
		self.panY = 15
		self.cmdAddress = '/cgi/ptdc.cgi'




	def buildCmdRequest(self, deltaX,deltaY):
		return self.cmdAddress + '?command=set_relative_pos' + '&posX=' + str(deltaX) + '&posY=' + str(deltaY)
		
	def buildHomeCmdRequest(self):
		return self.cmdAddress + '?command=go_home'
		
	def buildZoomCmdRequest(self, z):
		return self.cmdAddress + '?command=set_zoom&zoom_mag=' + str(z)

	def request(self, mode='GET', address=None, data=None):
		""" Utility function for HTTP GET/PUT requests for the API"""
		print(address)
		connection = httplib.HTTPConnection(self.ip)
		if mode == 'GET' or mode == 'DELETE':
			connection.request(mode, address)
		if mode == 'PUT' or mode == 'POST':
			connection.request(mode, address, data)

		#Qlogger.debug("{0} {1} {2}".format(mode, address, str(data)))
		
		#time.sleep(3)
		result = connection.getresponse()
		response = result.read()
		print(response)
		connection.close()



	def up(self):
		self.request('GET',self.buildCmdRequest(0,self.panY))
		
	def down(self):
		self.request('GET',self.buildCmdRequest(0,-self.panY))
		
	def right(self):
		self.request('GET',self.buildCmdRequest(-self.panX,0))
		
	def left(self):
		self.request('GET',self.buildCmdRequest(self.panX,0))

	def upright(self):
		self.request('GET',self.buildCmdRequest(-self.panX,self.panY))

	def upleft(self):
		self.request('GET',self.buildCmdRequest(self.panX,self.panY))
		
	def downright(self):
		self.request('GET',self.buildCmdRequest(-self.panX,-self.panY))
		
	def downleft(self):
		self.request('GET',self.buildCmdRequest(self.panX,-self.panY))
		
	def panorama(self):
		self.home()
		time.sleep(2)
		self.request('GET',self.buildCmdRequest(-171,0))
		time.sleep(2)
		self.home()
		time.sleep(2)
		self.request('GET',self.buildCmdRequest(174,0))
		time.sleep(2)
		self.home()

	######ZOOM
	def z1x(self): 
		self.request('GET', self.buildZoomCmdRequest(1.0))
		
	def z2x(self): 
		self.request('GET', self.buildZoomCmdRequest(2.0))
		
	def z4x(self): 
		self.request('GET', self.buildZoomCmdRequest(4.0))
		
	#####Home position + Zoom x1
	def home(self):
		self.request('GET',self.buildHomeCmdRequest())
		#z1x()
		
		

######TEST#####
def testallMovments():
	cam = cameraInterraction()
	cam.up()
	time.sleep(1)
	cam.down()
	time.sleep(1)
	cam.right()
	time.sleep(1)
	cam.left()
	time.sleep(1)
	cam.upright()
	time.sleep(1)
	cam.upleft()
	time.sleep(1)
	cam.downright()
	time.sleep(1)
	cam.downleft()
	time.sleep(1)
	
	cam.home()

# if(__name__ == '__main__'):
	# if len(sys.argv) == 1 :
		# xbmc.Player( xbmc.PLAYER_CORE_MPLAYER ).play('rtsp://192.168.0.20:554/play1.sdp')
	# else :
		##len(sys.argv>1)
		# cam = cameraInterraction()
		# if sys.argv[1] == 'up':
			# cam.up()
		# elif sys.argv[1] == 'down':
			# cam.down()
		# elif sys.argv[1] == 'left':
			# cam.left()
		# elif sys.argv[1] == 'right':
			# cam.right()
		# elif sys.argv[1] == 'home':
			# cam.home()
			

		
		
	
	
	



