#!BPY

""" Registration info for Blender menus:
Name: 'RoR Importer 0.6.7 (.truck,.load,.trailer,.boat,.airplane,.car)...'
Blender: 240
Group: 'Import'

Tip: ' RoR trucks'
"""
# date format: (DD/MM/YYYY)
# version 0.1.0 - 05/03/2007  by Thomas Fischer, thomas@thomasfischer.biz
# version 0.2.0 - 06/03/2007  no changes
# version 0.3.0 - 06/03/2007  thomas: added submesh import
# version 0.4.0 - 08/03/2007  thomas: added texture UV mapping import support
# version 0.5.0 - 08/03/2007  thomas: added RoRSettings support
# version 0.5.1 - 08/03/2007  thomas: fixed import bug
# version 0.5.2 - 09/03/2007  thomas: added comments import
# version 0.5.4 - 20/05/2007  thomas: fixed line ending export bug, added popups
# version 0.5.5 - 20/05/2007  thomas: fixed export without UV coords bug
# version 0.5.6 - 21/05/2007  thomas: fixed export bug with submeshes regarding comments
# version 0.5.7 - 23/05/2007  thomas: fixed export bug with submeshes regarding textures
# version 0.6.0 - 09/02/2008  thomas: improved script: added support for hidden/normal beams as well as some other nice stuff (see wiki)
# version 0.6.1 - 11/02/2008  thomas: improved submesh grouping
# version 0.6.2 - 11/02/2008  thomas: fixed some bugs, fixed texture loading, added mass import
# version 0.6.3 - 12/02/2008  thomas: bugfixes
# version 0.6.4 - 11/03/2008  thomas: fixed submesh double export bug
# version 0.6.5 - 22/05/2008  thomas: simplified: removed all except the main layer
# version 0.6.6 - ?
# version 0.6.7 - 16/06/2008  thomas: added new sections

PythonOK=True

from RoRUtils_0_6_7 import *
if not pythoncheck():
	PythonOK=False


import os.path
import Blender
from Blender import NMesh,Object,Material,Texture,Image,Draw,Window,Registry
import glob
from truckparser import *
#import xmlrpclib

__version__ = "0.6.8"

