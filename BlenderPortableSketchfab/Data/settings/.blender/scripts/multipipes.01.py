#!BPY
"""
Name: 'MultiPipes'
Blender: 248
Group: 'AddMesh'
"""
# MultiPipes
# v.0.01
# by harveen on BlenderArtists.org
#
# Description: MultiPipes creates a group of pipes with banded segements for
# use as quick background greeble piping for industrial, scifi or abstract models
#
# Based on Pipe Joints by Buerbaum Martin (Pontiac)
# http://gitorious.org/blender-scripts/blender-pipe-joint-script
# http://blenderartists.org/forum/showthread.php?t=154394
# http://wiki.blender.org/index.php/Extensions:Py/Scripts/Add/Pipe_Joint
#
# Also based on 'Parametric custom objects with Python' by Ari Hayrinen
# http://www.opendimension.org/blender_en/pymesh.php
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

import BPyAddMesh
import Blender
import math
from math import *
from Blender.Mathutils import Rand

def drawCircle(div, zPosition, vertIdx):
    verts = []
    curVertAngle = vertIdx * (2.0 * pi / div)
    locX = sin(curVertAngle)
    locY = cos(curVertAngle)
    locZ = zPosition
    verts = [locX, locY, locZ]
    return verts

"""
createFaces
    A very simple "bridge" tool.
    Connects two equaly long vertex-loops.
Parameters
    vertIdx1 ... List of vertex indices of the first loop.
    vertIdx2 ... List of vertex indices of the second loop.
"""
def createFaces(vertIdx1, vertIdx2):
    faces = []

    if (len(vertIdx1) != len(vertIdx2)) or (len(vertIdx1) < 2):
        return None

    total = len(vertIdx1)

    # Bridge the start with the end.
    faces.append([vertIdx2[0], vertIdx1[0], vertIdx1[total-1], vertIdx2[total-1]])

    # Bridge the rest of the faces.
    for num in range(total-1):
        faces.append([vertIdx1[num], vertIdx2[num], vertIdx2[num+1], vertIdx1[num+1]])

    return faces

# --------------------------------------------------------------------------
"""
addPipe
    Create the vertices and polygons for a simple pipe.
Parameters
    radius ... Radius of the pipe.
    div ... Number of vertices per circle/cross section.
    length ... Length of pipe
"""
def addPipe(radius=0.1, div=6, length=8.0, thickness=0.02, ratio=0.1, bands=10, xOffset=0, yOffset=0):
    verts = []
    faces = []
    segments = (bands*4) + 2 #82
    setsize = 4
    loop = [[] for n in range(segments)]
    zPosition = -(length/2)

# BANDS != segments

# NEW RAND CODE - generate random segments +Zpositions

    bandCoverage = length*ratio
    bandSlices = [0 for n in range(bands)]
    bandLengths = []

    # calculate outer band lengths
    for i in range(bands):
        while (bandSlices[i] < 1):
            randCut = Rand(1, 99)
            if randCut not in bandSlices:
                bandSlices[i] = randCut

    bandSlices.sort()

    for i in range(bands):
        if i == 0:
            bandLengths.append((length*ratio)*(bandSlices[i]/100.0))
        elif i == bands-1:
            bandLengths.append((length*ratio)-sum(bandLengths))
        elif i > 0 and i < bands-1:
            bandLengths.append(((length*ratio)*(bandSlices[i]/100.0))-sum(bandLengths))

    # calculate inner band lengths
    innerBands = bands+1
    innerRatio = (1.0 - ratio)
    innerSlices = [0 for n in range(innerBands)]
    innerLengths = []

    for i in range(innerBands):
        while (innerSlices[i] < 1):
            randCut = Rand(1, 99)
            if randCut not in innerSlices:
                innerSlices[i] = randCut

    innerSlices.sort()

    for i in range(innerBands):
        if i == 0:
            innerLengths.append((length*innerRatio)*(innerSlices[i]/100.0))
        elif i == innerBands-1:
            innerLengths.append((length*innerRatio)-sum(innerLengths))
        elif i > 0 and i < innerBands-1:
            innerLengths.append(((length*innerRatio)*(innerSlices[i]/100.0))-sum(innerLengths))

