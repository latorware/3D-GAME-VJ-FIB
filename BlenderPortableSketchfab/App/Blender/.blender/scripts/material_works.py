#!BPY

""" Registration info for Blender menus:
Name: 'Material Works'
Blender: 241
Group: 'Materials'
Tooltip: 'Search all objects/faces assigned with material 1 and replace it by material 2, rename materisls, material surface area.'
"""

# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
#
# Copyright (C) 2007 Vaclav Chaloupka
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

__author__ = "Vaclav Chaloupka"
__url__ = ("http:\\blender.chaloupkovi.cz")
__version__ = "1.1"
__bpydoc__ = """
Material Works 1.1

"""

import Blender
from Blender import Mesh, Material, Curve, Metaball
from Blender import *

##change materials in object
def changeObjectMaterial(obj,Mat,toMat):
	materials=obj.getMaterials()
	i=0
	changed=0
	for ma in materials: #cycle through Object materials
		if ma!=None and ma.name==Mat:
			changed+=1
			print " - Replacing (object)"+obj.name+".material["+str(i+1)+"]"
			materials[i]=toMat #CHANGE MATERIAL
		i+=1
	if changed>0:
		obj.setMaterials(materials) #update object
	return changed

##change materials in mesh
def changeMeshMaterial(me,Mat1,toMat):
	nme=NMesh.GetRaw(me.name) #the material must be changed here
	i=0
	changed=0
	for ma in nme.materials: #cycle through mesh materials
		if ma!=None and ma.name==Mat1:
			changed+=1
			print " - Replacing (mesh)"+nme.name+".material["+str(i+1)+"]"
			nme.materials[i]=toMat #CHANGE MATERIAL
		i+=1
	if changed>0:
		nme.update() #update mesh
	return changed

##change materials in curve
def changeCurveMaterial(cu,Mat1,toMat):
	i=0
	changed=0
	mats=cu.materials	 
	for ma in cu.materials: #cycle through curve materials
		if ma!=None and ma.name==Mat1:
			changed+=1
			print " - Replacing (curve)"+cu.name+".material["+str(i+1)+"]"
			mats[i]=toMat #CHANGE MATERIAL
		i+=1
	if changed>0:
		cu.materials=mats
	return changed 

##change materials in metaball
def changeMetaBallMaterial(mb,Mat1,toMat): #same procedure as curve
	i=0;
	changed=0
	mats=mb.materials
	for ma in mb.materials: #cycle through metaball materials
		if ma!=None and ma.name==Mat1:
			changed+=1
			print " - Replacing (metaball)"+mb.name+".material["+str(i+1)+"]"
			mats[i]=toMat #CHANGE MATERIAL
		i+=1
	if changed>0:
		mb.materials=mats
	return changed

##########################################
# replace material1 by material2
##########################################
def replace(Mat1,Mat2):
	global Limit 
	 
	print "Replacing material " +Mat1 + " by " +Mat2
	toMat=Material.Get(Mat2)

	editmode = Window.EditMode()    # are we in edit mode?  If so ...
	if editmode: Window.EditMode(0) # leave edit mode before getting the mesh

	# Change materials
	obj_changed=0
	me_changed=0
	cu_changed=0
	mb_changed=0
	me_array=[]
	cu_array=[]
	mb_array=[]
	layers=Blender.Window.ViewLayers()
	if Limit==3:
		objects = Blender.Object.GetSelected() #cycle through all Selected Objects
	else:
		objects = Blender.Object.Get() #cycle through all Objects
		
	for obj in objects:
		if Limit==2: # is object (layer) visible?
			visible=False
			for l in obj.layers:
				if layers.count(l)>0: visible=True
			if not visible: continue		 
		obj_changed+=changeObjectMaterial(obj,Mat1,toMat)
		data_name=obj.getData(True,False)
		if obj.type=="Mesh": #mesh
			if me_array.count(data_name)==0:
				me_array.append(data_name)
				me=Mesh.Get(data_name)
				me_changed+=changeMeshMaterial(me,Mat1,toMat)
		elif obj.type=="Curve" or obj.type=="Text" or obj.type=="Surf": #curve
			if cu_array.count(data_name)==0:
				cu_array.append(data_name)
				cu=Curve.Get(data_name)
				cu_changed+=changeCurveMaterial(cu,Mat1,toMat)
		elif obj.type=="MBall": #MetaBall
			if mb_array.count(data_name)==0:
				mb_array.append(data_name)
				mb=Metaball.Get(data_name)
				mb_changed+=changeMetaBallMaterial(mb,Mat1,toMat)
			
	msg="Replaced materials in "+str(me_changed)+" meshes, "+str(obj_changed)+" objects, "+str(cu_changed)+" curves and "+str(mb_changed)+" metaballs"
	print msg
	Draw.PupMenu(msg+"%t|Ok")
	
	if editmode: Window.EditMode(1)  # optional, just being nice

