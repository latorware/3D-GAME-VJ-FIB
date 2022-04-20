
import string, os, os.path, glob
#import  wx.lib.multisash    as  sash
import  wx
import  wx.grid as gridlib
import  wx.html as  html
import  wx.lib.wxpTag
from truckparser import *
from RoRGridTable import *
from RoRVirtualKeys import *
from types import *

#---------------------------------------------------------------------------
class MyCellEditor(gridlib.PyGridCellEditor):
	"""
	This is a sample GridCellEditor that shows you how to make your own custom
	grid editors.  All the methods that can be overridden are shown here.  The
	ones that must be overridden are marked with "*Must Override*" in the
	docstring.
	"""
	def __init__(self):
		print "MyCellEditor ctor\n"
		gridlib.PyGridCellEditor.__init__(self)


	def Create(self, parent, id, evtHandler):
		"""
		Called to create the control, which must derive from wx.Control.
		*Must Override*
		"""
		print "MyCellEditor: Create\n"
		self._tc = wx.TextCtrl(parent, id, "")
		self._tc.SetInsertionPoint(0)
		self.SetControl(self._tc)

		if evtHandler:
			self._tc.PushEventHandler(evtHandler)


	def SetSize(self, rect):
		"""
		Called to position/size the edit control within the cell rectangle.
		If you don't fill the cell (the rect) then be sure to override
		PaintBackground and do something meaningful there.
		"""
		print "MyCellEditor: SetSize %s\n" % rect
		self._tc.SetDimensions(rect.x, rect.y, rect.width + 2, rect.height + 2,
							   wx.SIZE_ALLOW_MINUS_ONE)


	def Show(self, show, attr):
		"""
		Show or hide the edit control.  You can use the attr (if not None)
		to set colours or fonts for the control.
		"""
		print "MyCellEditor: Show(self, %s, %s)\n" % (show, attr)
		super(MyCellEditor, self).Show(show, attr)


	def PaintBackground(self, rect, attr):
		"""
		Draws the part of the cell not occupied by the edit control.  The
		base  class version just fills it with background colour from the
		attribute.  In this class the edit control fills the whole cell so
		don't do anything at all in order to reduce flicker.
		"""
		print "MyCellEditor: PaintBackground\n"


	def BeginEdit(self, row, col, grid):
		"""
		Fetch the value from the table and prepare the edit control
		to begin editing.  Set the focus to the edit control.
		*Must Override*
		"""
		print "MyCellEditor: BeginEdit (%d,%d)\n" % (row, col)
		self.startValue = grid.GetTable().GetValue(row, col)
		self._tc.SetValue(self.startValue)
		self._tc.SetInsertionPointEnd()
		self._tc.SetFocus()

		# For this example, select the text
		self._tc.SetSelection(0, self._tc.GetLastPosition())


	def EndEdit(self, row, col, grid):
		"""
		Complete the editing of the current cell. Returns True if the value
		has changed.  If necessary, the control may be destroyed.
		*Must Override*
		"""
		print "MyCellEditor: EndEdit (%d,%d)\n" % (row, col)
		changed = False

		val = self._tc.GetValue()
		
		if val != self.startValue:
			changed = True
			grid.GetTable().SetValue(row, col, val) # update the table

		self.startValue = ''
		self._tc.SetValue('')
		return changed


	def Reset(self):
		"""
		Reset the value in the control back to its starting value.
		*Must Override*
		"""
		print "MyCellEditor: Reset\n"
		self._tc.SetValue(self.startValue)
		self._tc.SetInsertionPointEnd()


	def IsAcceptedKey(self, evt):
		"""
		Return True to allow the given key to start editing: the base class
		version only checks that the event has no modifiers.  F2 is special
		and will always start the editor.
		"""
		print "MyCellEditor: IsAcceptedKey: %d\n" % (evt.GetKeyCode())

		## We can ask the base class to do it
		#return super(MyCellEditor, self).IsAcceptedKey(evt)

		# or do it ourselves
		return (not (evt.ControlDown() or evt.AltDown()) and
				evt.GetKeyCode() != wx.WXK_SHIFT)


	def StartingKey(self, evt):
		"""
		If the editor is enabled by pressing keys on the grid, this will be
		called to let the editor do something about that first key if desired.
		"""
		print "MyCellEditor: StartingKey %d\n" % evt.GetKeyCode()
		key = evt.GetKeyCode()
		ch = None
		if key in [ wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3,
					wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7,
					wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
					]:

			ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)

		elif key < 256 and key >= 0 and chr(key) in string.printable:
			ch = chr(key)

		if ch is not None:
			# For this example, replace the text.  Normally we would append it.
			#self._tc.AppendText(ch)
			self._tc.SetValue(ch)
			self._tc.SetInsertionPointEnd()
		else:
			evt.Skip()


	def StartingClick(self):
		"""
		If the editor is enabled by clicking on the cell, this method will be
		called to allow the editor to simulate the click on the control if
		needed.
		"""
		print "MyCellEditor: StartingClick\n"


	def Destroy(self):
		"""final cleanup"""
		print "MyCellEditor: Destroy\n"
		super(MyCellEditor, self).Destroy()


	def Clone(self):
		"""
		Create a new object which is the copy of this one
		*Must Override*
		"""
		print "MyCellEditor: Clone\n"
		return MyCellEditor(self.log)


