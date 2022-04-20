# SPACEHANDLER.VIEW3D.EVENT
#
# 2007 Carsten Wartmann
# Martin Poirier made a nice script out of my hack
#
# The space handler scripts ShowKeys and DrawKeys are showing
# the actual pressed keys in the 3D View.
#
# This is usefull for presentations or video tutorials where the
# key-combinations
# will give some hints whats going on beside the narration.
#
# To use activate the handlers in the View->Space Handler Scripts memu
# The display will be for the 3DView only and need to activated for
# every 3DView you like to see the keypresses.

# Be sure to put keymap.txt in ./blender/scripts/bpydata


"""
Problems/Todo

* BorderSelect in UVFaceSelectMode not working
* Tab and Space not showing
* some functions CTRL-Q, CTRL-W etc. not showing
* while in Transformation (GSR) the script gets no events
* B-B combination (Circle Select) not handled, maybe do the same for
 A-A? Reason: different Eventloop (see above)

"""


import Blender
from Blender import Draw
import string

reloadKeymap = False   
#reloadKeymap = True # f6r debgugging

qualifiers = (	Blender.Draw.LEFTCTRLKEY, Blender.Draw.RIGHTCTRLKEY,
				Blender.Draw.LEFTSHIFTKEY, Blender.Draw.RIGHTSHIFTKEY,
				Blender.Draw.LEFTALTKEY, Blender.Draw.RIGHTALTKEY
			  )

try:
	Blender.keymap
except:
	reloadKeymap = True
	Blender.odo = 0

if reloadKeymap or not Blender.keymap:
	print "reload...."
	Blender.keymap = {}
	f = open(Blender.Get('datadir') + "/keymap.txt", "r")
	for line in f:
		name, code, text = (x.strip() for x in line.split("|"))
		Blender.keymap[int(code)] = text

def Compose(key):
	q = Blender.Window.GetKeyQualifiers()
	keys = []
	if q & 3:
		keys.append(Blender.keymap[Blender.Draw.LEFTSHIFTKEY])
	if q & 12:
		keys.append(Blender.keymap[Blender.Draw.LEFTALTKEY])
	if q & 48:
		keys.append(Blender.keymap[Blender.Draw.LEFTCTRLKEY])
	keys.append(key)
	
	Blender.keypress = " + ".join(keys)
	Blender.Redraw()
	Blender.odo = 0


evt = Blender.event

if evt not in qualifiers:
	try:
		Compose(Blender.keymap[evt])
	except:
		pass # event not in keymap
	
# clear keyfield after some mouse movements
if evt in (Blender.Draw.MOUSEX, Blender.Draw.MOUSEY):
	Blender.odo = Blender.odo + 1
	if Blender.odo > 100:
 		Compose("")

# some testing/debugging lines
#print evt
#print dir(Draw)

# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2007: Carsten Wartmann
#
# this is a modified version by Martin Poirier
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK ***** 