class RORImport:
	def __init__(self, filename, position=None):
		global my_path

		print "reading File %s" % filename
		self.textimage = None
		self.filename = filename
		self.position=position

		self.lines = readFile(filename)

		my_path = Blender.sys.dirname(filename)
		self.sectiontitles = getSectionTitles()
		self.settings = getInitialSettings()

	def getSection(self, title= ""):
		""" return a pointer list of consecutive lineOfSection
		"""
		res = []
		foundHeader = False
		for l in self.parser.lines:
			if not foundHeader: foundHeader = l.isHeader and l.section == title
			if foundHeader: #include this line if it is a comment, command too
				if not l.isHeader and (l.section in [ title ,';' ,'set_beam_defaults'] or l.isCommand):
					res.append(l)
		return res

	def getSubMeshs(self):
		res = []
		submeshes = {}
		result = []
		record = False
		smcounter = -1
		for line in self.lines:
			if line.strip() in self.sectiontitles and record:
				record = False
			if line.strip() == "submesh":
				record = True
				smcounter += 1
				submeshes[smcounter] = {}
				submeshes[smcounter]['text'] = []
				submeshes[smcounter]['mesh'] = []
				record = True
				continue
			if line.strip() == "texcoords" and record:
				record = 'text'
				continue
			if line.strip() == "cab" and record:
				record = 'mesh'
				continue
			if line.strip() == "":
				continue
			#if line.strip()[0] == ";":
				#continue
			if record != False and record != True:
				submeshes[smcounter][record].append(line.strip())

		#print "## submeshes: ", submeshes
		return submeshes

	def parseNodeLine(self, nodeline):
		# this is a workaround to make python happy if there is no optional option argument
		res = nodeline.split(',')
		if len(res) == 4:
			res.append(None)
		return res

	def parseTexcoordLine(self, textline):
		return textline.split(',')

	def parseGlobals(self, textlines):
		for line in textlines:
			if line[0] != ';':
				return line.split(',')

	def parseWings(self, line):
		return line.split(',')
				
	def parseBeamLine(self, beamline):
		res = beamline.split(',')
		if len(res) == 2:
			res.append(None)
		return res

	def parseCapLine(self, capline):
		res = capline.split(',')
		if len(res) == 3:
			res.append(None)
		return res

	def my_callback_for_img_name(self,filename):
		self.textimage = filename
		
	def findImageNameForMaterialName(self, material):
		filefilter=os.path.join(os.path.dirname(self.filename),"*.material")
		matfiles=glob.glob(filefilter)
		#print filefilter, matfiles
		texfilename = None
		for file in matfiles:
			print "reading material file %s" % file
			lines = readFile(file)
			found = False
			for line in lines:
				if found and line.strip()[:8] == "texture ":
					texfilename=line.strip()[8:].strip()
					print "found texture in material: %s " % (texfilename)
					break
				if line.strip() == "material %s" % (material):
					print "found fitting material '%s' in file '%s', now searching for texture filename" % (material, file)
					found=True
			if found:
				break
		if texfilename is None:
			print "did not found material!"
			return None
		else:
			texfile=os.path.join(os.path.dirname(self.filename), texfilename)
			if os.path.isfile(texfile) == 0:
				print "texture file '%s' could not be found in the same directory No texture available now." % (texfilename)
				return None
			else:
				return texfile
		

	def Import(self, mode='normal'):
		import time
		print "import!"
		lines = self.lines
		progressmsg(0, "importing into Blender ...")
		scene  = Blender.Scene.GetCurrent()
		mesh = NMesh.GetRaw()
		meshname = str(int(time.time()))+"m"+mode
		NMesh.PutRaw(mesh, meshname, 1)
		img = None
		
		# create some basic vertex groups
		#mesh.addVertGroup('beams_invisible');
		#mesh.addVertGroup('beams_normal');
		#mesh.addVertGroup('command');
		#mesh.addVertGroup('hydro');
		
		#list of vertices to be added to the same vertex group
		vg = {} # { 'vertex group name' : [ list of vertices] }
		
		Blender.Window.WaitCursor(1)
		progressmsg(0.2, "loading texture ...")
		self.parser = rorparser()
		self.parser.parse(self.filename)
		idx = self.parser.sectionStart('globals')
		if idx == -1: print "Error finding globals.... youk!"

		materialname = self.parser.lines[idx].material
		progressmsg(0.22, "found material name: %s ..." % materialname)
		self.textimage = self.findImageNameForMaterialName(materialname)
		
		truckmaterial = Material.New('truckmaterial')               # get a material
		if not self.textimage is None:
			try:
				progressmsg(0.25, "Trying to load image %s as texture" % self.textimage)
				if not os.path.isfile(self.textimage):
					print "%s is not a file!" %self.textimage
					popup("error occured during import", "%s is not a file!" %self.textimage)
					return
				img = Image.Load(self.textimage)            # load an image
			except:
				popup("error occured during import", "error while loading texture!")
				print "error while loading texture!"
				return
			if not img is None:
				trucktexture = Texture.New('trucktexture')             # get texture named 'foo'
				trucktexture.setType('Image')                 # make foo be an image texture
				trucktexture.image = img                      # link the image to the texture
				trucktexture.useAlpha=1
				truckmaterial.setTexture(0, trucktexture)               # set the material's first texture # to be our texture
				progressmsg(0.29, "texture successfully loaded")
			else:
				popup("error occured during import", "error while loading texture (2)!")
				print "error while loading texture (2)!"

		else:
			print "no texture available"

		progressmsg(0.3, "applying material")
		mesh.materials.append(truckmaterial)

		mtextures = truckmaterial.getTextures()
		for mtex in mtextures:
			if not mtex is None:
				mtex.texco = Blender.Texture.TexCo['UV']

		nodes = self.getSection("nodes")
		vertics = {}
		progressmsg(0.4, "processing nodes...")
		if self.settings['comments'] is None:
			self.settings['comments'] = {'nodes':{},'beams':{}}
		self.settings['nodes'] = {}
		vid = -1
		grp = ''
		for node in nodes:
			if node.section == ";" and node.comment_line is not None:
				#self.settings['comments']['nodes'][str(vid)] = nodeline.strip()
				nl = node.comment_line.strip()
				if len(nl) > 1 :
					k = nl[1:30].strip()
					if not vg.has_key(k): vg[k] = []
					grp = k
				continue
			try:
				if node.section == "set_beam_defaults":
					continue
				elif node.section == 'nodes':
					v = NMesh.Vert(node.z, node.x, node.y)
					vertics[node.id] = v
					mesh.verts.append(v)
				if grp !='': vg[grp].append(int(node.id))
			except:
				popup("error occured during import", "error with node line: %s" % node.getTruckLine())
				print "error with node line: %s" % node.getTruckLine()
				continue



		print "MODE: %s" % mode
		
		if mode == 'wings':	
	# arguments:
	#
	# 0	A Front left down node number
    # 1	B Front right down node number
    # 2	C Front left up node number
	# 3	D Front right up node number
	#
    # 4	E Back left down node number
    # 5	F Back right down node number
    # 6	G Back left up node number
    # 7	H Back right up node number
    #
	# 8	Texture X coordinate of the front left of the wing (in the texture defined in "globals")
    # 9	Texture Y coordinate of the front left of the wing (in the texture defined in "globals")
    # 10	Texture X coordinate of the front right of the wing (in the texture defined in "globals")
    # 11	Texture Y coordinate of the front right of the wing (in the texture defined in "globals")
    #
	# 12	Texture X coordinate of the back left of the wing (in the texture defined in "globals")
    # 13	Texture Y coordinate of the back left of the wing (in the texture defined in "globals")
    # 14	Texture X coordinate of the back right of the wing (in the texture defined in "globals")
    # 15	Texture Y coordinate of the back right of the wing (in the texture defined in "globals")
    #
	# 16	Type of control surface: 'n'=none, 'a'=right aileron, 'b'=left aileron, 'f'=flap, 'e'=elevator, 'r'=rudder
    # 17	Relative chord point at which starts the control surface (between 0.5 and 1.0)
    # 18	Minimum deflection of the control surface, in degree (negative deflection)
    # 19	Maximum deflection of the control surface, in degree (positive deflection)
    # 20	Airfoil file to use 
			winglines = self.getSection("wings")
			for wing in winglines:
				try:
					wing = self.parseWings(wingline)
				except:
					popup("error occured during import", "error with wings line: %s" % wingline)
					print "error with wing line: %s" % wingline
					continue
				
				if wing is None or len(wing) < 6:
					continue
				
				#print wingline
				# C-G-D
				face = NMesh.Face()
				face.v.append(vertics[int(wing[2])])
				face.v.append(vertics[int(wing[6])])
				face.v.append(vertics[int(wing[3])])
				face.uv.append( (float(wing[8]), 1-float(wing[9])) )
				face.uv.append( (float(wing[12]), 1-float(wing[13])) )
				face.uv.append( (float(wing[10]), 1-float(wing[11])) )
				face.mode |= Blender.Mesh.FaceModes.TWOSIDE
				if not img is None:
					face.image = img
				mesh.faces.append(face)

				# D-G-H
				face = NMesh.Face()
				face.v.append(vertics[int(wing[3])])
				face.v.append(vertics[int(wing[6])])
				face.v.append(vertics[int(wing[7])])
				face.uv.append( (float(wing[10]), 1-float(wing[11])) )
				face.uv.append( (float(wing[12]), 1-float(wing[13])) )
				face.uv.append( (float(wing[14]), 1-float(wing[15])) )
				face.mode |= Blender.Mesh.FaceModes.TWOSIDE
				if not img is None:
					face.image = img
				mesh.faces.append(face)
				print "added wing segment ..."
				
		else:
			beams = self.getSection("beams")
			for x in beams:
				print x.getTruckLine()
			progressmsg(0.7, "processing beams...")
			beamcounter = 0
			invertexgroup = ''
			for beam in beams:
				beamcounter += 1
				if beam.section == ';':
					beamcounter -= 1
					if beam.comment_line is not None:
						bl = beam.comment_line[0:30]
						print "new group on beams called: ", bl
						vg[bl] = [] #new vertex group
						invertexgroup = bl
					else: 
						invertexgroup = ''
					continue
				try:
					if beam.section == 'beams': 
						list = [beam.first_node, beam.second_node]
						if beam.first_node == beam.second_node: continue
					else: list = None
					if beam.isCommand:
						continue
					elif invertexgroup !='':
						vg[invertexgroup].extend(list)
					if not beam.options is None and beam.options.strip() != "":
						option = beam.options.strip()
						if 'i' in option : 
							if not vg.has_key('beams_invisible'): vg['beams_invisible'] = []
							vg['beams_invisible'].extend(list)
						elif 'v' in option or 'n' in option:
							if not vg.has_key('beams_normal'): vg['beams_normal'] = []
							vg['beams_normal'].extend(list)
						
				except:
					raise
					#popup("error occured during import", "error with beam line: %s" % beamline)
					#print "error with line: %s" % beamline
					
				#EDGEDRAW = Blender.Mesh.EdgeFlags['SELECT']
				"""
				if mode=='submesh':
					if not option is None and option.find('i') == -1:
						edge = mesh.addEdge(vertics[int(a)], vertics[int(b)])
					else:
						edge = None
				else:
				"""
				edge = mesh.addEdge(vertics[beam.first_node], vertics[beam.second_node])
			"""
				if not option is None and not edge is None and mode == 'normal':
					if option.find('i') == -1:
						# we assume visible node then
						edge.flag |= Blender.Mesh.EdgeFlags.SELECT
						try:
							vertlist = [mesh.verts[int(a)], mesh.verts[int(b)]]
							mesh.assignVertsToGroup('beams_invisible', vertlist, 0.5, 'add')
						except:
							pass
					else:						
						edge.flag &= not Blender.Mesh.EdgeFlags.SELECT
						try:
							vertlist = [int(a), int(b)]
							mesh.assignVertsToGroup('beams_normal', vertlist, 0.5, 'add')
						except:
							pass
			"""
			submeshs = self.getSubMeshs()
			#print submeshs
			self.settings['submeshgroupsoptions'] = {}
			self.settings['submeshgroupscomments'] = {}
			self.settings['submeshgroups'] = {}
			submeshgroupcount = 0
			self.settings['capoptions'] = {}
			scounter=0
			for smid in submeshs:
				scounter+=1
				progressmsg(0.8, "submesh %2d %%" % (int(float(scounter)/float(len(submeshs))*100)))
				if not smid in self.settings['submeshgroupscomments'].keys():
					self.settings['submeshgroupscomments'][smid] = []

				self.settings['submeshgroupsoptions'][smid] = '' # + 1 to align with submeshgroups
				#progressmsg(0.8, "submesh texture %2d" % smid)
				texture = {}
				for textline in submeshs[smid]['text']:
					#print textline
					if textline.strip()[0] == ";":
						self.settings['submeshgroupscomments'][smid].append(textline)
						continue
					try:
						n, u, v = self.parseTexcoordLine(textline)
					except:
						popup("error occured during import", "error with textcoord line: %s" % textline)
						print "error with textcoord line: %s" % textline
						continue
					texture[int(n)] = (float(u),1-float(v))
				#progressmsg(0.8, "submesh mesh    %2d" % smid)

				actualsubmeshgroup = []
				for cabline in submeshs[smid]['mesh']:
					#print cabline
					if cabline.strip()[0] == ";":
						self.settings['submeshgroupscomments'][smid].append(cabline)
						continue
					if cabline.strip() == "backmesh":
						self.settings['submeshgroupsoptions'][smid] = 'backmesh'

						#ignore it for the moment
						continue
					try:
						a, b, c, option = self.parseCapLine(cabline)
					except:
						popup("error occured during import", "error with cab line: %s" % cabline)
						print "error with cabline: %s" % cabline
					face = NMesh.Face()
					#print texture[int(a)], texture[int(b)], texture[int(c)]

					# get unique (we hope so) faceid and add it to the current group
					faceid = getFaceID(a, b, c)
					actualsubmeshgroup.append(faceid)
					if not option is None and option.strip() != "":
						option = option.strip()
						self.settings['capoptions'][faceid] = option

					# create face now
					if len(vertics) > 0:
							face.v.append(vertics[int(a)])
							face.v.append(vertics[int(b)])
							face.v.append(vertics[int(c)])

					if len(texture) > 0:
						try:
							face.uv.append(texture[int(a)])
							face.uv.append(texture[int(b)])
							face.uv.append(texture[int(c)])
						except:
							popup("error occured during import", "error with cab line\n (regarding texture): %s" % cabline)
							print "error with cabline (regarding texture): '%s'" % (cabline)
							print "textures: ", texture
							print "vertics: ", vertics
						if not img is None:
							face.image = img
						#face.materialIndex = 0
					if len(vertics) > 0:
						mesh.faces.append(face)
				self.settings['submeshgroups'][submeshgroupcount] = actualsubmeshgroup
				submeshgroupcount += 1
		progressmsg(0.95, "saving RoR settings")
		from Blender import Text
		try:
			txt = Text.Get(meshname)
		except: # :-F
			txt = Text.New(meshname)
		for l in self.parser.lines:
			txt.write(l.getTruckLine() + '\n')
		#dumpsettings(self.settings)
		saveSettings(self.filename, self.settings)

		#try:
		#	s = xmlrpclib.Server('http://localhost:8000')
		#	s.savesettings()
		#except:
		#	pass
		
		Blender.Window.WaitCursor(0)
		progressmsg(1, "finished")

		mesh.hasFaceUV(True)
		#does not work correctly
		mesh.update()
		
		#print "adding mesh to scene: "+meshname
		obj = Blender.Object.New("Mesh", meshname)
		obj.link(mesh)
		# once linked we can add vertex groups
		for k in vg.keys():
			if len(vg[k]) > 0:
				print " group and vertexs ", k, vg[k]
				mesh.addVertGroup(k)
				mesh.assignVertsToGroup(k, vg[k], 0.5, 'add')

		#sce = Blender.Scene.GetCurrent()
		#sce.link(obj)

		#scene.objects.link(object)
		#object = Blender.Object.New("Mesh", meshname)
		#object.link(mesh)
		
		"""
		if mode=='normal':
			object.layers = [1, 2]
		elif mode=='submesh':
			object.layers = [1, 3]
		elif mode=='wings':
			object.layers = [1, 4]
		"""

		# this is for whatever reason not working:
		#if not self.position is None:
		#	obj.setLocation(self.position[0], self.position[1], self.position[2])
		
		#scene = Blender.Scene.GetCurrent()
		#scene.objects.link(object)		
		
		Blender.Redraw(-1)