#---------------------------------------------------------------------------
class GridEditorTest(gridlib.Grid):
	def __init__(self, parent, **args):
		gridlib.Grid.__init__(self, parent, -1, **args)

		self.parent = parent
		self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.LeftClickCell)
		self.Bind(gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.RightClickCell)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.onMouseEvent)
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyEvent)
		self.Bind(gridlib.EVT_GRID_RANGE_SELECT, self.OnSelectRange)
		self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
#		self.Bind(gridlib.EVT_GRID_CELL_CHANGE, self.OnCellChanged)
		
		self.SetDefaultCellOverflow(True)
		self.SetDefaultCellBackgroundColour(wx.Color(220, 220, 220))
		self.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
		self.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
		self.selCells = []
		self._Row = 0
		self._fontsize = 0
		self.menuItems = {}		

		table = rortable(self)
		self.parser = rorparser()
		content = getContent(os.path.join(self.currentPath(), 'openFile.txt'))
		self.truckPath = os.path.abspath(os.path.dirname(content[0]))
		self.parser.parse(content[0])
		table.FromLinesOfSection(self.parser.lines)
		table.maxColumns = self.parser.maxColumns() + 1
		self.SetTable(table)
		
		self.retrieveFiles(self.truckPath)
#		for i in range(0, table.maxColumns - 1):
#			self.SetColSize(i, 50)

		self.ForceRefresh()
		l = self.parser.lines
		content = []

		self.RegisterDataType('string',
							  gridlib.GridCellStringRenderer(),
							  gridlib.GridCellTextEditor())
		
		self.RegisterDataType('material_managed_effect',
							  gridlib.GridCellStringRenderer(),
							  gridlib.GridCellChoiceEditor(managedMaterialEffect, False))
		
		self.RegisterDataType('material',
							  gridlib.GridCellStringRenderer(),
							  gridlib.GridCellChoiceEditor(self.materials, True))
		self.RegisterDataType('mesh',
							gridlib.GridCellStringRenderer(),
							gridlib.GridCellChoiceEditor(self.meshes, True))
		self.RegisterDataType('sound',
							gridlib.GridCellStringRenderer(),
							gridlib.GridCellChoiceEditor(self.sounds, True))
		self.RegisterDataType('shortcut',
							gridlib.GridCellStringRenderer(),
							gridlib.GridCellChoiceEditor(self.shortcuts, False))


		self.RegisterDataType('int',
							gridlib.GridCellNumberRenderer(),
							gridlib.GridCellNumberEditor())
		self.RegisterDataType('node',
							gridlib.GridCellNumberRenderer(),
							gridlib.GridCellNumberEditor())
		self.RegisterDataType('float',
							gridlib.GridCellFloatRenderer(precision=2),
							gridlib.GridCellFloatEditor(precision=3))
	def createMenu(self):
		""" popup menu with commands and sections to add"""
		def doMenu(themenu, listOfCaptions, popuphandler=None):
			listOfCaptions.sort()
			for it in listOfCaptions:
				id = wx.NewId()
				self.menuItems[str(id)] = it
				item = themenu.Append(id, it)
				if popuphandler is None: self.Bind(wx.EVT_MENU, self.popupHandler, item)
				else: self.Bind(wx.EVT_MENU, popuphandler, item) 
		self.menu = wx.Menu()
		commands = wx.Menu()
		doMenu(commands, self.parser.commands.keys())
		self.menu.AppendSubMenu(commands, 'commands')
		k = self.parser.sections.keys()
		sections = wx.Menu()
		doMenu(sections, [x for x in k if x not in self.parser.truckSections])
		self.menu.AppendSubMenu(sections, 'sections')
		
		doMenu(self.menu, ['group beams'], self.groupHightlightBeams)
		
		#local variable
		#menuItems = ['set_beam_defaults', ';']
		
	def groupHightlightBeams(self, evt):
		""" beams highligthed in 3D window are moved into a continous block
		"""
		minIdx, howmany = self.groupBeams()
		if minIdx > 0:
			section = self.insertSection(';', minIdx)
			section.comment_line = 'grp:groupName'
			footer = self.insertSection(';', minIdx+2 + howmany)
			footer.comment_line = 'groupName'
			
			self.Refresh()
			self.Update()
		evt.Skip()
		
	def insertSection(self, sectionOrObj, atRow):
		""" insert a new section notifying Grid
		return the lineOfSection created
		"""
		gr = self.parser.insertLine(atRow, sectionOrObj)
		msg = gridlib.GridTableMessage(self.GetTable(), 			# The table
				gridlib.GRIDTABLE_NOTIFY_ROWS_APPENDED, # what we did to it
				1									   # how many
				)
		self.ProcessTableMessage(msg)	
		return gr
		
	def groupBeams(self):
		""" move all selected beams into a contigous block

		return a tuple
		- the minimun row index used
		- how many beams are in the group
		"""
		minidx = -1
		cont = 0
		sel = self.selCells # a list of tuples: [ (row1, col1), (row2, col2) ... ]
		if len(sel) > 0:
			idxlist = []
			for c in sel:
				idxRow = c[0]
				if self.parser.lines[idxRow].section == 'beams':
					if not idxRow in idxlist:
						idxlist.append(idxRow) 
			if len(idxlist) < 2: 
				print "emtpy list to hightlight"
				return (minidx, cont)
			minidx = min(idxlist)
			idxlist.pop(idxlist.index(minidx))
			for i in idxlist:
				item = self.parser.lines.pop(i)
				self.parser.lines.insert(minidx + cont + 1, item)
				print "Unit testing: item was at ", i, " now it is at ", self.parser.lines.index(item), " that should be ", minidx + cont
				cont += 1
		print "min row is ", minidx, " count is ", cont
		return (minidx, cont)
		
	def popupHandler(self, evt):
		id = evt.GetId()
		section = self.menuItems[str(id)]
		self.insertSection(section, self._Row)
		if self.parser.sections.has_key(section):
			header = self.insertSection(section, self._Row)
			header.isHeader = True
		idx = list_has_key(self.parser.sectionfooter, section)
		if idx > -1:
			self.insertSection(section, self._Row + 1)
	
		evt.Skip()
	def getShortcuts(self):
		""" shortcuts used on commands, commands2, etc.
		we return a list used as a combobox to choose the text to show
		instead the number of the key
		"""
		result = []
		for i in range(0, 48):
			text = 'F' + str((i % 12) + 1)
			if i >= 36:   text = 'CTRL + ALT + ' + text
			elif i >= 24: text = 'ALT + ' + text
			elif i >= 12: text = 'CTRL + ' + text
			result.append(text)
		return result
		
		
	def retrieveFiles(self, path):
		self.meshes = []
		self.materials = []
		self.sounds = []
		self.shortcuts = self.getShortcuts()
		files = glob.glob(os.path.join(path, '*.*'))
		for file in files:
			if file.endswith('.mesh'):
				self.meshes.append(file)
			elif file.endswith('.material'):
				content = getContent(file)
				for line in content:
					if line.startswith('material '):
						self.materials.append(line.split(' ')[1].replace('\n', ''))
			elif file.endswith('.wav'):
				self.sounds.append(file)

	def currentPath(self):
		print os.path.dirname(os.path.abspath(__file__))
		return os.path.dirname(os.path.abspath(__file__))
		evt.Skip()

	def OnSelectRange(self, event):
		"""Internal update to the selection tracking list"""
		if event.Selecting():
			# adding to the list...
			for row in range(event.GetTopRow(), event.GetBottomRow() + 1):
				for col in range(event.GetLeftCol(), event.GetRightCol() + 1): 
					ele = (row, col)
					if  ele not in self.selCells:
						self.selCells.append(ele)
		else:
			# removal from list
		   for row in range(event.GetTopRow(), event.GetBottomRow() + 1):
				for col in range(event.GetLeftCol(), event.GetRightCol() + 1): 
					ele = (row, col)
					if  ele in self.selCells:
						self.selCells.remove(ele)
