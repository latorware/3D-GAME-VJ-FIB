# SPACEHANDLER.VIEW3D.DRAW
#
# 2007 Carsten Wartmann
# Martin Poirier made a nice script out of my hack
#
# The space handler scripts ShowKeys and DrawKeys are showing
# the actual pressed keys in the 3D View.


# Modified by Lepes, 04-29-2010

import Blender
from Blender.BGL import *

#BGL.glBegin(BGL.GL_LINES)
#BGL.glVertex3f(0.0, 10.0, 20.0)
#BGL.glVertex3f(0.0,  20.0, 0.0)
#BGL.glEnd()


show ={
'commands':[True, [0.3, 0.9, 0.9, 1]],
'commands2':[True, [0.4, 0.9, 0.9, 1]],
'shocks':[True, [0, 0.5, 0.5, 1]],
'shocks2':[True, [0, 0.6, 0.6, 1]]
}

if not hasattr(Blender, 'nodeodo'):
	Blender.nodeodo = 0 # odometer
	Blender.nodekeypress = ""

def nodeStatusDraw(keystring):
	if keystring:
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()
		
		wsx,wsy = Blender.Window.GetAreaSize()
		lines = keystring.split('|') 
	
		glColor3f(1,1,1)
		top = 35 # don't overlap on window Name
		for l in lines:
			len = Blender.Draw.GetStringWidth(l, "normal")
			glRasterPos2i(10, wsy - top)
			Blender.Draw.Text(l, "normal")
			top += 15
			 
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix() 
nodeStatusDraw(Blender.nodekeypress)


from Blender import Object, Scene, Window, Mathutils, Text

def updateNodes():
	scn = Scene.GetCurrent()
	ob = scn.getActiveObject()
	if ob: 	
		x,y,z = ob.getLocation()
		me = ob.getData(False, True)
		origin = Mathutils.Vector([x, y, z])
		# Get the Window matrix and create a gl Buffer with its data.
		viewMatrix = Window.GetPerspMatrix()
		viewBuff = [viewMatrix[i][j] for i in xrange(4) for j in xrange(4)]
		viewBuff = Buffer(GL_FLOAT, 16, viewBuff)
		
		# Load the Window matrix for gl Drawing.
		glLoadIdentity()
		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadMatrixf(viewBuff)

		if 'rorimporter' in dir(Blender): #truck loaded
			p = Blender.rorimporter.parser
			for section in show.keys():
				if not show[section][0]: continue # don't want to show it
				s = p.sectionStart(section)
				if s!= -1:
					e = p.sectionEnd(section)
					#print section ," start at line ", s, " finisth at line " , e			
					glColor4f(show[section][1][0], show[section][1][1], show[section][1][2], show[section][1][3]) 
					glLineWidth(2)
					for i in range(s,e):
						l = p.lines[i]
						if not l.section in ['commands', 'commands2', 'shocks', 'shocks2']:continue #comments
						if l.first_node is None or l.second_node is None: continue
						if me.verts[l.first_node].hide ==1 or me.verts[l.second_node].hide == 1: continue #these edges are hidden on Blender, don't paint it!
						start = Mathutils.Vector(me.verts[l.first_node].co) + origin
						end =  Mathutils.Vector(me.verts[l.second_node].co) + origin
						#glRasterPos3f(start.x, start.y, start.z)
						glBegin(GL_LINES)
						glVertex3f(start.x, start.y, start.z)
						glVertex3f(end.x, end.y, end.z)
						glEnd()

		#print node numbers
		glColor4f(1,0,0,1)
		if len(me.verts) > 1500: return
		for v in me.verts:
			if v.hide == 1 :continue
			glColor4f(1,1,1,1)
			vv = Mathutils.Vector(v.co) + origin
			if v.sel: 
				glColor4f(1, 1, 0, 0)
			glRasterPos3f(vv.x, vv.y, vv.z + 0.03)
			Blender.Draw.Text(str(v.index),"large")
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix() 
			
if Window.EditMode():
	updateNodes()