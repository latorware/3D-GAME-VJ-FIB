;Copyright (C) 2004-2009 John T. Haller
;Copyright (C) 2006-2009 Geoff Shearsmith

;Website: http://PortableApps.com/BlenderPortable

;This software is OSI Certified Open Source Software.
;OSI Certified is a certification mark of the Open Source Initiative.

;This program is free software; you can redistribute it and/or
;modify it under the terms of the GNU General Public License
;as published by the Free Software Foundation; either version 2
;of the License, or (at your option) any later version.

;This program is distributed in the hope that it will be useful,
;but WITHOUT ANY WARRANTY; without even the implied warranty of
;MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;GNU General Public License for more details.

;You should have received a copy of the GNU General Public License
;along with this program; if not, write to the Free Software
;Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

!define NAME "BlenderPortable"
!define PORTABLEAPPNAME "Blender Portable"
!define APPNAME "Blender"
!define VER "1.6.5.3"
!define WEBSITE "PortableApps.com/BlenderPortable"
!define DEFAULTEXE "blender.exe"
!define DEFAULTAPPDIR "Blender"
!define DEFAULTPYTHONDIR "Python26"
!define DEFAULTSETTINGSDIR "settings"
!define LAUNCHERLANGUAGE "English"

;=== Program Details
Name "${PORTABLEAPPNAME}"
OutFile "..\..\${NAME}.exe"
Caption "${PORTABLEAPPNAME} | PortableApps.com"
VIProductVersion "${VER}"
VIAddVersionKey ProductName "${PORTABLEAPPNAME}"
VIAddVersionKey Comments "Allows ${APPNAME} to be run from a removable drive.  For additional details, visit ${WEBSITE}"
VIAddVersionKey CompanyName "PortableApps.com"
VIAddVersionKey LegalCopyright "John T. Haller"
VIAddVersionKey FileDescription "${PORTABLEAPPNAME}"
VIAddVersionKey FileVersion "${VER}"
VIAddVersionKey ProductVersion "${VER}"
VIAddVersionKey InternalName "${PORTABLEAPPNAME}"
VIAddVersionKey LegalTrademarks "PortableApps.com is a Trademark of Rare Ideas, LLC."
VIAddVersionKey OriginalFilename "${NAME}.exe"
;VIAddVersionKey PrivateBuild ""
;VIAddVersionKey SpecialBuild ""

;=== Runtime Switches
CRCCheck On
WindowIcon Off
SilentInstall Silent
AutoCloseWindow True
RequestExecutionLevel user

; Best Compression
SetCompress Auto
SetCompressor /SOLID lzma
SetCompressorDictSize 32
SetDatablockOptimize On

;=== Include
;(Standard NSIS)
!include FileFunc.nsh
!insertmacro GetParameters
!insertmacro GetParent
!insertmacro GetRoot

;(NSIS Plugins)

;(Custom)
!include ReadINIStrWithDefault.nsh

;=== Program Icon
Icon "..\..\App\AppInfo\appicon.ico"

;=== Icon & Stye ===

;=== Languages
LoadLanguageFile "${NSISDIR}\Contrib\Language files\${LAUNCHERLANGUAGE}.nlf"
!include PortableApps.comLauncherLANG_${LAUNCHERLANGUAGE}.nsh

Var PROGRAMDIRECTORY
Var PYTHONDIRECTORY
Var SETTINGSDIRECTORY
Var ADDITIONALPARAMETERS
Var EXECSTRING
Var WAITFORPROGRAM
Var PROGRAMEXECUTABLE
Var DISABLESPLASHSCREEN
Var ISDEFAULTDIRECTORY
Var MISSINGFILEORPATH
Var SECONDARYLAUNCH

