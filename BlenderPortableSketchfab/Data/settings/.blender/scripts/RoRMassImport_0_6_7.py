#!BPY

""" Registration info for Blender menus:
Name: 'RoR Mass Importer 0.6.7 (.truck,.load,.trailer,.boat,.airplane,.car)...'
Blender: 240
Group: 'Import'

Tip: 'Import All RoR trucks'
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

import RoRImport_0_6_7

import os.path, glob
import Blender
from Blender import NMesh,Object,Material,Texture,Image,Draw,Window,Registry
import glob
#import xmlrpclib

__version__ = "0.6.7"

truckfile = None
def run():
	global truckfile
	in_emode = Window.EditMode()
	if in_emode:
		Window.EditMode(0)
	
	files = []
	exts = ['*.truck', '*.load', '*.airplane', '*.trailer', '*.car', '*.boat']
	for ext in exts:
		for file in glob.glob(os.path.join(os.path.dirname(truckfile), ext)):
			files.append(file)
	
	space=5
	x=0
	for f in files:
		print "importing %s" % f
		rorimport = RoRImport_0_6_7.RORImport(f, (x, 0, 0))
		rorimport.Import()
		x+=space
	if in_emode:
		Window.EditMode(1)

arg = __script__['arg']
def my_callback_for_truck(filename):
	global truckfile
	truckfile = filename
	run()

if __name__ == '__main__' and PythonOK:
	Blender.Window.FileSelector(my_callback_for_truck, "Import All RoR Trucks", "*.truck,*.load")
