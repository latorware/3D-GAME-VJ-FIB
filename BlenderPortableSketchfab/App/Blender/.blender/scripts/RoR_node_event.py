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
#-------------------------------------- -------------------------------
# getNodesBeams function by Thomas Fisher (www.rigsofrods.com):
#     - Thomas Fischer, 10th of June 2007
#     - updated on 11th of March 2008: added face display and number to display 
#
# Modified by Lepes, 04-29-2010:
# - no need to change from Object Mode to Edit mode to update messages (just move your mouse more than 10 pixels)
# - Removed background of getNodesBeams and changed text colors 
# - Update messages and positions (was overlapping with 3D View name ( "Top View (ortho)" )
# - swithching to object Mode hide all messages

# INSTALLATION
# - place keypress_event.py and keypress_draw.py on any folder you want.
# - open blender and choose a "Text Editor" window
# - load both files (File -> Open)
# - switch to any 3D window ( perspective or ortho)
# - View menu -> space handler Scripts (click on both scripts)
# - select a mesh, go to Edit Mode and select some vertex, edges or faces.
#    Be sure to move your mouse 10 pixels to update screen messages

import Blender
import string
from Blender import Draw, Registry, Window, Object, Scene, Mesh, BGL

def getNodesBeams():
	id = Window.GetAreaID()
	view3ds = Window.GetScreenInfo(Window.Types.VIEW3D)
	for view in view3ds:
		if view['id'] == id:
			x, y, xmax, ymax = view['vertices']
			w, h = (xmax - x), (ymax - y) # w, h = Window.GetAreaSize()
	 
	statusverts = ""
	selectedverts = []
	 
	statusedges = ""
	selectededges = []
	 
	statusfaces = ""
	selectedfaces = []
	 
	obj = Object.GetSelected()
	if len(obj) > 0: 
		obj = obj[0]
		if obj.getType() == "Mesh":
			obj = Mesh.Get(obj.getData(True, False))
			if len(obj.verts) > 1500: return "more than 1500 node numbers to paint"
			for i in obj.verts:
				if i.sel:
					selectedverts.append(str(i.index))
			if len(selectedverts) > 0 and len(selectedverts) <= 20:
				statusverts = "nodes (%d): %s" % (len(selectedverts), ", ".join(selectedverts))
			elif len(selectedverts) > 20:
				statusverts = "nodes (%d)." % (len(selectedverts))
			elif len(selectedverts) == 0:
				statusverts = ""

			for e in obj.edges:
				if e.sel:
					selectededges.append(str(e.index))
			if len(selectededges) > 0 and len(selectededges) <= 20:
				statusedges = "beams (%d): %s" % (len(selectededges), ", ".join(selectededges))
			elif len(selectededges) > 20:
				statusedges = "beams (%d)." % len(selectededges)
			elif len(selectededges) == 0:
				statusedges = ""
		 
			for e in obj.faces:
				if e.sel:
					selectedfaces.append(e)
			if len(selectedfaces) > 0 and len(selectedfaces) <= 20:
				faces=[]
				for f in selectedfaces:
					s = "%d_%d_%d" % (f.v[0].index, f.v[1].index, f.v[2].index)
					faces.append(s)
				statusfaces = "faces (%d): %s" % (len(selectedfaces), ", ".join(faces))
			elif len(selectedfaces) > 20:
				statusfaces = "faces (%d)." % len(selectedfaces)
			elif len(selectedfaces) == 0:
				statusfaces = ""
	else:
		statusverts = "selected non mesh:"
		statusedges = " %s" % str(obj)
		statusfaces = ""
	return statusverts +'|' + statusedges + '|' + statusfaces

qualifiers = (	
				Blender.Draw.LEFTCTRLKEY, Blender.Draw.RIGHTCTRLKEY,
				Blender.Draw.LEFTSHIFTKEY, Blender.Draw.RIGHTSHIFTKEY,
				Blender.Draw.LEFTALTKEY, Blender.Draw.RIGHTALTKEY
			  )

def nodeCompose(key):
	wasEditMode = Window.EditMode()	
	if wasEditMode:
		Window.EditMode(0)
		Blender.nodekeypress = getNodesBeams()
		Window.EditMode(1)
	else:
		Blender.nodekeypress = ""
	Blender.Redraw()
	Blender.nodeodo = 0



if not hasattr(Blender, 'nodeodo'): Blender.nodeodo = 0 # odometer
evt = Blender.event
Blender.nodeodo += 1
if not evt in qualifiers and Blender.nodeodo > 10: 
	try:
		nodeCompose(1)
	except:
		pass # event not in keymap

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