Section "Main"
	${ReadINIStrWithDefault} $ADDITIONALPARAMETERS "$EXEDIR\${NAME}.ini" "${NAME}" "AdditionalParameters" ""
	${ReadINIStrWithDefault} $WAITFORPROGRAM "$EXEDIR\${NAME}.ini" "${NAME}" "WaitFor${APPNAME}" "false"
	${ReadINIStrWithDefault} $DISABLESPLASHSCREEN "$EXEDIR\${NAME}.ini" "${NAME}" "DisableSplashScreen" "false"

	IfFileExists "$EXEDIR\App\${DEFAULTAPPDIR}\${DEFAULTEXE}" "" NoProgramEXE
		StrCpy "$PROGRAMDIRECTORY" "$EXEDIR\App\${DEFAULTAPPDIR}"
		StrCpy "$PYTHONDIRECTORY" "$EXEDIR\App\${DEFAULTPYTHONDIR}"
		StrCpy "$SETTINGSDIRECTORY" "$EXEDIR\Data\${DEFAULTSETTINGSDIR}"
		StrCpy "$ISDEFAULTDIRECTORY" "true"
		StrCpy "$PROGRAMEXECUTABLE" "${DEFAULTEXE}"

		;=== Check Python directory
		IfFileExists "$EXEDIR\App\${DEFAULTPYTHONDIR}\*.*" "" PythonCommonFiles
			StrCpy $PYTHONDIRECTORY "$EXEDIR\App\${DEFAULTPYTHONDIR}"
			Goto EndINI

		PythonCommonFiles:
			${GetParent} "$EXEDIR" $0
			StrCpy $PYTHONDIRECTORY "$0\CommonFiles\Python26"
			GoTo EndINI
	
	EndINI:
		;=== Check if already running
		System::Call 'kernel32::CreateMutexA(i 0, i 0, t "${NAME}") i .r1 ?e'
		Pop $0
		StrCmp $0 0 CheckForEXE
			StrCpy $SECONDARYLAUNCH "true"
			StrCpy $DISABLESPLASHSCREEN "true"

	CheckForEXE:
		IfFileExists "$PROGRAMDIRECTORY\$PROGRAMEXECUTABLE" FoundProgramEXE
	
	NoProgramEXE:
		;=== Program executable not where expected
		StrCpy $MISSINGFILEORPATH $PROGRAMEXECUTABLE
		MessageBox MB_OK|MB_ICONEXCLAMATION `$(LauncherFileNotFound)`
		Abort

	FoundProgramEXE:
		;=== Check if already running
		StrCmp $SECONDARYLAUNCH "true" CheckForSettings
		FindProcDLL::FindProc "$PROGRAMEXECUTABLE"                                  
		StrCmp $R0 "1" WarnAnotherInstance CheckForSettings

	WarnAnotherInstance:
		MessageBox MB_OK|MB_ICONINFORMATION `$(LauncherAlreadyRunning)`
		Abort
	
	CheckForSettings:
		IfFileExists "$SETTINGSDIRECTORY\.blender\.B.blend" SettingsFound
		StrCmp $SECONDARYLAUNCH "true" SettingsFound
		;=== No settings found
		StrCmp $ISDEFAULTDIRECTORY "true" CopyDefaultSettings
		CreateDirectory $SETTINGSDIRECTORY
		Goto SettingsFound
	
	CopyDefaultSettings:
		CreateDirectory "$EXEDIR\Data"
		CreateDirectory "$EXEDIR\Data\settings"
		CopyFiles /SILENT $EXEDIR\App\DefaultData\settings\*.* $EXEDIR\Data\settings
		Goto SettingsFound

	SettingsFound:
		StrCmp $DISABLESPLASHSCREEN "true" SkipSplashScreen
			;=== Show the splash screen before processing the files
			InitPluginsDir
			File /oname=$PLUGINSDIR\splash.jpg "${NAME}.jpg"	
			newadvsplash::show /NOUNLOAD 1200 0 0 -1 /L $PLUGINSDIR\splash.jpg

	SkipSplashScreen:
		;=== Get any passed parameters
		${GetParameters} $0
		StrCmp "'$0'" "''" "" LaunchProgramParameters

		;=== No parameters
		StrCpy $EXECSTRING `"$PROGRAMDIRECTORY\$PROGRAMEXECUTABLE" `
		Goto AdditionalParameters

	LaunchProgramParameters:
		StrCpy $EXECSTRING `"$PROGRAMDIRECTORY\$PROGRAMEXECUTABLE" $0`

	AdditionalParameters:
		StrCmp $ADDITIONALPARAMETERS "" MoveSettings

		;=== Additional Parameters
		StrCpy $EXECSTRING `$EXECSTRING $ADDITIONALPARAMETERS`

	MoveSettings:
		StrCmp $SECONDARYLAUNCH "true" LaunchAndExit
		Sleep 100
		CopyFiles /SILENT $EXEDIR\Data\settings\.blender\*.* $EXEDIR\App\Blender\.blender
		CopyFiles /SILENT $EXEDIR\Data\settings\plugins\*.* $EXEDIR\App\Blender\plugins
		Sleep 100
		Goto BlenderSettingsFound
		
	BlenderSettingsFound:
		;=== Add Python to the %PATH% directory if we have a path, otherwise, skip it
		StrCpy $0 "$PYTHONDIRECTORY\Lib;$PYTHONDIRECTORY\DLLs;$PYTHONDIRECTORY\Lib\lib-tk;$PROGRAMDIRECTORY"
		System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PYTHONPATH", "$0").r0'
		System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("PYTHON_BASEPATH", "$PYTHONDIRECTORY").r0'

		;=== Create a subdirectory in data/settings and tell Blender that that is TEMP
		StrCpy $R0 "$EXEDIR\Data\settings\TEMP"
		IfFileExists $R0 SkipCreateTEMPDir
			CreateDirectory $R0

		SkipCreateTEMPDir:
			System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("TEMP", R0).r2'
			System::Call 'Kernel32::SetEnvironmentVariableA(t, t) i("TMP", R0).r2'
			StrCmp $SECONDARYLAUNCH "true" LaunchNow

	LaunchNow:
		ExecWait $EXECSTRING

	CheckRunning:
		Sleep 1000
		FindProcDLL::FindProc "${DEFAULTEXE}"                  
		StrCmp $R0 "1" CheckRunning
		Goto MoveBack
		
	MoveBack:
		CopyFiles /SILENT $EXEDIR\App\Blender\.blender\.B.blend $EXEDIR\Data\settings\.blender
		CopyFiles /SILENT $EXEDIR\App\Blender\.blender\tmp\*.* $EXEDIR\Data\settings\.blender\tmp
		Delete "$PROGRAMDIRECTORY\.blender\.B.blend"
		Delete "$PROGRAMDIRECTORY\.blender\tmp\*.*"
		RMDir "$PROGRAMDIRECTORY\.blender\tmp"
		Goto TheRealEnd
		
	LaunchAndExit:
		Exec $EXECSTRING
	
	TheRealEnd:
		newadvsplash::stop /WAIT
SectionEnd