#		   self.ConfigureForSelection()
		self.getSelection()
		event.Skip()
	def OnSelectCell(self, event):
		"""Internal update to the selection tracking list"""
		self.selCells = [ (event.GetRow(), event.GetCol())]
		self.Row = event.GetRow()
		old = super(GridEditorTest, self).GetGridCursorCol()
		self.getSelection()
		#attr = self.GetTable().GetAttr(self.GetGridCursorRow(), old, 0)
		#if attr is not None:
		#	pass #print "get size " , attr.GetSize()
		#else: print "attr is none for %d %d" % (self.GetGridCursorRow(), old)
		
		event.Skip()
	def selSameCol(self):
		if len(selCells) == 0 : return False
		for ele in range(0, len(self.selCells) - 1):
			if self.selCells[ele][1] <> self.selCells[ele + 1][1]: return False
		return True
	
	def selSameRow(self):
		if len(selCells) == 0 : return False
		for ele in range(0, len(self.selCells) - 1):
			if self.selCells[ele][0] <> self.selCells[ele + 1][0]: return False
		return True
	def getSelection(self):
		print "cur selection ------------", type(self.selCells)
		for c in self.selCells:
			print c
		print "end selection ------------"			
#	def OnCellChanged(self, evt):
#		# update helpWindow
#		self.Row = evt.GetRow()
#		self.Col = evt.GetCol()
#
#		sec = self.parser.lines[self.Row].section
#		self.parent.helpWindow.section = sec
#
#
#
#		evt.Skip()
#		return
#		# extract help for validvalues, validmultiplevalues and so on
#		if coldef is not None:
#			self.parent.helpWindow.column = coldef['name']
#			thehelp = ""
#			optionList = None
#			if coldef.has_key("help"): thehelp = coldef['help'] 
#			if coldef.has_key("validmultiplevalues"): 
#				optionList = coldef['validmultiplevalues']
#			elif coldef.has_key('validvalues'):
#				optionList = coldef['validvalues']
#			
#			if optionList is not None:
#				if isinstance(optionList, ListType):
#					for element in optionList:
#						if isinstance(element, DictType):
#							thehelp += element['option']
#							if element.has_key('help'):
#								thehelp += ' - ' + element['help']
#							thehelp += '\n'
#						elif isinstance(element, StringType):
#							thehelp += element + ' ' 
#			self.parent.helpWindow.text = thehelp
#				
#		else:
#			self.parent.helpWindow.column = ""
#			self.parent.helpWindow.text = ""
#		evt.Skip()
	def OnKeyEvent(self, evt):
		Skip = True
		if evt.m_keyCode == wx.WXK_RETURN or evt.m_keyCode == wx.WXK_NUMPAD_ENTER:
			if evt.ControlDown():   # the edit control needs this key
				evt.Skip()
				return
			# ENTER key go ahead, SHIFT + ENTER go backawards
			self.DisableCellEditControl()
