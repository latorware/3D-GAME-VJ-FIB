'''
Created on 22/02/2010

@author: Lupas
'''

import  wx
import  wx.grid as  gridlib

class rortable(gridlib.PyGridTableBase):

	def __init__(self, parent):
		gridlib.PyGridTableBase.__init__(self)
		self.parent = parent
		self.lines = []
		self.maxColumns = 5

	def GetAttr(self, row, col, kind):
		""" set up coloring cells based on their section definition
		"""
#		print " row %d col %d kind %s" % (row, col, str(kind))
		ncol = col
		default = super(rortable, self).GetAttr(row, ncol, kind)		
		coldef = self.parent.parser.getColOfSection(self.lines[row].section, ncol)
		if coldef is None: return default

		if default is None: default = gridlib.GridCellAttr()#wx.RED, wx.WHITE, self.parent.GetDefaultCellFont(), wx.ALIGN_LEFT, wx.ALIGN_CENTER_VERTICAL)
		default.IncRef()
		default.SetOverflow(True)
		if self.lines[row].isHeader:
			default.SetBackgroundColour(wx.CYAN)
			default.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
		else:
			default.SetBackgroundColour(wx.Color(220, 220, 220))
			coltype = coldef['type']
			colname = coldef['name']
			if coltype == "string" : 
				default.SetSize(1, 2)
				default.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
				if colname.find('material') <> -1: 
					default.SetTextColour(wx.NamedColor('#23ab26'))
				elif colname.find("mesh") <> -1: default.SetTextColour(wx.Colour(244, 90, 231))
				else: default.SetTextColour(wx.BLACK)
			elif coltype == "node": 
				default.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
				default.SetTextColour(wx.BLUE)
			elif coltype == "float": 
				default.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
				default.SetTextColour(wx.BLACK)
			elif coltype == "int": 
				default.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
				default.SetTextColour(wx.RED)
			else: 
				default.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
				default.SetTextColour(wx.BLACK)
		return default
		
	def GetNumberRows(self):
		return len(self.lines)

	def GetNumberCols(self):
		return self.maxColumns

	def IsEmptyCell(self, row, col):
		if row >= len(self.lines) or col > self.lines[row].getMaxCols() : return True
		else : return False

	def GetValue(self, row, col):
#		offset = self.colSpan(row, col)
		if self.lines[row].isHeader and col == 0: return self.lines[row].section
		elif self.lines[row].getColValue(col) is not None: return str(self.lines[row].getColValue(col))
		return super(rortable, self).GetValue(row, col)

	def SetValue(self, row, col, value):
#		offset = self.colSpan(row, col)
		
		if row >= len(self.lines) or col > self.lines[row].getMaxCols() : raise Exception("row is greater than maximum rows")
		if self.lines[row].isHeader and col == 0: return 
		else:
			#Value is unicode string
			theValue = None
			coltype = self.parent.parser.getColOfSection(self.lines[row].section, col)['type']
			if coltype == 'int' or coltype == 'node': theValue = int(value)
			elif coltype == 'float': theValue = float(value)
			elif coltype == 'string': theValue = str(value)
			else: theValue = value 
			setattr(self.lines[row], self.lines[row].getColName(col), theValue)

	def GetColLabelValue(self, col):
#		offset = self.colSpan(self.parent.GetGridCursorRow(), col)
		if col >= self.lines[self.parent.Row].getMaxCols(): return ""
		else: return self.lines[self.parent.Row].getColName(col).replace("_", " ")
	
	def GetRowLabelValue(self, row):
		""" actual section
		"""
		return self.lines[row].section
	
	def InsertRows(self, pos=0, numRows=1):	
		for i in range(0, numRows):
			self.parent.parser.insertLine(self.parent.GetGridCursorRow())
		msg = gridlib.GridTableMessage(self, 			# The table
				gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
				numRows									   # how many
				)

		self.GetView().ProcessTableMessage(msg)
		
		return True
#	 Called to determine the kind of editor/renderer to use by
#	 default, doesn't necessarily have to be the same type used
#	 natively by the editor/renderer if they know how to convert.

	def GetTypeName(self, row, col):
		coldef = self.parent.parser.getColOfSection(self.lines[row].section, col)
		if coldef is not None:
			if coldef['name'].find('material') != -1 : return 'material'
			elif coldef['name'].find('mesh') != -1 : return 'mesh'
			elif coldef['name'].find('sound') != -1 : return 'sound'
			elif coldef['name'] == 'effect' : return 'material_managed_effect'
			else: return coldef['type']
		else: return gridlib.GRID_VALUE_STRING

	# Called to determine how the data can be fetched and stored by the
	# editor and renderer.  This allows you to enforce some type-safety
	# in the grid.
#	def CanGetValueAs(self, row, col, typeName):
#		coldef = self.parent.parser.getColOfSection(self.lines[row].section, col)['name']
#		return coldef.find('material') != -1 
#
#	def CanSetValueAs(self, row, col, typeName):
#		return self.CanGetValueAs(row, col, typeName)	
	
#-----------------------end override methods----------------------------------------------------
	def colSpan(self, row, col):
		""" string columns are span 2 columns, so return the real grid column
		"""
		cont = 0 
		realCol = 0
		while cont <= col:
			coldef = self.parent.parser.getColOfSection(self.lines[row].section, cont)
			if coldef is not None:
				if coldef['type'] == 'string':
					realCol += 1
			cont += 1
		return realCol
	
	def sameSection(self, Row1, Row2):
		return self.lines[Row1].section == self.lines[Row2].section
	
	def FromLinesOfSection(self, LinesOfSection):
		self.lines = LinesOfSection
