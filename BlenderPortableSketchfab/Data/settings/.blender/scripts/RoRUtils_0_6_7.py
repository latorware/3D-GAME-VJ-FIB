# date format: (DD/MM/YYYY)
# version 0.5.4 - 20/05/2007  thomas: fixed line ending export bug
# version 0.5.5 - 20/05/2007  thomas: fixed export without UV coords bug
# version 0.5.7 - 23/05/2007  thomas: fixed export bug with submeshes regarding textures
# version 0.6.0 - 09/02/2008  thomas: improved script: added support for hidden/normal beams as well as some other nice stuff (see wiki)
# version 0.6.1 - 11/02/2008  thomas: improved submesh grouping
# version 0.6.2 - 11/02/2008  thomas: fixed some bugs, fixed texture loading, added mass import
# version 0.6.3 - 12/02/2008  thomas: bugfixes
# version 0.6.4 - 11/03/2008  thomas: fixed submesh double export bug
# version 0.6.5 - 22/05/2008  thomas: simplified: removed all except the main layer
# version 0.6.6 - ?
# version 0.6.7 - 16/06/2008  thomas: added new sections

import Blender
from Blender import NMesh,Object,Material,Texture,Image,Draw,Window,Registry

def pythoncheck():
	print "checking for python..."
	try:
		import pickle
		print "python is fine!"
		return True
	except:
		print "python not found! please install python."
		print "You will need the correct python version that fits to your blender python api version."
		print "For Blender 2.43 you will need python 2.4.x from http://www.python.org/"
		print "Please install python and try again."
		msg = []
		msg.append("This script needs python!")
		msg.append("Install python before using.")
		Blender.Draw.PupBlock("Python not found!", msg)
		return False

def progressmsg(per, msg):
	Window.DrawProgressBar (per, msg)
	print msg

def popup(title,msg2):
	block = []
	lines = msg2.split('\n')
	blocks = []
	for line in lines:
		if len(line)>399:
			line=line[0:398]
		text = Blender.Draw.Create(line)
		blocks.append(("Message: ", text, 0, 240, line))
	return Blender.Draw.PupBlock(title, blocks)

def saveSettings(forfile, settings):
	import pickle, tempfile, os.path
	try:
		from Blender import Text
		txt = Text.New("BeamSettings")
		#(fid, filename) = tempfile.mkstemp()
		txt.write(pickle.dumps(settings))
		print "saving as Blender Text successfull!"
	except:
	    print "error while saving settings"

"""
	#old version:
	import pickle, tempfile, os.path
	#(fid, filename) = tempfile.mkstemp()
	filename = forfile + ".beamsettings"
	print "trying to save Settings to file %s for file %s" % (filename, os.path.basename(forfile))
	#try:
	fh = open(filename, 'w')
	pickle.dump(settings, fh)
	fh.close()
	rorsettings = {'tempfile':filename, 'forfile': forfile}
	Registry.SetKey('RoRSettings', rorsettings, True)
	print "saving successfull!"
	#except:
	#    print "error while saving settings"
"""

def loadSettings():
	import pickle, os.path
	print "trying to load Blender Text"
	try:
		settings = None
		from Blender import Text
		txt = Text.Get("BeamSettings")
		if txt:
			num = txt.getNLines()
			if num == 0:
				print "no lines found!"
				return
			content=""
			for line in txt.asLines():
				content+=line+"\n"
			settings = pickle.loads(content)
			return settings
		else:
			print "error getting blender text"
	except:
		print "error while loading settings"
"""
	#old version:
	import pickle, os.path
	settings = None
	rorsettings = None
	try:
		rorsettings = Registry.GetKey('RoRSettings', True)
	except:
		rorsettings=None
		print "error loading RoRSettings"
	if rorsettings is None:
		return None
	filename = str(rorsettings['tempfile'])
	print "trying to load Settings from file %s" % filename
	if not os.path.isfile(filename):
		print "%s is not a file" % filename
		filename = os.path.basename(filename)
		print "trying to load Settings from file %s" % filename
		if not os.path.isfile(filename):
			print "%s is not a file" % filename
			return
	try:
		fh = open(filename,"r")
		settings = pickle.load(fh)
		fh.close()
		print "successfull load Settings for file %s" % (os.path.basename(str(rorsettings['forfile'])))
		return settings
	except:
		print "error while loading settings"
"""
def dumpsettings(settings):
	print "############################################################"
	print "dumping Settings:"
	print "############################################################"
	for skey in settings:
		print "============================================================"
		print "%s: (%d)" %(str(skey), len(settings[skey]))
		if type(settings[skey]) == type({}):
			print "------------------------------------------------------------"
			for skey2 in settings[skey]:
				print "%10s: %s" %(str(skey2), str(settings[skey][skey2]))
		else:
			print settings[skey]
	print "############################################################"

def getFaceID(v1,v2,v3):
	v = [int(v1),int(v2),int(v3)]
	#v.sort()
	return (str(v[0]).strip()+"_"+str(v[1]).strip()+"_"+str(v[2]).strip())

def getBeamID(b1,b2):
	b = [int(b1),int(b2)]
	b.sort()
	return (str(b[0])+"_"+str(b[1]))

def writeFile(filename, lines):
	outfile = open(filename,'w')
	for line in lines:
		outfile.write(line.strip()+"\n")
	outfile.close()

def formatFloat(floatnumber):
	return "%3.10f" % floatnumber

def formatInt(intnumber):
	return "%d" % intnumber

def readFile(filename):
	infile = open(filename,'r')
	res = infile.readlines()
	infile.close()
	return res

def getSectionTitles():
	return ['beams', 'submesh', 'cameras', 'cinecam',
			'wheels', 'wheels2', 'meshwheels', 'hydros','shocks','props', 'ropables', 'commands', 'commands2', 'commandlist', 
			'help', 'ropes', 'ties', 'contacters', 'flares', 'hydros', 'fixes', 'minimass', 'ropables2', 'particles', 'rigidifiers', 'hookgroup',
			'gripnodes', 'flexbodies', 'exhausts', 'wings', 'end', 'exhausts', 'comment', 'guisettings', 'airbrakes', 'turboprops', 'fusedrag',
			'turboprops2', 'pistonprops', 'turbojets', 'screwprops']

def getInitialSettings():
	return {'nodes':None,
			'beams':None,
			'beamoptions':None,
			'comments':None, #contains comments for beams and notes
			'submeshgroups':None, 
			'submeshgroupsoptions':None,
			'submeshgroupscomments':None, #contains comments for the submeshgroups
			'capoptions':None,
		   }