#			c = self.GetGridCursorCol()
			r = self.GetGridCursorRow()
			if evt.ShiftDown(): sum = -1
			else: sum = 1
			c = self.GetGridCursorCol() + sum
			if c == -1 : 
				r += sum
				c = self.parser.lines[r].getMaxCols() - 1
			elif c == self.parser.lines[r].getMaxCols():
				r += sum
				c = 0
			while self.GetTable().lines[r].isHeader:
				if r == len(self.GetTable().lines) - 1 or r == 0: break
				else:r += sum
			self.SetGridCursor(r, c)
			self.MakeCellVisible(r, c)
			if self.CanEnableCellControl():
				self.EnableCellEditControl()
			return
		
		elif evt.m_keyCode == wx.WXK_F12 :
			# print selected cells (row, column)  at screen
			for a in self.selCells:
				print str(a)
		elif evt.m_keyCode == wx.WXK_INSERT and evt.ControlDown():
			# insert a new line (same section) at current position
			self.InsertRows(self.GetGridCursorRow(), 1)
		elif evt.m_keyCode == wx.WXK_DELETE and evt.ControlDown():
			# delete a line
			self.DeleteRows(self.GetGridCursorRow(), 1)
		
		elif evt.m_keyCode == wx.WXK_UP and evt.ControlDown():
			# move current row up
			if self._Row > 0:
				Skip = False
				i = self._Row
				old = self.parser.lines[self._Row - 1]
				self.parser.lines[self._Row - 1] = self.parser.lines[self._Row]
				self.parser.lines[self._Row] = old
				self.Refresh()
				self.Update()
				self.Row = i - 1
				self.SetGridCursor(self.GetGridCursorRow()-1, self.GetGridCursorCol())				
		elif evt.m_keyCode == wx.WXK_DOWN and evt.ControlDown():				
			# move current row down
			if self._Row < len(self.parser.lines) - 1:
				Skip = False
				i = self._Row
				old = self.parser.lines[self._Row + 1]
				self.parser.lines[self._Row + 1] = self.parser.lines[self._Row]
				self.parser.lines[self._Row] = old
				self.Row = i + 1
				self.SetGridCursor(self.GetGridCursorRow()+1, self.GetGridCursorCol())
				self.Refresh()
				self.Update()
		elif evt.m_keyCode == WXK_D and evt.ControlDown():
			#Duplicate currentLine
			Skip = False
			new = self.parser.insertLine(self._Row, self.parser.lines[self._Row])
			if hasattr(new, 'entry'):
				new.entry = None # new object doesn't share 3D object
			self.SetGridCursor(self.GetGridCursorRow()+1, self.GetGridCursorCol())
			self.Refresh()
			self.Update()
			
		elif evt.m_keyCode == WXK_S and evt.ControlDown():
			# saving truck without overwrite original file !!
			self.SaveEditControlValue()
			content = []
			sec = "title"
			l = self.parser.lines
			for i in range(len(l)):
				content.append(l[i].getTruckLine() + '\n')
			saveContent(content, os.path.join(self.currentPath(), 'new_generated.truck'))
		if Skip: evt.Skip()
			
	def onMouseEvent(self, evt):
		# change Grid Font size 
		if evt.ControlDown() and evt.GetWheelRotation() != 0:
			self.Parent.fontsize = (evt.GetWheelRotation() / abs(evt.GetWheelRotation()))
			self.MakeCellVisible(self.Row, self.GetGridCursorCol())
		else:
			evt.Skip()

	def RightClickCell(self, evt):
		# show a popup to group beams and insert some section or commands
		self.createMenu()
		self.PopupMenu(self.menu)
		self.menu.Destroy()
		evt.Skip()

	def LeftClickCell(self, evt):
		evt.Skip()
	
	def _getRow(self):
		return self._Row
			
	def _setRow(self, value):
		if self.GetTable().sameSection(self._Row, value) : 
			self._Row = value
			return
		self._Row = value
		sec = self.parser.lines[self.Row].section
		
		if sec is not None: self.parent.helpWindow.section = sec
		w = 100