# END NEW RAND CODE

    # start circle
    for vertIdx in range(div):
        circlePoint = drawCircle(div,zPosition,vertIdx)
        loop[0].append(len(verts))
        verts.append([(circlePoint[0] * radius)+xOffset, (circlePoint[1] * radius)+yOffset, circlePoint[2]])

    # middle circles
    segmentCount = 0
    for n in range((segments-2)/setsize): #10  = (42-2)/4
        for i in range(setsize): #4 (0-3)
            newRadius = radius

            if i == 0:
                zPosition += innerLengths[segmentCount]
            if i == 1:
                newRadius = radius+thickness
            if i == 2:
                newRadius = radius+thickness
                zPosition += bandLengths[segmentCount]

            for vertIdx in range(div):
                circlePoint = drawCircle(div,zPosition,vertIdx)
                loop[i+(n*(setsize))+1].append(len(verts))
                verts.append([(circlePoint[0] * newRadius)+xOffset, (circlePoint[1] * newRadius)+yOffset, circlePoint[2]])
        segmentCount += 1

    # end circle
    zPosition = length/2
    for vertIdx in range(div):
        circlePoint = drawCircle(div,zPosition,vertIdx)
        loop[segments-1].append(len(verts))
        verts.append([(circlePoint[0] * radius)+xOffset, (circlePoint[1] * radius)+yOffset, circlePoint[2]])

    # Create faces
    for j in range(segments-1):
        faces.extend(createFaces(loop[j], loop[j+1]))

    return verts, faces


