#!BPY
"""
Name: 'Getting Started'
Blender: 234
Group: 'Help'
Tooltip: 'Help for new users'
"""

__author__ = "Matt Ebb"
__url__ = ("blender", "blenderartists.org")
__version__ = "1.0"
__bpydoc__ = """\
This script opens the user's default web browser at www.blender3d.org's
"Getting Started" page.
"""

# $Id: help_getting_started.py 14530 2008-04-23 14:04:05Z campbellbarton $
#
# --------------------------------------------------------------------------
# Getting Started Help Menu Item
# --------------------------------------------------------------------------
# ***** BEGIN GPL LICENSE BLOCK *****
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

import Blender, webbrowser
version = str(Blender.Get('version'))
webbrowser.open('http://www.blender3d.org/Help/?pg=GettingStarted&ver=' + version)
