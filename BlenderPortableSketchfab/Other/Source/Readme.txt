Blender Portable Launcher
========================
Copyright 2004-2007 John T. Haller

Website: http://PortableApps.com/BlenderPortable

This software is OSI Certified Open Source Software.
OSI Certified is a certification mark of the Open Source Initiative.

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


ABOUT Blender PORTABLE
===================
The Blender Portable Launcher allows you to run Blender from a removable drive whose
letter changes as you move it to another computer.  The program can be entirely
self-contained on the drive and then used on any Windows computer.


LICENSE
=======
This code is released under the GPL.  The full code is included with this
package as BlenderPortable.nsi.


INSTALLATION / DIRECTORY STRUCTURE
==================================
By default, the program expects this directory structure:

-\ <--- Directory with BlenderPortable.exe
	+\App\
		+\Blender\
		+\Python26\
	+\Data\
		+\settings\


It can be used in other directory configurations by including the BlenderPortable.ini file in the
same directory as BlenderPortable.exe and configuring it as details in the INI file section below.


BlenderPortable.INI CONFIGURATION
==============================
The Blender Portable Launcher will look for an ini file called BlenderPortable.ini within its
directory.  If you are happy with the default options, it is not necessary, though.  The INI
file is formatted as follows:

[BlenderPortable]
AdditionalParameters=
WaitForBlender=false
DisableSplashScreen=false

The AdditionalParameters entry allows you to pass additional commandline parameter entries
to Blender.exe.  Whatever you enter here will be appended to the call to Blender.exe.

The WaitForBlender entry allows you to set the Blender Portable Launcher to wait for Blender to
close before it closes.  This option is mainly of use when BlenderPortable.exe is called by
another program that awaits it's conclusion to perform a task.

The DisableSplashScreen entry allows you to disable the splash screen by setting it to
true (lowercase).


PROGRAM HISTORY / ABOUT THE AUTHORS
===================================
This launcher contains elements from multiple sources.  It is loosely based on the
Firefox Portable launcher and contains some ideas from mai9 and tracon on the mozillaZine
forums.