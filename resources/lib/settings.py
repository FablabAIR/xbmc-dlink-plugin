import sys
import xbmcaddon

__addon__ = xbmcaddon.Addon(id='script.DLinkCameraXBMCAddon')

class settings():
	def __init__( self, *args, **kwargs ):
		self.readxml()
		
	def readxml(self):
                self.camera_id     = int(__addon__.getSetting("id_camera"))
		self.camera_ip     = __addon__.getSetting("camera_ip")
		self.debug_enabled = bool(__addon__.getSetting("debug_enabled"))
		
	def update(self, **kwargs):
		self.__dict__.update(**kwargs)
		for k, v in kwargs.iteritems():
			self.addon.setSetting(k, v)