truckfile = None
#imgfile = None

def run():
	global truckfile, imgfile
	in_emode = Window.EditMode()
	if in_emode:
		Window.EditMode(0)
	if truckfile is None:
		print "you should at least select a truck to import"
		popup("error occured during import", "you should at least select a truck to import")
		return
	rorimport = RORImport(truckfile) #, imgfile)
	rorimport.Import()
	Blender.rorimporter = rorimport
	#rorimport.Import('normal')
	#rorimport.Import('submesh')
	#rorimport.Import('wings')
	if in_emode:
		Window.EditMode(1)

#arg = __script__['arg']

def my_callback_for_truck(filename):
	global truckfile
	#if not filename.lower().endswith('.truck') or filename.lower().endswith('.load'):
	#	print "Not a .truck or .load file, i hope you know what you do!"
	#	popup("notice", " %s is not a .truck or .load file, i hope you know what you do!" % filename)
	#	#return
	truckfile = filename
	#Blender.Window.ImageSelector(my_callback_for_img, "Select Texture", "*.png,*.jpg")
	run()


#def my_callback_for_img(filename):
#	global imgfile
#	imgfile = filename
#	run()

if __name__ == '__main__' and PythonOK:
	Blender.Window.FileSelector(my_callback_for_truck, "Import RoR Trucks", "*.truck,*.load")