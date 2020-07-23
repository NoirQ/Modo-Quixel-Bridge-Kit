#python

# Quixel stuff from here:
# https://github.com/Quixel/Bridge-Python-Plugin


import json, sys, socket, time, threading

import lx
import lxifc
import lxu
import Queue

callback_queue = Queue.Queue() 
interval = 1000

host, port = '127.0.0.1', 24981 # The port number here is just an arbitrary number that's > 20000

threadServer = None

#Background_Server is driven from Thread class in order to make it run in the background.
class ms_Init(threading.Thread):

	#Initialize the thread and assign the method (i.e. importer) to be called when it receives JSON data.
	def __init__(self, importer):
		threading.Thread.__init__(self)
		self.importer = importer
		self.stopThread = False

	#Start the thread to start listing to the port.
	def run(self):
    		#Adding a little delay to the thread doesn't get called in an infinite loop.
		time.sleep(0.1)
		
		try:
			#Making a socket object.
			socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			#Binding the socket to host and port number mentioned at the start.
			socket_.bind((host, port))

			#Run until the thread starts receiving data.
			while True:
				if self.stopThread:
					return
				socket_.listen(5)
				#Accept connection request.
				client, addr = socket_.accept()
				data = ""
				buffer_size = 4096*2
				#Receive data from the client. 
				data = client.recv(buffer_size)

				#If any data is received over the port.
				if data != "":
					self.TotalData = b""
					self.TotalData += data #Append the previously received data to the Total Data.
					#Keep running until the connection is open and we are receiving data.
					while True:
						if self.stopThread:
							return
    					#Keep receiving data from client.
						data = client.recv(4096*2)
						#if we are getting data keep appending it to the Total data.
						if data : self.TotalData += data
						else:
    						#Once the data transmission is over call the importer method and send the collected TotalData.
							self.importer(self.TotalData)
							break

		except:
			pass

def ms_asset_importer (imported_data): 	
	try:
		#Array of assets in case of Batch export.
		imported_assets_array = []
		#Parsing JSON data that we received earlier.
		json_array = json.loads(imported_data)

		#For each asset data in the received array of assets (Multiple in case of batch export)
		for jData in json_array:
			packed_textures_list = [] #Channel packed texture list.
			textures_list = [] #All of the other textures list.
			geo_list = [] #Geometry list will contain data about meshes and LODs.

			#Get and store textures in the textures_list.
			for item in jData['components']:
				if 'path' in item:
					textures_list.append([item['path'], item['type']])

			#Get and store the geometry in the geo_list.
			for item in jData['meshList']:
				if 'path' in item:
					geo_list.append(item['path'])
			
			#Get and store the channel packed textures in the packed_texture_list.
			for item in jData['packedTextures']:
				if 'path' in item:
					packed_textures_list.append([item['path'], item['type']])

			#Reading other variables from JSON data. 
			export_ = dict({
				"AssetID": jData['id'],
				"FolderPath": jData['path'],
				"MeshList": geo_list,
				"TextureList": textures_list,
				"packedTextures": packed_textures_list,
				"Resolution": jData['resolution'],
				"activeLOD": jData['activeLOD']
			})
			
			callback_queue.put(export_)

	
	#Exception handling.
	except Exception as e:
		print "Failed"
		print('Error Line : {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
		pass

class doTheWork(lxifc.Visitor):
	def __init__(self):
		self.importData = None
		pass

	def vis_Evaluate(self):
		if self.importData is not None:
			tSrv = lx.service.Thread()
			tSrv.InitThread()
			for mesh in self.importData["MeshList"]:
				lx.eval("scene.open {%s} import" % mesh)
			textstring = ""
			for texture in self.importData["TextureList"]:
				textstring = textstring + texture[0] + ";"
			# not supported in the pbr command in 14.1
			for texture in self.importData["packedTextures"]:
				textstring = textstring + texture[0] + ";"

			print textstring
			lx.eval("shader.loadPBR path:{%s}" % textstring)
			tSrv.CleanupThread()

			


class visIdle (lxifc.Visitor):
	# checks to see if we have any new incoming things when user is idle, run on a timer. Currently every second, could be expanded.
	def __init__(self):
		pass

	def vis_Evaluate(self):
		pSrv = lx.service.Platform()
		callback = None
		try:
			callback = callback_queue.get(False) #doesn't block	
		except Queue.Empty:
			pass
		
		if callback is not None:
			idleVis = doTheWork()
			idleVis.importData = callback
			doTheWork_com = lx.object.Unknown(idleVis)
			pSrv.DoWhenUserIsIdle(doTheWork_com, lx.symbol.iUSERIDLE_ALWAYS)

		# wait for next idle again
		myVis = self
		com_myVis = lx.object.Unknown(myVis)
		pSrv.TimerStart(com_myVis, interval, lx.symbol.iUSERIDLE_ALWAYS)


def StartThread():
	tSrv = lx.service.Thread()
	tSrv.InitThread()
	global threadServer
	threadServer = ms_Init(ms_asset_importer)
	threadServer.daemon = True
	threadServer.start()
	

	pSrv = lx.service.Platform()
	vis = visIdle()
	com_visitor = lx.object.Unknown(vis)
	pSrv.TimerStart(com_visitor, interval, lx.symbol.iUSERIDLE_ALWAYS)
	tSrv.CleanupThread()

def StopThread():
	global threadServer
	threadServer.stopThread = True
	threadServer = None
	print "Stopping Quixel Bridge."


class StartBridgeCMD(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
	def cmd_Flags(self):
		return 0
	def basic_Enable(self, msg):
		return True
	def basic_Execute(self, msg, flags):
		print "Starting Quixel Bridge"
		StartThread()

class StopBridgeCMD(lxu.command.BasicCommand):
	def __init__(self):
		lxu.command.BasicCommand.__init__(self)
	def cmd_Flags(self):
		return 0
	def basic_Enable(self, msg):
		return True
	def basic_Execute(self, msg, flags):
		StopThread()

 
lx.bless(StartBridgeCMD, "quixelBridge.start")
lx.bless(StopBridgeCMD, "quixelBridge.stop")







