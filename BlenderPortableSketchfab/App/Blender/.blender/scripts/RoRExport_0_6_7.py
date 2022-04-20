#!BPY

""" Registration info for Blender menus:
Name: 'RoR Exporter 0.6.7 (.truck,.load,.trailer,.boat,.airplane,.car)...'
Blender: 240
Group: 'Export'

Tip: 'Export truck RoR Trucks.'
"""
# date format: (DD/MM/YYYY)
# version 0.1.0 - 05/03/2007  by Thomas Fischer, thomas@thomasfischer.biz
# version 0.2.0 - 06/03/2007  thomas: added submesh export support
# version 0.3.0 - 06/03/2007  thomas: added submesh export support
# version 0.4.0 - 08/03/2007  thomas: added texture UV mapping export support
# version 0.5.0 - 08/03/2007  thomas: added RoRSettings support
# version 0.5.1 - 08/03/2007  thomas: small fixes
# version 0.5.2 - 09/03/2007  thomas: added comments export, fixed line ending bug
# version 0.5.4 - 20/05/2007  thomas: fixed line ending export bug
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


import os, os.path
import Blender
from Blender import NMesh,Object,Material,Texture,Image,Draw,Window,Registry
from RoRUtils_0_6_7 import *

__version__ = "0.6.7"