##########################################
# rename material
##########################################
def rename(mat1,newname):
	print "Renaming material " +mat1 + " to " + newname
	if mat1==newname:
		Draw.PupMenu("The new and old names are the same!?%t|Ok")
		return
	if Material_array.count(newname)>0:
		Draw.PupMenu("The name already exists!%t|Ok")
		return
	ma=Material.Get(mat1)
	ma.setName(newname)

##########################################
#assign mat to selected objects 
#(replace all materials by mat)
##########################################
def AssignObjects(mat):
	editmode = Window.EditMode()    # are we in edit mode?  If so ...
	if editmode: Window.EditMode(0) # leave edit mode before getting the mesh

	toMat=Material.Get(mat)
	objects=Blender.Object.GetSelected()
	if objects==[]:
		Draw.PupMenu("No selected objects!%t|Ok")
		return
	for obj in objects:
		materials=obj.getMaterials()
		cntobjmat=len(materials)
		i=0
		for m in materials:
			materials[i]=toMat #CHANGE MATERIAL
			i+=1
		obj.setMaterials(materials) #update object
			
		data_name=obj.getData(True,False)		
		if obj.type=="Mesh":
			nme=NMesh.GetRaw(data_name)
			if cntobjmat==0 and len(nme.materials)==0:
				nme.materials+=[toMat]
			else: 
				i=0
				for m in nme.materials: #cycle through mesh materials
					nme.materials[i]=toMat #CHANGE MATERIAL
					i+=1
			nme.update() #update mesh
		elif obj.type=="Curve" or obj.type=="Text" or obj.type=="Surf": #curve
			cu=Curve.Get(data_name)
			mats=cu.materials
			if cntobjmat==0 and len(mats)==0:
				mats+=[toMat]
			else: 
				i=0
				for ma in cu.materials: #cycle through curve materials
					if ma!=None:
						mats[i]=toMat #CHANGE MATERIAL
					i+=1
			cu.materials=mats
		elif obj.type=="MBall": #MetaBall
			mb=Metaball.Get(data_name)
			mats=mb.materials
			if cntobjmat==0 and len(mats)==0:
				mats+=[toMat]
			else: 
				i=0
				for ma in mb.materials: #cycle through curve materials
					if ma!=None:
						mats[i]=toMat #CHANGE MATERIAL
					i+=1
			mb.materials=mats
	if editmode: Window.EditMode(1)  # optional, just being nice

##########################################
#assign mat to selected faces
##########################################
def AssignFaces(mat):
	editmode = Window.EditMode()    # are we in edit mode?  If so ...
	if editmode: Window.EditMode(0) # leave edit mode before getting the mesh

	toMat=Material.Get(mat)
	objects=Blender.Object.GetSelected()
	if objects==[]:
		Draw.PupMenu("No active object!%t|Ok")
		return
	obj=objects[0]
	if obj.type!="Mesh": 
		Draw.PupMenu("Active object is not mesh!%t|Ok")
		return
	me=obj.getData(False,True)
	nme=NMesh.GetRaw(me.name) #the material must be changed here
	#search through mesh materials
	materials=nme.materials
	index=-1
	i=0
	for m in materials:
		if m.name==mat:
			if (obj.colbits & (1 << i)) == 0:
				index=i
		i+=1
	if index<0: #if not found, append material to the list
		nme.materials+=[toMat] #append to mesh material list
		index=i
		
	for f in nme.faces:
		if f.sel==1:
			f.materialIndex=index
	nme.update()

	if editmode: Window.EditMode(1)  # optional, just being nice
	
