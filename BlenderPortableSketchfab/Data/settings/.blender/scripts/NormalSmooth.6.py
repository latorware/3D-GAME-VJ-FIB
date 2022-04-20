#!BPY
"""
Name: 'NormalSmooth'
Blender: 245
Group: 'Mesh'
Tooltip: 'Smooth the selected verts in your mesh'
"""

__author__ = ["macouno"]
__url__ = ("http://www.alienhelpdesk.com")
__version__ = "6"
__bpydoc__ = """\

NormalSmooth

This script uses vertex normals to smooth out a mesh.
It works fastest / best if you run in on only one or two edge loops (selections) at a time.
If you have a larger selected surface the script will get slower and may create a 'dip' in the middle of your selection.

v2: Attempt to get neater end result
v3: Simplified code, can run on an entire mesh now, probably needs more iterations
v4: Switched from iterations to steps to solve the dip issue
v5: Went back to v2 code but did make that work with entire meshes
v6: Made flat surfaces be displaced in their entirety in the v3 code

"""

# ***** BEGIN GPL LICENSE BLOCK *****
#
# Script copyright (C) macouno 2007
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# ***** END GPL LICENCE BLOCK *****
# --------------------------------------------------------------------------

from Blender import Window, Scene, Draw, Mathutils
import BPyMesh

## A couple of global variables
Iterations = 1	#Standard nr of iterations

## A few extra vars
vNew = {}
areas = []
inArea = []


## Get the angle between two vectors
def VtoVAngle(vec1, vec2):
	if (vec1.length == 0.0 or vec2.length == 0.0): return 0.0
	else: return Mathutils.AngleBetweenVecs(vec1, vec2)


## Rotate one vector (vec1) towards another (vec2)
## (deg = ammount of degrees to rotate)
def RotVtoV(vec1, vec2, deg):
	cross = Mathutils.CrossVecs(vec1,vec2)
	mat = Mathutils.RotationMatrix(deg, 3, 'r', cross)
	return (vec1 * mat)


## Get the averase location in a list of locations
def GetAverage(vList):
		v = Mathutils.Vector()
		for m in vList:
			v += m
		v /= len(vList)
		return v


## Get all the verts that have matching normal angles and are connected by faces
def GetConnected(me, v1, matched):

	global areas, inArea

	v1in = v1.index

	# Find faces 
	for f in me.faces:
		if v1 in f.verts:
			for v2 in f.verts:
				v2in = v2.index
				## Make sure the verts arent the same and that v2 isn't already in the area
				if not v1in == v2in and not v2in in inArea:
					
					# If the angle between the normals is 0 we have found a surface!
					if VtoVAngle(v1.no, v2.no) < 0.2:
					
						if not matched:
							matched += 1
							areas.append([v1in, v2in])
							inArea.append(v1in)
							inArea.append(v2in)
						else:
							areas[(len(areas)-1)].append(v2in)
							inArea.append(v2in)
							
						GetConnected(me, v2, 1)


## Find larger areas with matching normals
def GetAreas(me):
	
	global areas, inArea
	areas = []
	inArea = []
	
	## Find a selected vert that isn't in an area
	for v1 in me.verts:
		if v1.sel and not v1.index in inArea:
			GetConnected(me, v1, 0)


## Move the vert relative to it's neighbouring normals
def SmoothVert(me, v1, vCh):

	v1in = v1.index
	v1co = Mathutils.Vector(v1.co)
	vCh.append(v1in)
	vList = []

	for f in me.faces:
		if v1 in f:
			for v2 in f:
				v2in = v2.index
				if not v2in in vCh:
					
					# Since we're checking this vert already, add it to the list of checked verts
					vCh.append(v2in)
					
					v2co = Mathutils.Vector(v2.co)
					
					# Get the vector from one vert to the other
					vTov = v1co - v2co
					
					# Get half the distance from one vert to the other
					vLen = vTov.length * 0.514
					
					# Get the normal rotated 90 degrees towards the original vert
					vNor = RotVtoV(v2.no, vTov.normalize(), 90)
					
					# Make the new rotated normal the hald distance long
					vNor = vNor.normalize() * vLen
					
					# Find the location the vector points at
					vNew = v2co + vNor
				
					vList.append(vNew)
	
	# Go get the average position change and return
	if len(vList):
		return GetAverage(vList)

	return 0


def MainScript(me):

	global vNew, areas, inArea
	vNew = {}
	
	# Get all the areas that have verts with the same normal
	GetAreas(me)
	
	## If there are areas get the new coords for all verts in em
	if len(areas):
		for a in areas:
			vList = []
			coords = {}
			for v in a:
				vert = me.verts[v]
				coords[v] = Mathutils.Vector(vert.co)
				smoothCo = SmoothVert(me, vert, list(a))
				if smoothCo:
					vList.append(smoothCo - coords[v])
				
			## If no new coords were found no need to continue
			if len(vList):
				vN = GetAverage(vList)
				
				for v in a:
					vNew[v] = vN + coords[v]

	# Loop through the non area verts and get the new coords
	for v in me.verts:
		if v.sel and not v.index in inArea:
			vNew[v.index] = SmoothVert(me, v, [])

	# Implement the changes
	if len(vNew):
		for i in vNew.keys():
			if vNew[i]:
				me.verts[i].co = vNew[i]


## Lets get all the actual data we need and see if we can smooth something
def RunSmoothing():

	global Iterations

	scn = Scene.GetCurrent()
	ob = scn.getActiveObject()

	## If the current object is no mesh then we can quit
	if not ob or ob.getType() != 'Mesh':
		Draw.PupMenu('Error, no active mesh object, aborting.')
		return
		
	me = ob.getData(mesh=1)
	del ob
	
	## If the current object is no mesh then we can quit
	if not len(me.faces):
		Draw.PupMenu('Error, no faces found in this mesh object, aborting.')
		return
	
	## Draw the popup menu that sets the number of iterations
	Iterations = Draw.PupIntInput('iterations:', 1, 1, 1000) 
	
	BPyMesh.meshCalcNormals(me)
	for i in range(Iterations):
		if i < Iterations:
			MainScript(me)
			
	me.update()
	scn.update()
	del scn, me

	
## Set up the scene/windows and reset em when done
def  Initialise():

	Window.WaitCursor(1)

	emode = int(Window.EditMode())
	if emode: Window.EditMode(0)

	RunSmoothing()

	Window.Redraw(Window.Types.VIEW3D)
	
	if emode: Window.EditMode(1)
	
	Window.WaitCursor(0)
	
## Initialise the script
Initialise()	