class RORExport:
	img = None
	def __init__(self, filename):
		self.filename = filename
		self.sectiontitles = getSectionTitles()
		self.settings = loadSettings()

	def getSection(self, title, lines):
		res = []
		record = False
		for line in lines:
			if line.strip() == title:
				record = True
				continue
			if line.strip() in self.sectiontitles and record:
				record = False
				return res
			if record:
				res.append(line.strip())
		return res
		
	def findSubmeshGroup(self,faceid):
		groups = None
		try:
			groups = self.settings['submeshgroups']
			sgcounter = 0
			for sgkey in groups:
				sgcounter += 1
				if faceid in groups[sgkey]:
					return sgkey
			# return new id, so open a new group, if not found
			return sgcounter + 1
		except:
			print "submeshgroups not found in settings!"
		# return 0 if no uv
		return 0

	def Export(self):
		debug = False
		objs = Object.GetSelected()
		if len(objs) < 1:
			print "please select one object to be exported! export failed."
			popup("error occured during export", "please select one object to be exported!\n export failed.")
			return
		if len(objs) > 1:
			popup("error occured during export", "please select only one object to be exported!\n export failed.")
			print "please select only one object to be exported! export failed."
			return
		obj = objs[0]
		objname = obj.getName()
		
		mode = 'normal'
		if objname.find('mnormal') != -1:
			mode='normal'
		elif objname.find('msubmesh') != -1:
			mode='submesh'
		elif objname.find('mwings') != -1:
			mode='wings'
		
		if obj.type == 'Mesh':
			mesh = obj.data
			
			if mode == 'normal':			
				progressmsg(0.1, "processing %d nodes..." % len(mesh.verts))
				nodes = []

				# adding -1 comment :/
				if not self.settings is None:
					try:
						nodes.append(self.settings['comments']['nodes'][-1])
					except:
						pass
				for v in mesh.verts:
					(x,y,z) = v.co
					option = 'n'
					# try to get options
					if not self.settings is None:
						try:
							option = self.settings['nodes'][v.index]
						except:
							print "option for node %d not found in settings!" % v.index
							option = None
						if option is None:
							# re - add default option
							option = 'n'
						option = option.strip()
					nodes.append("%d, %f, %f, %f, %s" % (v.index, y, z, x, option))
					# try to write comments
					if not self.settings is None:
						try:
							for ckey in self.settings['comments']['nodes']:
								if str(ckey) == str(v.index):
									nodes.append(self.settings['comments']['nodes'][ckey])
						except:
							continue

				progressmsg(0.3, "processing %d beams..." % len(mesh.edges))
				beams = []
				beamcounter = 0
				#1st: add beam options
				if not self.settings is None:
					try:
						for beamline in self.settings['beamoptions']:
							beams.append(beamline)
					except:
						popup("error occured during export", "error while adding beam-options")
						print "error while adding beam-options"

				#now add the beams itself
				for e in mesh.edges:
					beamcounter += 1
					option = 'v'
					edgename = getBeamID(e.v1.index,e.v2.index)
					# try to write comments
					if not self.settings is None:
						try:
							for ckey in self.settings['comments']['beams']:
								if str(ckey) == str(beamcounter):
									beams.append(self.settings['comments']['beams'][ckey])
						except:
							continue
					if not self.settings is None:
						try:
							option = self.settings['beams'][edgename]
						except:
							print "option for beam %s not found in settings!" % edgename
							option = None
						if option is None:
							# re - add default option
							option = 'i'
						option = option.strip()
					#beams.append("%-4s %4d, %s  ; beam number %03d" % (str(e.v1.index)+',', e.v2.index, option, beamcounter))
					beams.append("%d, %d, %s" % (e.v1.index, e.v2.index, option))
				beams.append("")


				submeshs = {}
				try:
					breakcounter = 0
					progressmsg(0.4, "pre-processing faces")
					for f in mesh.faces:
						if len(f.v) == 4:
							# break up into two triangle faces
							breakcounter += 1
							print "breaking up 4-lenght face:"
							print f.v
							newface = NMesh.Face()
							newface.v.append(f.v[2])
							newface.v.append(f.v[3])
							newface.v.append(f.v[0])
							del f.v[3]
							if len(f.uv) == 4:
								newface.uv.append(f.uv[2])
								newface.uv.append(f.uv[3])
								newface.uv.append(f.uv[0])
								del f.uv[3]
							mesh.faces.append(newface)
					if breakcounter > 0:
						popup("export notice", "%d faces were broken up in triangles!" % breakcounter)
				except:
					print "error while breaking up faces"
			
			if mode in ['normal', 'submesh']:
				progressmsg(0.6, "processing faces")
							
				facemapping = {}
				for f in mesh.faces:
					fid=getFaceID(f.v[0].index, f.v[1].index, f.v[2].index)
					facemapping[fid] = f
				
				faces = {}
				alreadyconnected = []
				for f in mesh.faces:
					fid=getFaceID(f.v[0].index, f.v[1].index, f.v[2].index)
					#if fid in alreadyconnected:
					#	continue
					connectedwith = []
					for i in range(0,len(f.uv)):
						u = f.uv[i][0]
						v = f.uv[i][1]
						for fa in mesh.faces:
							fida=getFaceID(fa.v[0].index, fa.v[1].index, fa.v[2].index)
							if fida == fid:
								# ignore self
								continue

							connected = False
							for ia in range(0,len(f.uv)):
								ua = fa.uv[ia][0]
								va = fa.uv[ia][1]
								if abs(ua-u) < 0.001 and abs(va-v) < 0.001:
									connected=True
									break
							if connected:
								#print "connected"
								connectedwith.append(fida)
								alreadyconnected.append(fida)
					faces[fid] = connectedwith
					if debug:
						print "face " + str(fid) + " connected with: " + str(len(connectedwith)) + " other faces: " + str(connectedwith)
				
				# splitting up into groups
				if debug:
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
					print "XXX faces"
					for k in faces.keys():
						print k, faces[k]
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
				groups = []
				print "grouping..."
				for k in faces.keys():
					if debug:
						print "grouping " + str(k)
					existing=False
					for group in groups:
						if k in group:
							for f in faces[k]:
								if not f in group:
									group.append(f)
							existing=True
							break
					if not existing:
						if debug:
								print "not existing:" +str(faces[k])
						faces[k].append(k)
						groups.append(faces[k])
					else:
						if debug:
							print "existing"
				
				if debug:
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
					print "XXX groups, before merging"
					for g in groups:
						print g
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
						
				#resorting:
				mergeloop=True
				mergecount=0
				print "merging groups..."
				while(mergeloop):
					mergecount+=1
					mergeloop=False
					for a in range(0, len(groups)):
						ga=groups[a]
						for el in ga:
							for b in range(0, len(groups)):
								gb=groups[b]
								if a == b:
									continue
								if el in gb:
									# found, merge them
									mergeloop=True
									for elb in gb:
										if elb != el:
											ga.append(elb)
									groups.remove(gb)
									break
							if mergeloop:
								break
						if mergeloop:
							break
				print "merging done, %d merges" % mergecount
						
				if debug:
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
					print "XXX groups, after merging"
					for g in groups:
						print g
					print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

				facelines=[]
				for group in groups:		
					# build texture coordinates
					textcoords = {}
					for face in group:
						vert = facemapping[face]
						for i in range(0, len(vert.uv)):
							u = vert.uv[i][0]
							v = -(vert.uv[i][1]-1)
							textcoords[vert.v[i].index]= (u, v)

					# build triangle definitions
					triangles = []
					for face in group:
						vert = facemapping[face]
						val = (vert.v[0].index, vert.v[1].index, vert.v[2].index)
						if not val in triangles:
							triangles.append(val)
					
					# build lines finally
					facelines.append("submesh")
					facelines.append("texcoords")
					for kt in textcoords.keys():
						line = "%d, %1.6f, %1.6f" % (kt, textcoords[kt][0], textcoords[kt][1])
						facelines.append(line)
					
					facelines.append("cab")				
					for tri in triangles:
						option = 'n'
						faceid = getFaceID(tri[0], tri[1], tri[2])
						if not self.settings is None:
							try:
								option = self.settings['capoptions'][faceid]
							except:
								option = 'n'
						line = "%d, %d, %d, %s" % (tri[0], tri[1], tri[2], option)
						facelines.append(line)
					facelines.append("")
				#print facelines
				
			if mode == 'wings':
				progressmsg(0.6, "processing wings")
				winglines = []
				facedata = []
				storedface = None
				counter = 0
				for face in mesh.faces:
					if storedface is None:
						# only use every 2nd face!
						storedface = face
					else:
						data = (storedface.v[0], storedface.v[1], storedface.v[2], face.v[0], face.v[1], face.v[2], storedface.uv[0], storedface.uv[1], storedface.uv[2], face.uv[0], face.uv[1], face.uv[2])
						facedata.append(data)
						storedface=None
						counter +=1
						print "parsed wing %d ..." % counter

				print "got %d wings" % len(facedata)
						
				infile = open(self.filename,'r')
				lines = infile.readlines()
				infile.close()
				
				lines=self.getSection('wings', lines)
				for i in range(0, len(lines)):
					if len(lines[i]) == 0 or lines[i][0] == ';':
						winglines.append(lines[i])
						continue
					wing = lines[i].split(',')
					
					if len(wing) < 15:
						winglines.append(lines[i])
						continue
					
					# XXX: TODO: fix that damn bug, that the last wing is forgotten always
					if i >= len(facedata) or len(facedata[i]) < 12:
						continue
					print i, len(wing), len(facedata[i])
					
					wing[2]=str(facedata[i][0].index)
					wing[6]=str(facedata[i][1].index)
					wing[3]=str(facedata[i][2].index)			
					wing[3]=str(facedata[i][3].index)
					wing[6]=str(facedata[i][4].index)
					wing[7]=str(facedata[i][5].index)

					# 1st face
					wing[8]="%0.4f" % (facedata[i][6][0])
					wing[9]="%0.4f" % (1-facedata[i][6][1])
					
					wing[12]="%0.4f" % (facedata[i][7][0])
					wing[13]="%0.4f" % (1-facedata[i][7][1])
					
					wing[10]="%0.4f" % (facedata[i][8][0])
					wing[11]="%0.4f" % (1-facedata[i][8][1])

					# 2nd face
					wing[10]="%0.4f" % (facedata[i][9][0])
					wing[11]="%0.4f" % (1-facedata[i][9][1])
					
					wing[12]="%0.4f" % (facedata[i][10][0])
					wing[13]="%0.4f" % (1-facedata[i][10][1])
					
					wing[14]="%0.4f" % (facedata[i][11][0])
					wing[15]="%0.4f" % (1-facedata[i][11][1])
					print wing
					newline = ','.join(wing)
					winglines.append(newline)
					
				
				
			#if len(mesh.verts) > 1024:
			#	print "!!! ROR WILL CRASH WITH > 1024 NODES PER OBJECT!"
			#	popup("export notice", "ROR WILL CRASH WITH > 1024 NODES PER OBJECT")

			progressmsg(0.8, "preprocessing input file")
			infile = open(self.filename,'r')
			lines = infile.readlines()
			infile.close()

			res = []
			cutout = False
			submeshtitlecount = 0
			for line in lines:
				if line.strip() in self.sectiontitles and cutout:
					cutout = False

				if line.strip() == "submesh" and cutout == False and (mode == 'normal' or mode == 'submesh'):
					# because sumesh can occur several times in the file
					# but we only want one anchor remaining
					if submeshtitlecount == 0:
						submeshtitlecount += 1
						res.append(line.strip())
					cutout = True
				
				stripsections=[]
				if mode == 'normal':
					stripsections=["nodes", "beams"]
				elif mode == 'wings':
					stripsections=["wings"]
				
				if line.strip() in stripsections and cutout == False:
					res.append(line.strip())
					cutout = True
				if not cutout:
					res.append(line.strip())
			lines = res

			# debug: output empty template
			#writeFile(self.filename+"_empty", lines)
			progressmsg(0.9, "constructing data")

			res = []
			# ok, original nodes and beams and meshes should be gone
			# construct the new data now
			nodes_ok = False
			beams_ok = False
			submesh_ok = False
			wings_ok = False
			for line in lines:
				if line.strip() == "nodes" and mode == 'normal':
					nodes_ok = True
					res.append(line)    # leave nodes tag there
					for n in nodes:
						res.append(n)
				elif line.strip() == "beams" and mode == 'normal':
					beams_ok = True
					res.append(line)    # leave beams tag there
					for b in beams:
						res.append(b)
				elif line.strip() == "submesh" and (mode == 'normal' or mode =='submesh'):
					submesh_ok = True
					for line in facelines:
						res.append(line)
				elif line.strip() == "wings" and mode == 'wings':
					wings_ok = True
					res.append(line)    # leave wings tag there
					for line in winglines:
						res.append(line)
				else:
					res.append(line)
			lines = res

			if not nodes_ok and mode == 'normal':
				print "nodes section in the file not found, so no node is exported."
				popup("export notice", "nodes section not found, no nodes exported")
			if not beams_ok and mode == 'normal':
				print "beams section in the file not found, so no beam is exported."
				popup("export notice", "beams section not found, no beams exported")
			#if not submesh_ok and (mode == 'normal' or mode == 'submesh'):
			#	#print "submesh section in the file not found, so no submesh is exported."
			#	#popup("export notice", "submesh section not found, no submeshs exported")
			if submesh_ok:
				txtw="please use flexbodies for visual aspects.\n Submesh support is just in here for physical and historical reasons.\n It is known that the UV mapping still contains bugs.\n"
				popup("NOTICE", txtw)
				print txtw

			if not wings_ok and mode == 'wings':
				print "wings section in the file not found, so no wings are exported."
				popup("export notice", "wings section not found, no wings exported")

			writeFile(self.filename, lines)
			progressmsg(1, "exporting finished!")

		else:
			popup("error occured during export", "the selected object is not a mesh! export failed.")
			return

def createBackup(filename):
	print "we will make a backup to be sure :)"
	import time
	nfn = filename+"_"+str(int(time.time()))
	print "backup file: %s" % nfn
	infile = open(filename, "r")
	outfile = open(nfn, "w")
	outfile.write(infile.read())
	infile.close()
	outfile.close()

def my_callback(filename):
	#if not filename.lower().endswith('.truck') or filename.lower().endswith('.load'):
	#	popup("notice", " %s is not a .truck or .load file, i hope you know what you do!" % filename)
	#	print "Not a .truck or .load file"
	createBackup(filename)
	rorexport = RORExport(filename)
	rorexport.Export()

arg = __script__['arg']

if __name__ == '__main__':
	if pythoncheck():
		Blender.Window.FileSelector(my_callback, "Export RoR Trucks", "*.truck,*.load")