##########################################
#List objects and meshes using the material
##########################################
def list_users(Mat):
	editmode = Window.EditMode()    # are we in edit mode?  If so ...
	if editmode: Window.EditMode(0) # leave edit mode before getting the mesh
	block=""
	cnt_o=0
	cnt_m=0
	cnt_c=0
	cnt_b=0
	users=[]
	# List Object materials
	objects = Blender.Object.Get() #cycle through the Objects
	for obj in objects:
		materials=obj.getMaterials()
		i=0;
		for ma in materials: #cycle through Object materials
			if ma!=None and ma.name==Mat:
				cnt_o+=1
				users.append(obj.name+"(O)")
			i+=1
	# List Mesh materials
	meshes=Mesh.Get() #cycle through the Meshes
	for me in meshes:
		i=0;
		nme=NMesh.GetRaw(me.name)
		for ma in nme.materials: #cycle through mesh materials
			if ma!=None and ma.name==Mat:
				cnt_m+=1
				users.append(nme.name+"(M)")
			i+=1
	# List Curve materials
	curves=Curve.Get() #cycle through the Curves
	for cu in curves:
		i=0;
		for ma in cu.materials: #cycle through curve materials
			if ma!=None and ma.name==Mat:
				cnt_c+=1
				users.append(cu.name+"(C)")
			i+=1	
	# List Metaball materials
	metaballs=Metaball.Get() #cycle through the Metaballs
	for mb in metaballs:
		i=0;
		for ma in mb.materials: #cycle through curve materials
			if ma!=None and ma.name==Mat:
				cnt_b+=1
				users.append(mb.name+"(B)")
			i+=1

	users.sort()
	for u in users:
		block+="|"+u

	if (cnt_m+cnt_o+cnt_c+cnt_b)>0:
		result=Draw.PupMenu(str(cnt_m)+" Meshes(M) / "+str(cnt_o)+" Objects(O) / "+str(cnt_c)+" Curves(C) / "+str(cnt_b)+" Metaballs(B)%t" + block)
		if result>0:
			choice=users[result-1][:-3]
			tpe=users[result-1][-3:]
			if tpe!="(O)":
				objects = Blender.Object.Get() #cycle through the Objects
				onames=[]
				for obj in objects:
					data_name=obj.getData(True,False)
					if data_name==choice:
						onames.append(obj.name)
				onames.sort()
				block=""
				for o in onames:
					block+="|"+o
				if tpe=="C": stpe="curve"
				elif tpe=="B": stpe="metaball"
				else: stpe="mesh"
				result=Draw.PupMenu("Object(s) using this "+stpe+":%t" + block)
				if result>0:
					choice=onames[result-1]
				else:
					choice=""
			if choice!="":
				result=Draw.PupMenu("Do you want to make object "+choice+" active?:%t|Yes|No")
				if result==1:
					obj=Object.Get(choice)
					scn=Blender.Scene.GetCurrent()
					scn.objects.selected = []
					obj.sel=True
					scn.objects.active=obj
					Draw.Redraw(1)
	else:	
		Draw.PupMenu("Material is not used%t|Ok")
	if editmode: Window.EditMode(1)  # optional, just being nice

##########################################
# Populate material combo boxes (Material1_combo, Material2_combo) and material index (Material_array) 
##########################################
def getMaterials():
	global Material1_combo, Material2_combo, Material_array, Material_count, Rename_to
	
	blocks =  Material.Get() #get all materials
	blocks.sort()
	Material1_combo=""
	Material2_combo=""
	Material_array=[]
	i = 1
	for m in blocks:
		Material1_combo += m.name+" ("+str(m.users)+")" + " %x" + str(i) + "|"
		Material2_combo += m.name+" ("+str(m.users)+")" + " %x" + str(i) + "|"
		Material_array.append(m.name)
		i += 1
	Material_count=i-1

