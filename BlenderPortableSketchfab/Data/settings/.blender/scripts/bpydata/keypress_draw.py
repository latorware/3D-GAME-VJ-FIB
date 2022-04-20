# SPACEHANDLER.VIEW3D.DRAW
import Blender
from Blender import BGL

#BGL.glBegin(BGL.GL_LINES)
#BGL.glVertex3f(0.0, 10.0, 20.0)
#BGL.glVertex3f(0.0,  20.0, 0.0)
#BGL.glEnd()

def StatusDraw(keystring):
	 if keystring:
		 BGL.glMatrixMode(BGL.GL_MODELVIEW)
		 BGL.glPushMatrix()
		 BGL.glLoadIdentity()
		
		 wsx,wsy = Blender.Window.GetAreaSize()
		 len = Blender.Draw.GetStringWidth(keystring,"large")
		
		 left = wsx - len - 10
		 top = wsy - 15
		 bottom = wsy-45
		 right = wsx -2
		 #shadow
		 Blender.BGL.glColor4f(0.1,0.1,0.1,0.50)
		 Blender.BGL.glRecti(left, top, right, bottom)
		 
		 #fill
		 Blender.BGL.glColor4f(0.278,0.031,0.125,0.10)
		 Blender.BGL.glRecti(left + 2 , top -2, right - 2 , bottom +2)
				
		 #Text
		 Blender.BGL.glColor3f(1,1,1)
		 Blender.BGL.glRasterPos2i(left +5, top - 20 )
		 Blender.Draw.Text(keystring, "large")
			 
		 BGL.glMatrixMode(BGL.GL_MODELVIEW)
		 BGL.glPopMatrix() 

StatusDraw(Blender.keypress)