# changing column width when you click on a cell is sick !!

		for i in range(0, self.parser.lines[self._Row].getMaxCols() - 1):
			coldef = self.parser.getColOfSection(sec, i)
			if coldef is not None:
				if coldef['type'] == 'int' or coldef['type'] == 'node': w = 75
				elif coldef['type'] == 'float' : w = 80
				elif coldef['type'] == 'string': w = 200
			self.SetColSize(i, w + (self._fontsize))
		self.ForceRefresh()	

	def _delRow(self):
		del self._Row
			
	def _getfontsize(self):
		return self._fontsize
			
	def _setfontsize(self, value):
		font = self.GetDefaultCellFont()
		self._fontsize = font.GetPointSize() + value 
		font.SetPointSize(self._fontsize)  
		self.SetDefaultCellFont(font)
		self.SetDefaultRowSize(self._fontsize * 2 , True)
		font.SetWeight(wx.FONTWEIGHT_BOLD)
		self.SetLabelFont(font)
		self.SetRowLabelSize(self._fontsize * 10)
		self.ForceRefresh()
			
	fontsize = property(_getfontsize, _setfontsize)
	""" increasement of point size  
	"""	
	Row = property(_getRow, _setRow, _delRow)
#---------------------------------------------------------------------------

class TestFrame(wx.Frame):
	def __init__(self, parent, **args):
		wx.Frame.__init__(self, parent, -1, "RoRNotepad", **args)