##########################################
#Return area of all faces with material index 
##########################################
def msh_area(msh,mat):
	a=0
	faces=msh.faces
	for f in faces:
		if f.mat==mat:
			a+=f.area
	return a

##########################################
#Calculate material area
##########################################
def area(mat):
	editmode = Window.EditMode()    # are we in edit mode?  If so ...
	if editmode: Window.EditMode(0) # leave edit mode before getting the mesh
	a=0
	# Go through objects
	scn=Blender.Scene.GetCurrent()
	for obj in scn.objects: #cycle through the Objects
		if obj.getType()=="Mesh":
			data_name=obj.getData(True,False)
			omesh=Mesh.Get(data_name)
			nmesh=NMesh.GetRaw(data_name)
			verts = omesh.verts[:] #make backup of object geometry
			omesh.transform(obj.matrixWorld) 	
			
			#create area of materials used by current object
			omaterials=obj.getMaterials()
			mmaterials=nmesh.materials
			omatindex=0
			mmatindex=0
			materials=[]
			i=0
						
			while mmatindex<len(mmaterials) or omatindex<len(omaterials):
				if (obj.colbits & (1 << i)) != 0: # object material
					materials.append(omaterials[omatindex])
					omatindex+=1
					mmatindex+=1
				else: #mesh material		
					materials.append(mmaterials[mmatindex])
					mmatindex+=1
				i+=1
			
			i=0
			for ma in materials:
				if ma.name==mat:		
						a+=msh_area(omesh,i) 
				i+=1
			
			omesh.verts = verts #restore object
			
	if editmode: Window.EditMode(1)  # optional, just being nice
	s="Sum area of faces using this material: "+str(a)+"%t"
	s+="|The formula only works with meshes on current scene!"
	Draw.PupMenu(s)

##########################################
#default event handler
##########################################
def event(evt, val):
	if evt == Draw.ESCKEY or evt == Draw.QKEY: 
		Draw.Exit()             
		return

##########################################
#what buttons do
##########################################
def button_event(evt): 
	global Material1_index, Material2_index, Material_count, MENU_MAT1, MENU_MAT2, Action, Limit, Assign, Rename_to
	if evt==1: #source material combo
		if MENU_MAT1.val <= Material_count:
			Material1_index = MENU_MAT1.val
			Draw.Redraw(1)
	elif evt==2: #source material - left arrow (prev)
		if Material1_index > 1:
			Material1_index=Material1_index-1
			Draw.Redraw(1)  
	elif evt==3: #source material - right arrow (next)
		if Material1_index < Material_count: 
			Material1_index=Material1_index+1
			Draw.Redraw(1)
	elif evt==4: #rename radio
		Action=1
		Draw.Redraw(1)
	elif evt==5: #replace radio
		Action=2
		Draw.Redraw(1)			 
	elif evt==6: #assign radio
		Action=3
		Draw.Redraw(1)			 
	elif evt==8: #source material - show users
		list_users(Material_array[Material1_index-1])
	elif evt==9: #area
		area(Material_array[Material1_index-1])

	elif evt==11: #dest material combo		
		if MENU_MAT2.val <= Material_count:
			Material2_index = MENU_MAT2.val
			Draw.Redraw(1)
	elif evt==12: #dest material - left arrow (prev)
		if Material2_index > 1:
			Material2_index=Material2_index-1
			Draw.Redraw(1)  
	elif evt==13: #dest material - right arrow (next)
		if Material2_index < Material_count: 
			Material2_index=Material2_index+1
			Draw.Redraw(1)
	elif evt==14: #limit all
		Limit=1
		Draw.Redraw(1)			 
	elif evt==15: #limit visible
		Limit=2
		Draw.Redraw(1)			 
	elif evt==16: #limit selected
		Limit=3
		Draw.Redraw(1)			 
			 
	elif evt==18: #dest material - show users
		list_users(Material_array[Material2_index-1])
	elif evt==19: #area
		area(Material_array[Material2_index-1])
	elif evt==20:
		Rename_to=RENAME_BUTTON.val
		Draw.Redraw(1)
	elif evt==21: #replace button
		replace(Material_array[Material1_index-1],Material_array[Material2_index-1])		
		getMaterials()			
		Draw.Redraw(1)
	elif evt==22: #rename button 
		rename(Material_array[Material1_index-1],Rename_to)
		RENAME_BUTTON.val=""
		getMaterials()
		Draw.Redraw(1)
	elif evt==23: #assign button
		if Assign==1:
			AssignFaces(Material_array[Material1_index-1])
		else:
			AssignObjects(Material_array[Material1_index-1])
		getMaterials()
		Draw.Redraw(1)
	elif evt==31: #assign faces
		Assign=1
		Draw.Redraw(1)			 
	elif evt==32: #assign objects
		Assign=2
		Draw.Redraw(1)			 
	elif evt==40: #refresh button
		getMaterials()			
		Draw.Redraw(1) 