def main():

    # Numeric input for default values
    pipesInput = Blender.Draw.Create(5)
    rowsInput = Blender.Draw.Create(1)
    maxRadiusInput = Blender.Draw.Create(0.4)
    minRadiusInput = Blender.Draw.Create(0.1)
    divInput  = Blender.Draw.Create(6)
    maxLengthInput  = Blender.Draw.Create(12.0)
    minLengthInput  = Blender.Draw.Create(12.0)
    maxThicknessInput = Blender.Draw.Create(0.15)
    minThicknessInput = Blender.Draw.Create(0.05)
    maxRatioInput = Blender.Draw.Create(0.10)
    minRatioInput = Blender.Draw.Create(0.02)
    maxBandsInput = Blender.Draw.Create(12)
    minBandsInput = Blender.Draw.Create(4)
    padInput = Blender.Draw.Create(0.02)

    # array for popup window's content
    block = []

    # add inputs to array with title, min/max values and tooltip
    block.append(("pipes: ", pipesInput, 1, 100, "number of pipes per row"))
    block.append(("rows: ", rowsInput, 1, 100, "number of rows"))
    block.append(("divisions: ", divInput, 4, 100, "number of divisions"))
    block.append(("max length: ", maxLengthInput, 0.01, 100, "maximum length of the pipe"))
    block.append(("min length: ", minLengthInput, 0.01, 100, "minimum length of the pipe"))
    block.append(("max radius: ", maxRadiusInput, 0.01, 100, "maximum radius range of the pipe"))
    block.append(("min radius: ", minRadiusInput, 0.01, 100, "minimum radius range of the pipe"))
    block.append(("max bands: ", maxBandsInput, 1, 100, "maximum bands per pipe"))
    block.append(("min bands: ", minBandsInput, 1, 100, "minimum bands per pipe"))
    block.append(("max thickness: ", maxThicknessInput, 0.01, 100,
        "maximum band thickness as percent of radius"))
    block.append(("min thickness: ", minThicknessInput, 0.01, 100,
        "minimum band thickness as percent of radius"))
    block.append(("max coverage: ", maxRatioInput, 0.01, 0.99, "coverage ratio of band to pipe"))
    block.append(("min coverage: ", minRatioInput, 0.01, 0.99, "coverage ratio of band to pipe"))
    block.append(("padding: ", padInput, 0.000, 100, "space between pipes"))

    # draw    popup if it is not open allready
    if not Blender.Draw.PupBlock("Create MultiPipes",block):
        return

    prevXOffset = 0.0
    prevYOffset = 0.0

    for j in range(rowsInput.val):
        for i in range(pipesInput.val):

            # set pipe length from user max min
            if minLengthInput.val > maxLengthInput.val:
                pipeLength = Rand(maxLengthInput.val,minLengthInput.val)
            elif maxLengthInput.val == minLengthInput.val:
                pipeLength = maxLengthInput.val
            elif maxLengthInput.val > minLengthInput.val:
                pipeLength = Rand(minLengthInput.val,maxLengthInput.val)

            # set pipe radius from user max min
            if minRadiusInput.val > maxRadiusInput.val:
                pipeRadius = Rand(maxRadiusInput.val,minRadiusInput.val)
            elif maxRadiusInput.val == minRadiusInput.val:
                pipeRadius = maxRadiusInput.val
            elif maxRadiusInput.val > minRadiusInput.val:
                pipeRadius = Rand(minRadiusInput.val,maxRadiusInput.val)

            #set number of bands from user max min
            if minBandsInput.val > maxBandsInput.val:
                numBands = Rand(maxBandsInput.val,minBandsInput.val)
            elif maxBandsInput.val == minBandsInput.val:
                numBands = maxBandsInput.val
            elif maxBandsInput.val > minBandsInput.val:
                numBands = Rand(minBandsInput.val,maxBandsInput.val)

            #set bands coverage ratio from user max min
            if minThicknessInput.val > maxThicknessInput.val:
                thickness = Rand(maxThicknessInput.val,minThicknessInput.val)
            elif maxThicknessInput.val == minThicknessInput.val:
                thickness = maxThicknessInput.val
            elif maxThicknessInput.val > minThicknessInput.val:
                thickness = Rand(minThicknessInput.val,maxThicknessInput.val)

            thickness = thickness*pipeRadius

            #set bands coverage ratio from user max min
            if minRatioInput.val > maxRatioInput.val:
                coverage = Rand(maxRatioInput.val,minRatioInput.val)
            elif maxRatioInput.val == minRatioInput.val:
                coverage = maxRatioInput.val
            elif maxRatioInput.val > minRatioInput.val:
                coverage = Rand(minRatioInput.val,maxRatioInput.val)

            if i == 0:
                xOffset = 0.0
                prevXOffset = pipeRadius + thickness
                if j == 0:
                    yOffset = 0.0
                    prevYOffset = maxRadiusInput.val + maxThicknessInput.val
                elif j > 0:
                    yOffset = prevYOffset + padInput.val + maxRadiusInput.val + maxThicknessInput.val
                    prevYOffset = yOffset + maxRadiusInput.val + maxThicknessInput.val
            elif i > 0:
                xOffset = prevXOffset + padInput.val + pipeRadius + thickness
                prevXOffset = xOffset + pipeRadius + thickness
                if j == 0:
                    if prevYOffset < (maxRadiusInput.val + maxThicknessInput.val):
                        prevYOffset = maxRadiusInput.val + maxThicknessInput.val
                if j > 0:
                    if prevYOffset < (yOffset + maxRadiusInput.val + maxThicknessInput.val):
                        prevYOffset = yOffset + maxRadiusInput.val + maxThicknessInput.val

            verts, faces = addPipe(pipeRadius, divInput.val, pipeLength, thickness, coverage, int(numBands), xOffset, yOffset)

            BPyAddMesh.add_mesh_simple('MultiPipes', verts, [], faces)

main()