#		self.grid = sash.MultiSash(self, -1, pos=(0, 0), size=(640, 480))
#		self.grid.SetDefaultChildClass(GridEditorTest)
		self._fontsize = 0
		self.grid = GridEditorTest(self, **args)
		self.grid.SetScrollLineY(40)
		
		self.helpWindow = helpFrame(self, size=((300, 400)))
		self.helpWindow.Show(True)
		


	def _getfontsize(self):
		return self._fontsize
			
	def _setfontsize(self, value):
		self._fontsize = value
		self.grid.fontsize = value
		self.helpWindow.fontsize = value
	
	fontsize = property(_getfontsize, _setfontsize)
	""" increase or decrement font size of help window
	"""
		
class helpFrame(wx.Frame):
	def __init__(self, parent, **args):
		wx.Frame.__init__(self, parent, -1, "help", **args)
		self.myhtml = html.HtmlWindow(self, -1)#, style=wx.NO_FULL_REPAINT_ON_RESIZE)
		self.loaded = False
		self.file = ""
		path = os.path.join(os.path.dirname(__file__), 'tdf.htm')
		if os.path.isfile(path):
			self.myhtml.LoadPage(path)
			self.file = path
			self.loaded = True
		else:
			path = os.path.join(os.path.dirname(__file__), 'default.htm')
			self.myhtml.LoadPage(path)
			
			
#		self.html.SetRelatedFrame(frame, self.titleBase + " -- %s")
		return

		grid = wx.GridBagSizer(2, 2)
		grid.SetFlexibleDirection(wx.BOTH)
		r = 0
		c = 0
		self.txt = wx.TextCtrl(self, -1, " <help text>", style=wx.TE_MULTILINE | wx.TE_READONLY)
		grid.Add(self.txt, pos=wx.GBPosition(r, c), span=wx.GBSpan(2, 1), flag=wx.EXPAND)
		grid.AddGrowableRow(0)
		grid.AddGrowableCol(0)
		
#		self.SetSizerAndFit(grid)
		self.Layout()
		self.AutoLayout = True
	
	def _getsection(self):
		return self.lblSection.GetLabel()
			
	def _setsection(self, value):
		if self.loaded:
			if self.myhtml.HasAnchor(value.title()): self.myhtml.ScrollToAnchor(value.title())
			#only a few of anchor are in lowercase
			elif self.myhtml.HasAnchor(value): self.myhtml.ScrollToAnchor(value)
			elif len(value) > 2: 
				if self.myhtml.HasAnchor(value.capitalize()): self.myhtml.ScrollToAnchor(value.capitalize())
#			else: print "web help for not found, searched ' % s' and ' % s'" % (value, value.title())
#			page = self.file + '#' + value.title()
#			self.myhtml.LoadPage(page)

	def _getcolumn(self):
		return self.lblColumn.GetLabel()
			
	def _setcolumn(self, value):
#		self.lblColumn.SetLabel("Column: " + value)
		pass
		
			
	def _gettext(self):
		return self.txt.GetValue()
			
	def _settext(self, value):
		self.txt.SetValue(value)

	def _getfontsize(self):
		return self._fontsize
			
	def _setfontsize(self, value):
#		for x in [self.txt ]:#,self.lblSection, self.lblColumn, ]:
#			font = x.GetFont()
#			font.SetPointSize(font.GetPointSize() + value)
#			x.SetFont(font)
#		self.Refresh()
		pass

	fontsize = property(_getfontsize, _setfontsize)
	""" increase or decrement font size of help window
	"""

		
	text = property(_gettext, _settext)
	""" set help text
	"""
	section = property(_getsection, _setsection)
	"""set up label of section 
	"""
	column = property(_getcolumn, _setcolumn)
	""" set column label
	"""

if __name__ == '__main__':
	import sys
	app = wx.PySimpleApp()
	frame = TestFrame(None, size=((800, 600)))
	frame.Show(True)
	app.MainLoop()