##########################################
def draw_rectangle(x,y,w,h,r,g,b,a):
	BGL.glEnable(BGL.GL_BLEND)
	BGL.glBlendFunc(BGL.GL_SRC_ALPHA, BGL.GL_ONE_MINUS_SRC_ALPHA)
	BGL.glColor4f(r,g,b,a)
	BGL.glBegin(BGL.GL_POLYGON)
	BGL.glVertex2i(x, y)
	BGL.glVertex2i(x, y + h)
	BGL.glVertex2i(x + w, y + h)
	BGL.glVertex2i(x + w, y)
	BGL.glEnd()	
	BGL.glDisable(BGL.GL_BLEND)

##########################################
def INTtoFLOAT(rgba):
	r = float(rgba[0] *10 /254) /10
	g = float(rgba[1] *10 /254) /10
	b = float(rgba[2] *10 /254) /10
	a = float(rgba[3] *10 /254) /10
	return [r,g,b,a]

class tmp_theme:
	back= [107, 107, 107, 255]
	panel=[175, 175, 175, 51]
	header=[107, 107, 107, 255]
	text=[0, 0, 0, 255]
	text_hi=[255, 255, 255, 255]	

##########################################
#Main screen
##########################################
def gui():
	global Material1_index, Material2_index, Material_count, Material1_combo, Material2_combo, MENU_MAT1, MENU_MAT2, Action, Assign, Limit, Rename_to, RENAME_BUTTON 

	c1_left=5
	c2_left=190
	c_width=170
	c_height=113
	c_bottom=30
	head_bottom=c_bottom+c_height
	head_height=16
	title_top=c_bottom+c_height+head_height+75
	combo_bottom=c_bottom+c_height-25
	combo_width=120
	index_bottom=combo_bottom-18
	radio_bottom=combo_bottom-85
	buttons_bottom=c_bottom+10
	action_bottom=7
	action_width=70
	button_height=16
	margin=5
	buttons_margin=c_width-action_width-margin
	
	theme = Window.Theme.Get()[0]
	buts = theme.get('buts')		
	r,g,b,a = INTtoFLOAT(buts.back)	
	BGL.glClearColor(r+0.05,g+0.05,b+0.05,a)
	BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
	r,g,b,a = INTtoFLOAT(buts.panel)	
	draw_rectangle(c1_left,c_bottom,c_width,c_height,r,g,b,a+0.1)		
	draw_rectangle(c2_left,c_bottom,c_width,c_height,r,g,b,a+0.1)		
	r,g,b,a = INTtoFLOAT(buts.header)	
	draw_rectangle(c1_left,head_bottom,c_width,head_height,r-0.1,g-0.1,b-0.1,a)		
	draw_rectangle(c2_left,head_bottom,c_width,head_height,r-0.1,g-0.1,b-0.1,a)		

	BGL.glRasterPos2i(c1_left+margin,title_top) 
	Draw.Text("Material Works 1.1 - basic functions", "small")
	BGL.glRasterPos2i(c1_left+margin,title_top-15) 
	Draw.Text("- Search objects, meshes, curves and metaballs with a material","small") 
	BGL.glRasterPos2i(c1_left+margin,title_top-25) 
	Draw.Text("    and replaces it by another material.","small")
	BGL.glRasterPos2i(c1_left+margin,title_top-35) 
	Draw.Text("     (Can be used for merging duplicate materials).","tiny")
	BGL.glRasterPos2i(c1_left+margin,title_top-45) 
	Draw.Text("- Rename materials.","small")
	BGL.glRasterPos2i(c1_left+margin,title_top-55) 
	Draw.Text("- Material surface area calculation.","small")
	BGL.glRasterPos2i(c1_left+margin,title_top-65) 
	Draw.Text("- Assign material to selected objects.","small")
	
	r,g,b,a = INTtoFLOAT(buts.text_hi)	
	BGL.glColor4f(r,g,b,a)

	if Action==1:
		BGL.glRasterPos2i(c1_left+margin,head_bottom+5) 
		Draw.Text("Replace material", "small")
		BGL.glRasterPos2i(c2_left+margin,head_bottom+5) 
		Draw.Text("by material", "small")
	elif Action==2:
		BGL.glRasterPos2i(c1_left+margin,head_bottom+5) 
		Draw.Text("Rename material", "small")
		BGL.glRasterPos2i(c2_left+margin,head_bottom+5) 
		Draw.Text("to", "small")
	elif Action==3:
		BGL.glRasterPos2i(c1_left+margin,head_bottom+5) 
		Draw.Text("Assign material", "small")
		BGL.glRasterPos2i(c2_left+margin,head_bottom+5) 
		Draw.Text("to", "small")

	r,g,b,a = INTtoFLOAT(buts.text)
	BGL.glColor4f(r,g,b,a)
	if Material_count > 0: # Write current item / total items.
		r,g,b,a = INTtoFLOAT(buts.header)	
		draw_rectangle(c1_left+margin,index_bottom,26,12,r,g,b,a)			
		BGL.glColor3f(0,0,0)
		BGL.glRasterPos2i(c1_left+margin,index_bottom+4)
		Draw.Text(str(Material1_index) + " / " + str(Material_count), "tiny")		
		MENU_MAT1 = Draw.Menu(Material1_combo, 1, c1_left+margin, combo_bottom, combo_width, button_height, Material1_index, "Select a material")	
		if Material1_index != 1 : Draw.PushButton("<", 2, c1_left+margin+combo_width+4, combo_bottom, button_height,button_height , "Prev MATERIAL")				
		if Material1_index != Material_count : Draw.PushButton(">", 3, c1_left+margin+combo_width+20, combo_bottom, button_height,button_height , "Next MATERIAL")
		
		r,g,b,a = INTtoFLOAT(buts.text_hi)	
		BGL.glColor4f(r,g,b,a)
		BGL.glRasterPos2i(c1_left+margin,radio_bottom+53)
		Draw.Text("Function","small")
		
		state=[0,0,0]
		state[Action-1]=1
		Draw.BeginAlign()
		Draw.Toggle("Replace", 4, c1_left+margin, radio_bottom+35,60,14,state[0], "Replace material by another")
		Draw.Toggle("Rename", 5, c1_left+margin, radio_bottom+21,60,14,state[1], "Rename material")
		Draw.Toggle("Assign", 6, c1_left+margin, radio_bottom+7, 60,14,state[2], "Assign material to selected faces or objects")
		Draw.EndAlign()

		Draw.PushButton("Show users", 8, c1_left+buttons_margin, buttons_bottom, action_width, button_height , "Show who is using this material")
		Draw.PushButton("Show area", 9, c1_left+buttons_margin, buttons_bottom+20, action_width, button_height , "Sum area of all faces using this material")

		if Action==1:
			r,g,b,a = INTtoFLOAT(buts.header)	
			draw_rectangle(c2_left+margin,index_bottom,26,12,r,g,b,a)			
			BGL.glColor3f(0,0,0)
			BGL.glRasterPos2i(c2_left+margin,index_bottom+4)
			Draw.Text(str(Material2_index) + " / " + str(Material_count), "tiny")		
			MENU_MAT2 = Draw.Menu(Material2_combo, 11, c2_left+margin, combo_bottom, combo_width, button_height, Material2_index, "Select a material")	
			if Material2_index != 1 : Draw.PushButton("<", 12, c2_left+margin+combo_width+4, combo_bottom, button_height,button_height , "Prev MATERIAL")				
			if Material2_index != Material_count : Draw.PushButton(">", 13, c2_left+margin+combo_width+20, combo_bottom, button_height,button_height , "Next MATERIAL")
			
			r,g,b,a = INTtoFLOAT(buts.text_hi)	
			BGL.glColor4f(r,g,b,a)
			BGL.glRasterPos2i(c2_left+margin,radio_bottom+53)
			Draw.Text("Limit to","small")

			state=[0,0,0]
			state[Limit-1]=1
			Draw.BeginAlign()
			Draw.Toggle("All", 14, c2_left+margin, radio_bottom+35,60,14,state[0], "No limit")
			Draw.Toggle("Visible", 15, c2_left+margin, radio_bottom+21,60,14,state[1], "Visible Layers")
			Draw.Toggle("Selected", 16, c2_left+margin, radio_bottom+7, 60,14,state[2], "Selected Objects")
			Draw.EndAlign()		

			if Limit==1:
				Draw.PushButton("Show users", 18, c2_left+buttons_margin, buttons_bottom, action_width, button_height , "Show who is using this material")
				Draw.PushButton("Show area", 19, c2_left+buttons_margin, buttons_bottom+20, action_width, button_height , "Sum area of all faces using this material")
			
		elif Action==2:
			RENAME_BUTTON=Draw.String("MA:",20,c2_left+margin, combo_bottom, combo_width, button_height,Rename_to,19, "Rename material")
		elif Action==3:
			r,g,b,a = INTtoFLOAT(buts.text_hi)	
			BGL.glColor4f(r,g,b,a)
			BGL.glRasterPos2i(c2_left+margin,combo_bottom+2)
			Draw.Text("Assign to","small")

			state=[0,0,0]
			state[Assign-1]=1
			Draw.BeginAlign()
			Draw.Toggle("Selected Faces", 31, c2_left+margin, combo_bottom-16,120,14,state[0], "Current object - selected faces")
			Draw.Toggle("Selected Objects", 32, c2_left+margin, combo_bottom-30,120,14,state[1], "Selected objects - all faces")
			Draw.EndAlign()				

		if Action==1: Draw.PushButton("Replace", 21, c2_left+c_width-action_width, action_bottom, action_width, button_height , "Replace materials in all objects")
		elif Action==2: Draw.PushButton("Rename", 22, c2_left+c_width-action_width, action_bottom, action_width, button_height , "Rename the material")
		elif Action==3:	Draw.PushButton("Assign", 23, c2_left+c_width-action_width, action_bottom, action_width, button_height , "Assign the material")

		Draw.PushButton("Refresh", 40, c1_left, action_bottom, action_width, button_height , "Reload materials")					

##########################################
#Start here
##########################################
AuthorName = "Vaclav Chaloupka"
AuthorEmail = "bruxy1@gmail.com"
AuthorWebPage = "http:\\blender.chaloupkovi.cz"
ShowWarnings = 1

Rename_to=""
Material1_combo= ""
Material2_combo= ""
Material_count = 0
Material_array=[]
Material1_index=1
Material2_index=1
getMaterials()
Action=1
Limit=1
Assign=1

Draw.Register(gui, event, button_event)
