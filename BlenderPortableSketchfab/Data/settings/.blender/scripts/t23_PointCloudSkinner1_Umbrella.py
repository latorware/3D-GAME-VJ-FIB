#!BPY
"""Registration info for Blender menus:
Name: 'Skin Vertices and Make Faces'
Blender: 240
Group: 'Mesh'
Tooltip: 'You can get a complete 3D mesh out of just vertices that have no edges or faces.'
"""

__scriptname__ = 'Point Cloud Skinner Umbrella'
__author__ = 'Hans.P.G.'
__version__ = 'v0.14 20090118, t23'
__url__ = ["Hans.P.G. Homepage, http://hanspg.web.fc2.com/Pages/index.html"]
#__bpydoc__ = """ """


# Change logs:
#  ToDo:
#   +display the state with a progress bar.
#   +fix the intersection of faces that still appears in many cases.
#   +decide the parameters automatically according to given clouds.
#   +change the values of the parameters during skinning automatically.
#  2009/01/18 v0.14, t23
#   +added a new UI mode which allows you to use the script from the 
#    menu Mesh in Blender. You can set the parameters quickly in the new  
#    popup block. 
#   +can switch the UI mode. The popup UI will be display if the 3D 
#    window is in EditMode, and the script GUI will be display in 
#    otherwise.
#  2009/01/11 v0.13, t21
#   +Corrected the function CalcAverageNormal. The algorithm is based 
#    on Lagrange's Lambda Method minimizing of sum(ax+by+cz)^2, which 
#    is the real minimization of the distances between vertices and the 
#    center, instead of least squares using ax+by+cz=1 in v0.13 or older.
#  2008/11/16 v0.12, t19
#   +The script name was changed and it's going to be called Point 
#    Cloud Skinner 1 Umbrella instead of Point Cloud to 3D Mesh, 
#    because another way of skinning has been created and it's called 
#    Point Cloud Skinner 2 Carapace.
#   +A GUI was added to make it easy to setup, using the module Blender
#    GUI Provider. The module code has been appended to t15 simply.
#   +TimeProfiler was created to measure process time, and the code 
#    was included into t19.
#   +PointsGridManager has been improved to collect vertices faster by
#    using hash values for keys of the dictionary that contains the 
#    grid cells.
#  2008/02/03 v0.11, t15
#   +created PointsGridManager class to manage a lot of vertices with a 
#    meshed grid. It allows you to gather vertices that are located in 
#    a distance with less time consumption.
#   +changed the process of checking the internal angles. Now it can 
#    check more correctly if the triangle outside has shaper angle than 
#    the triangle around center, and can avoid discarding the vertices.
#  2008/01/18 v0.10, t14
#   +changed the script to use average normal and added a new parameter
#    gb["MaxDistForAxis"] to set the distance in which it gathers 
#    vertices to decide the average normal.
#   +fixed the bug that causes an error in the process of checking the 
#    internal angles. It was solved by checking the length of NeigVert2
#    - NeigVert1.
#  2008/01/17 v0.9, t13
#   +The upgrade for checking the internal angles in t12 has two
#    problems and they could make a shape triangle because of missing
#    to reduce unnecessary vertices, and it has been fixed in t13. (One
#    of two was solved by enabling the vertex if its neighbor vertex is
#    in unable region in SomeEndVerts state, and the other was by 
#    enabling the vertex if it and its both neighbor vertices form a 
#    shaper triangle.)
#   +It has been found that the fixes above cause another problem near
#    the edges of the surface with making a shape triangle, and it has
#    been also fixed.
#  2008/01/16 v0.8, t12
#   +upgraded the functionality of checking the adjacent 2 triangles and
#    can reorganize the triangles into good shapes.
#   +modified the way of checking the internal angles using a new concept.
#    It can avoid the intersection of faces that will come from reducing
#    the vertices by the checking.
#  2008/01/06 v0.7, t10
#   +upgraded the functionality of checking the internal angles and can 
#    check if the angle is too small or large.
#  2007/12/10 v0.6, t7
#   +added the functionality to avoid making intersection of faces, but 
#    some faces still have intersection in a noisy point cloud.
#    (To avoid the intersection, it looks at faces that have been already 
#    made, and such a face is called a face-end face in the script. First 
#    it searches for face-end edges that are just connected to the center 
#    vertex and groups the vertices by the edges. Next in each group it 
#    searches for the other face-end edges and discards the vertices that 
#    are hidden by the edges. And it makes faces out of the left vertices.)
#   +haven't yet upgraded the functionality of checking the internal 
#    angles for the new version, so removed the previous codes.
#   +haven't yet upgraded the functionality of checking the adjacent
#    triangles for the new version, so commented out the codes now.
#  2007/11/29 v0.5, t6
#   +created FacesManager class to manage faces. It provides you with an 
#    easy way to find the faces that include a specified vertex. The 
#    purpose is to find the already made faces to avoid making overlapping 
#    faces. 
#  2007/11/29 v0.4, t5
#   +separated the algorithm code in MakeFacesAround into some smaller 
#    methods because the code length started to be long. Also changed the 
#    way to send data to those methods and now use Data class to send it.
#  2007/11/22 v0.3, t4
#   +can check if angles between adjacent 2 vertices are acceptable.
#   +can check if adjacent 2 triangles have appropriate shapes.
#   +changed the way of sending faces' information to downward 
#    functionalities in the algorithm and now treat it in the same unified 
#    data structure everywhere.
#  2007/11/18 v0.2, t3
#   +the algorithm has not changed but a few codes changed to make it easy 
#    to read, for example changing into gb["*"] style, compacting for loop
#    codes.
#  2007/11/16 v0.1, t2
#   +t1 code was separated and t2 started newly to concentrate on the 
#    development for skinning a point cloud.
#   +implemented a simple algorithm to make faces around each vertex.
#                                                                      END


#******************************
#---===Import declarations===
#******************************

from math import *
from copy import *
import Blender as B
import Blender.Mathutils as BM
BVec = BM.Vector
BMat = BM.Matrix


#******************************
#---===Global parameters===
#******************************

gb = {}
gb["TargetObject"] = "Plane" # Object name
gb["MaxAroundDist"] = 0.1
gb["MaxDistForAxis"] = 0.2
gb["MaxAroundCount"] = 10
gb["MinVertsAngle"] = 25
gb["MaxVertsAngle"] = 135
gb["GridSize"] = [0.3] * 3
gb["PrecisionLevel"] = 2
gb["TargetVertsMode"] = 1 # 0: skin all vertices, 1: skin selected vertices
gb["IgnoreErrors"] = True

gbLog = {}


#******************************
#---===Skin vertices===
#******************************

def SkinVerts():
    
    # Reset log data
    gbLog["TargetVerts"] = 0
    gbLog["MadeFaces"] = 0
    gbLog["FewVertsCases"] = 0
    gbLog["FullFacesCases"] = 0
    gbLog["TooSmallVertsAngles"] = 0
    gbLog["TooLargeVertsAngles"] = 0
    gbLog["ModifiedTriangles"] = 0
    gbLog["Errors"] = 0
    gbLog["Warnings"] = {"NZ1": 0, "NZ2": 0, "NZ3": 0}

    # Comes out of EditMode temporarily
    lcEditMode = B.Window.EditMode()
    if lcEditMode:
        B.Window.EditMode(0)

    gbTP.Start("Others")
    
    # Get mesh instance
    try:
        lcObj = B.Object.Get(gb["TargetObject"])
    except ValueError:
        B.Draw.PupMenu("Error: The object \"" + gb["TargetObject"] + "\" is not found.%t|Please specify the object name that you want to skin.")
        return
    lcMesh = B.Mesh.Get(lcObj.getData().name)
#    lcObjSize = [lcObj.SizeX, lcObj.SizeY, lcObj.SizeZ]

    # PointsGridManager initializes Grid from the existing vertices
    lcGridMana = PointsGridManager(gb["GridSize"])
    lcGridMana.PositionGetter = GetPositionFromMVert
    lcGridMana.Add(lcMesh.verts)
    lcGridMana.PrecisionLevel = gb["PrecisionLevel"]
    
    # FacesManager initializes Verts from the existing faces
    lcFaceMana = FacesManager(lcMesh)
    lcFaceMana.Import()
    
    # Process all vertices
    for enVert in lcMesh.verts:
        enIndex = enVert.index
        
        if gb["TargetVertsMode"] == 1:
            if lcMesh.verts[enIndex].sel == 0:
                continue
        
        gbTP.Start("+ 1 Select a vertex")
        
        lcData = ProcessingDataTransfer()
        lcData.Mesh = lcMesh
        lcData.CenterVert = enVert
        lcData.FacesManager = lcFaceMana
        lcData.GridManager = lcGridMana
        
        # Make faces around center vertex
        if gb["IgnoreErrors"]:
            try:
                MakeFacesAroundCenterVert(lcData)
            except:
                gbLog["Errors"] += 1
#                lcMesh.verts[enIndex].sel = 1 # Select the vertex if error
        else:
            MakeFacesAroundCenterVert(lcData)
        
        gbLog["TargetVerts"] += 1
        
    lcFaceMana.Bake()

    gbTP.End()

    # Restore the state of EditMode
    if lcEditMode:
        B.Window.EditMode(1)
    
    B.Redraw()

class ProcessingDataTransfer:
    def __init__(self):
        self.Mesh = None
        self.CenterVert = None # In form of MVert
        self.GridManager = None
        self.FacesManager = None
        self.VertsAround = None # In form of [MVert, ...]
        self.VertsForAxis = None # In form of [MVert, ...]
        self.ZAxis = None # In form of 3x1 Blender.Vector
        self.XYTransMat = None # In form of 3x3 Blender.Matrix
        self.XYZTransMat = None # In form of 3x3 Blender.Matrix
        self.EndVerts = None # In form of [EndVert, ...]
        self.EndState = None # In form of string
        self.VertGroups = None # In form of [VertsAround, ...]
        self.EndEdges = None # In form of [[MVert, MVert], ...]
        self.MakeFace = None # In form of [T or F, ...]
        self.FaceGroups = None # In form of [Faces, ...]
        self.Faces = None # In form of [[Index, Index, Index], ...]

# Make faces around center vertex
def MakeFacesAroundCenterVert(inData):
    
    gbTP.Start("+ 2 GatherCloserVertsAroundCenter")
    
    # Gather closer vertices around
    if not GatherCloserVertsAroundCenter(inData): return True
    
    gbTP.Start("+ 3 GatherCloserVertsForAxis")
    
    # Gather closer vertices around to decide axis
    if not GatherCloserVertsForAxis(inData): return True
    
    gbTP.Start("+ 4 DefindFrameToMeasureAngles")
    
    # Defind frame to measure angles
    DefindFrameToMeasureAngles(inData)
    
    gbTP.Start("+ 5 GetFaceEndVertsAroundCenterAndSort")

    # Get face-end vertices around and sort them
    if not GetFaceEndVertsAroundCenterAndSort(inData): return True
    
    gbTP.Start("+ 6 DoAdditionalSearch")
    
    # Do additional search for vertices outside
    DoAdditionalSearch(inData)
    
    gbTP.Start("+ 7 SortVertsGatheredAround")

    # Sort vertices gathered around
    SortVertsGatheredAround(inData)
    
    gbTP.Start("+ 8 GroupVertsByFaceEndVerts")
    
    # Separate vertices by already existing faces
    GroupVertsByFaceEndVerts(inData)
    
    inData.FaceGroups = []
    for enVertGroup in inData.VertGroups:
        
        gbTP.Start("+ 8-+1 Initialize lcData")
        
        # Initialize lcData
        lcData = copy(inData)
        lcData.VertsAround = enVertGroup
        lcData.MakeFace = [True] * len(enVertGroup)
        
        gbTP.Start("+ 8-+2 GatherAllFaceEndEdges")
        
        # Gather all face-end edges in each group
        GatherAllFaceEndEdges(lcData)
        
        gbTP.Start("+ 8-+3 CheckIfAnglesAreTooSmall")
        
        # Check if angles between adjacent 2 vertices are too small
        CheckIfAnglesAreTooSmall(lcData)
        
        gbTP.Start("+ 8-+4 DiscardVertsHiddenByFaceEnds")
        
        # Discard vertices hidden by face-end edges
        DiscardVertsHiddenByFaceEnds(lcData)
        
        gbTP.Start("+ 8-+5 CheckIfAnglesAreTooLarge")
        
        # Check if angles between adjacent 2 vertices are too large
        CheckIfAnglesAreTooLarge(lcData)
        
        gbTP.Start("+ 8-+6 MakeFacesAroundSimply")
        
        # Make faces around simply
        MakeFacesAroundSimply(lcData)
        
        inData.FaceGroups.append(lcData.Faces)
    
    gbTP.Start("+ 9 CombineFacesInAllVertGroups")
    
    # Combine all of faces that have been made in each group
    CombineFacesInAllVertGroups(inData)
    
    gbTP.Start("+10 CheckIfTrianglesHaveGoodShapes")
    
    # Check if adjacent 2 triangles have good shapes
    CheckIfTrianglesHaveGoodShapes(inData)
    
    gbTP.Start("+11 RegisterFacesToFacesManager")
    
    # Extend faces in faces manager
    RegisterFacesToFacesManager(inData)
    
    gbTP.Start("Others")
    
    return True

# Gather closer vertices around
def GatherCloserVertsAroundCenter(inData):
    inCenterVert = inData.CenterVert
    lcGridMana = inData.GridManager
    
    # Gather closer vertices around
    lcVertsAround = lcGridMana.GetVertsInDistance(inCenterVert.co, gb["MaxAroundDist"])
    # Sort vertices by distance
    lcDists = [((enVert.co - inCenterVert.co).length, enVert) for enVert in lcVertsAround]
    lcDists.sort()
    outVertsAround = [enVert for tmpDist, enVert in lcDists]
    # Gather closer vertices if VertsAround has a lot of vertices
    if len(outVertsAround) < 2:
        gbLog["FewVertsCases"] += 1
        return False
    elif len(outVertsAround) >= gb["MaxAroundCount"]:
        outVertsAround = outVertsAround[:gb["MaxAroundCount"]]
    
    inData.VertsAround = outVertsAround
    return True

# Gather closer vertices around to decide axis
def GatherCloserVertsForAxis(inData):
    inCenterVert = inData.CenterVert
    lcGridMana = inData.GridManager
    
    # Gather closer vertices around
    outVertsForAxis = lcGridMana.GetVertsInDistance(inCenterVert.co, gb["MaxDistForAxis"])
    if len(outVertsForAxis) < 2:
        gbLog["FewVertsCases"] += 1
        return False
    
    inData.VertsForAxis = outVertsForAxis
    return True
    
# Defind frame to measure angles
def DefindFrameToMeasureAngles(inData):
    # Assume: CalcAverageNormal returns a normalized vector for the axis
    inCenterVert = inData.CenterVert
    inVertsForAxis = inData.VertsForAxis

    # Calculate z-axis to measure angles
    outZAxis = CalcAverageNormal(inCenterVert, inVertsForAxis)
    # Decide a vertex as direction of x-axis
    for enVert in inVertsForAxis:
        lcXAxis = enVert.co - inCenterVert.co
        # Calcuate y-axis by crossing z,x-axes
        lcYAxis = BM.CrossVecs(outZAxis, lcXAxis)
        if lcYAxis.length != 0: break # x,z-axes must not be parallel
    lcYAxis = lcYAxis.normalize()
    lcXAxis = BM.CrossVecs(lcYAxis, outZAxis)
    outXYTransMat = BMat(lcXAxis, lcYAxis, [0, 0, 0])
    outXYZTransMat = BMat(lcXAxis, lcYAxis, outZAxis)

    inData.ZAxis = outZAxis
    inData.XYTransMat = outXYTransMat
    inData.XYZTransMat = outXYZTransMat
    return True

class MEndVert:
    def __init__(self, inMVert):
        self.Vert = inMVert
        self.co = inMVert.co
        self.index = inMVert.index
        self.Order = None
        self.Outside = None
        self.Opposite = None
        self.Direction = None
    
    def __repr__(self):
        return "[EndVert" + repr(self.Vert)[6:]
    
    def MEndVert(self): pass

def Is_MEndVert(o):
    try:
        o.MEndVert
        return True
    except AttributeError:
        return False

# Get face-end vertices around a given vertex
def GetFaceEndVerts(inData, inCenterVert):
    inMesh = inData.Mesh
    inMana = inData.FacesManager
    inVertsAround = inData.VertsAround
    
    # Gather vertices that make faces around center vertex, and sort it
    lcVertIndices = []
    lcCenterIndex = inCenterVert.index
    for enFace in inMana[lcCenterIndex]:
        enFace = enFace[:] # [:] is needed to copy array
        enFace.remove(lcCenterIndex)
        # Add (index, opposite index)
        lcVertIndices.append((enFace[0], enFace[1]))
        lcVertIndices.append((enFace[1], enFace[0]))
    lcVertIndices.sort()
    # Gather face-end vertices by checking vertex duplication
    outEndVerts = []
    n = len(lcVertIndices)
    for i in xrange(n):
        lcPrevIndex, tmpIndex = lcVertIndices[(i - 1) % n]
        lcIndex, lcOpposite = lcVertIndices[(i + 0) % n]
        lcNextIndex, tmpIndex = lcVertIndices[(i + 1) % n]
        if lcIndex == lcPrevIndex: continue # Ignore duplicated vertices
        if lcIndex == lcNextIndex: continue # Ignore duplicated vertices

        enVert = inMesh.verts[lcIndex]
        # Create EndVert instead of MVert to give additional info
        lcEndVert = MEndVert(enVert)
        for j, enVertAround in enumerate(inVertsAround):
            if enVertAround.index == enVert.index: # Have to compare index because VertsAround migth have both of MVert and EdVert
                lcEndVert.Order = j
                lcEndVert.Outside = False
                break
        if lcEndVert.Outside != False: # It means case where enVert wasn't found in VertsAround
            lcEndVert.Outside = True
        lcEndVert.Opposite = lcOpposite
        outEndVerts.append(lcEndVert)
    
    # Assign current state of EndVerts (T: some EndVerts, N: no EndVerts, F: full faces)
    if len(outEndVerts) > 0:
        outEndState = "SomeEndVerts"
    elif len(inMana[lcCenterIndex]) == 0:
        outEndState = "NoEndVerts"
    else:
        outEndState = "FullFaces"

    return outEndVerts, outEndState

# Get face-end vertices around center vertex, and sort them
def GetFaceEndVertsAroundCenterAndSort(inData):
    inMesh = inData.Mesh
    inCenterVert = inData.CenterVert
    inMana = inData.FacesManager
    inVertsAround = inData.VertsAround
    inZAxis = inData.ZAxis
    
    # Gather face-end vertices
    outEndVerts, outEndState = GetFaceEndVerts(inData, inCenterVert)
    if outEndState == "FullFaces":
        gbLog["FullFacesCases"] += 1
        return False
    # Replace MVert with EndVert and add direction info
    for enEndVert in outEndVerts:
        enOppoVert = inMesh.verts[enEndVert.Opposite]
        # Replace MVert with EndVert in VertsAround
        if enEndVert.Outside:
            inVertsAround.append(enEndVert) # Have to add it because it is outside
        else:
            inVertsAround[enEndVert.Order] = enEndVert
        # Add direction that shows which side of face-end edge has face
        lcVert2, lcOppoVert2 = (enVert.co - inCenterVert.co for enVert in [enEndVert, enOppoVert])
        lcAngle = VecsAngle2(lcVert2, lcOppoVert2, inZAxis)
        enEndVert.Direction = sign(lcAngle - 180)

    # Sort face-end vertices
    outEndVerts = SortVertsAroundZAxis(inData, outEndVerts)

    inData.EndVerts = outEndVerts
    inData.EndState = outEndState
    return True

# Do additional search for vertices outside
def DoAdditionalSearch(inData):
    # Assume: EndVerts has been setup and sorted around ZAxis.
    inCenterVert = inData.CenterVert
    lcGridMana = inData.GridManager
    inVertsAround = inData.VertsAround
    inXYZTransMat = inData.XYZTransMat
    inEndVerts = inData.EndVerts
    
    # Do additional search if either or both EndVerts are outside
    n = len(inEndVerts)
    for i in xrange(n):
        lcEndVerts = [inEndVerts[j % n] for j in [i, i + 1]]
        if not lcEndVerts[0].Direction > 0: continue
        if not lcEndVerts[0].Outside and not lcEndVerts[1].Outside: continue
        lcBase2 = [inXYZTransMat * (lcEndVerts[j].co - inCenterVert.co) for j in xrange(2)]
        lcMat = BMat([lcBase2[0] * lcBase2[0], lcBase2[0] * lcBase2[1]], [lcBase2[1] * lcBase2[0], lcBase2[1] * lcBase2[1]]).invert()
        lcZAxis = BM.CrossVecs(lcBase2[0], lcBase2[1]).normalize()
        # Gather vertices for additional search
        lcSearchLength = max((lcEndVerts[j].co - inCenterVert.co).length for j in xrange(2))
        lcSearchVerts = lcGridMana.GetVertsInDistance(inCenterVert.co, lcSearchLength, 1)
        # Search for additional vertices
        for enVert in lcSearchVerts:
            lcVert = enVert.co - inCenterVert.co
            if lcVert.length < gb["MaxAroundDist"]: continue
            lcVert2 = inXYZTransMat * lcVert
            lcVec = BVec(lcBase2[0] * lcVert2, lcBase2[1] * lcVert2)
            lcAns = lcMat * lcVec
            lcAns = [lcAns[0], lcAns[1], lcZAxis * lcVert2]
            if lcAns[0] <= 0 or lcAns[1] <= 0 or lcAns[0] + lcAns[1] >= 1: continue
            if abs(lcAns[2]) >= gb["MaxAroundDist"]: continue
            inVertsAround.append(enVert)
    
    return True

# Sort vertices around z-axis
def SortVertsAroundZAxis(inData, inVerts):
    inCenterVert = inData.CenterVert
    inXYTransMat = inData.XYTransMat

    # Transform vertices to defined frame
    lcVerts2 = [(inXYTransMat * (enVert.co - inCenterVert.co), enVert) for enVert in inVerts]
    # Measure angles and sort vertices by angle around z-axis
    lcAngles = [(PointAngleOnXY(enVert2), enVert) for enVert2, enVert in lcVerts2]
    lcAngles.sort()
    # Pull out sorted vertices
    outVertsAround = [enVert for tmpAngle, enVert in lcAngles]

    return outVertsAround

# Sort vertices gathered around
def SortVertsGatheredAround(inData):
    inData.VertsAround = SortVertsAroundZAxis(inData, inData.VertsAround)
    return True

# Separate vertices by faces that already exist around center vertex and make groups
def GroupVertsByFaceEndVerts(inData):
    # Assume: VertsAround has been sorted around ZAxis.
    # Assume: VertsAround has some MEndVerts, which shows the search for face-end vertices has been finished.
    inVertsAround = inData.VertsAround
    inEndVerts = inData.EndVerts
    inEndState = inData.EndState
    
    # Assign array straight or empty if EndVerts are not found
    if inEndState == "NoEndVerts":
        inData.VertGroups = [inVertsAround]
        return True
    
    # Find face-end vertex that has plus direction
    for i, enVert in enumerate(inVertsAround):
        if Is_MEndVert(enVert) and enVert.Direction > 0:
            lcStart = i
    # Group vertices from face-end vertex to another
    outVertGroups = []
    lcIsInGroup = False
    n = len(inVertsAround)
    for i in xrange(lcStart, lcStart + n): # Error will happen here when intersection of faces exists
        enVert = inVertsAround[i % n]
        if Is_MEndVert(enVert):
            if enVert.Direction > 0:
                lcVertGroup = []
                lcIsInGroup = True
            else:
                lcVertGroup.append(enVert) # Have to add last one because of turning flag to false
                outVertGroups.append(lcVertGroup)
                lcIsInGroup = False
        if lcIsInGroup:
            lcVertGroup.append(enVert)
    
    inData.VertGroups = outVertGroups
    return True

# Gather all face-end edges in each group
def GatherAllFaceEndEdges(inData):
    inCenterVert = inData.CenterVert
    inVertsAround = inData.VertsAround
    inEndState = inData.EndState
    
    # Gather all face-end edges in VertsAround
    outEndEdges = []
    for i, enVert in enumerate(inVertsAround):
        # Get face-end vertices around each vertex
        lcEndVerts, lcState = GetFaceEndVerts(inData, enVert)
        if not lcState == "SomeEndVerts": continue
        # Gather face-end edges in edges connected to enVert
        lcEndEdges = []
        for enEndVert in lcEndVerts:
            if enEndVert.Outside: continue
            if enEndVert.Order < i: continue
            lcEndEdges.append([enVert, enEndVert])
        outEndEdges.extend(lcEndEdges)
    if inEndState == "SomeEndVerts":
        # Add edges including center vertex
        outEndEdges.append([inCenterVert, inVertsAround[ + 0]])
        outEndEdges.append([inCenterVert, inVertsAround[ - 1]])
    
    inData.EndEdges = outEndEdges
    return True

# Discard vertices hidden by face-end edges
def DiscardVertsHiddenByFaceEnds(inData):
    inCenterVert = inData.CenterVert
    inVertsAround = inData.VertsAround
    inXYTransMat = inData.XYTransMat
    inEndEdges = inData.EndEdges
    
    # Add flags that represent whether or not vertex should be discarded
    lcIsHidden = [False] * len(inVertsAround)
    # Check if each vertex is hidden by each face-end edge
    for enEndEdge in inEndEdges:
        lcVec2 = [inXYTransMat * (enVert.co - inCenterVert.co) for enVert in enEndEdge]
        try:
            lcInv = BMat([lcVec2[0] * lcVec2[0], lcVec2[0] * lcVec2[1]], [lcVec2[1] * lcVec2[0], lcVec2[1] * lcVec2[1]]).invert()
        except ValueError: # Matrix doesn't have inverse becuase vectors in Vec2 are parallel or its length is 0
            continue
        for i, enVert in enumerate(inVertsAround):
            enHidden = lcIsHidden[i]
            if enHidden: continue
            if enVert.index == enEndEdge[0].index: continue # Must compare with index because MVert and EndVert are mixed
            if enVert.index == enEndEdge[1].index: continue
            # Check if vertex is hidden by shadow made from face-end edge
            lcVert2 = inXYTransMat * (enVert.co - inCenterVert.co)
            lcAns = lcInv * BVec(lcVec2[0] * lcVert2, lcVec2[1] * lcVert2)
            if lcAns[0] < 0 or lcAns[1] < 0 or lcAns[0] + lcAns[1] < 1: continue
            # Trun on flag to discard this vertex
            lcIsHidden[i] = True
    # Pull out left vertices all
    outVertsAround = [enVert for i, enVert in enumerate(inVertsAround) if not lcIsHidden[i]]

    inData.VertsAround = outVertsAround
    return True

# Check if angles between adjacent 2 vertices are too small
def CheckIfAnglesAreTooSmall(inData):
    # Assume: VertsAround has been sorted around ZAxis.
    inCenterVert = inData.CenterVert
    inVertsAround = inData.VertsAround
    inZAxis = inData.ZAxis
    inEndState = inData.EndState
    
    n = len(inVertsAround)
    lcEnables = [False] * n
    # Measure all distances between vertices and z-axis and sort vertices by them
    lcLengths = []
    if inEndState == "SomeEndVerts":
        lcRange = xrange(1, n - 1)
    else:
        lcRange = xrange(n)
    for i in lcRange:
        enVert = inVertsAround[i]
        lcVec = enVert.co - inCenterVert.co
        # Measure distance between vertex and z-axis
        lcLength = sqrt(lcVec.length ** 2 - (lcVec * inZAxis) ** 2)
        lcLengths.append([lcLength, i])
    # Sort vertices by distance
    lcLengths.sort()
    
    # Get both adjacent vertices that has been enabled
    def GetAdjacentEnabledVerts(inIndex):
        for i in xrange(inIndex + 1, inIndex + n, + 1):
            if not lcEnables[i % n]: continue
            lcVertL = inVertsAround[i % n]
            break
        for i in xrange(inIndex - 1, inIndex - n, - 1):
            if not lcEnables[i % n]: continue
            lcVertR = inVertsAround[i % n]
            break
        return lcVertL, lcVertR
    
    # Check if vertex is in unable region and return True if it is in
    def CheckIfItIsInUnableRegion(inVert, inRegion):
        lcVec = inVert.co - inRegion["Vec0"]
        lcAns = inRegion["Inv"] * BVec(inRegion["Vec1"] * lcVec, inRegion["Vec2"] * lcVec)
        if lcAns[0] == 0 or lcAns[1] == 0:
            gbLog["Warnings"]["NZ1"] += 1
#            print "!!Near zero 1!!", inVert.index, lcAns
        return lcAns[0] >= 0 and lcAns[1] >= 0    
    
    if inEndState == "SomeEndVerts":
        # Set True to enable both face-end vertices because it can't be ignored
        lcEnables[ + 0], lcEnables[ - 1] = True, True
    elif inEndState == "NoEndVerts":
        # Set True to enable closest vertex because more than one enabled vertex is needed to start to check
        lcEnables[lcLengths[0][1]] = True
        del lcLengths[0]
    # Check angles between enabled adjacent vertices in order of closer vertex
    lcUnableRegions = []
    for tmpLength, i in lcLengths:
        enVert = inVertsAround[i]
        # Ignore vertex if it is in unable regions
        lcInUnableRegion = False
        for enRegion in lcUnableRegions:
            if CheckIfItIsInUnableRegion(enVert, enRegion):
                lcInUnableRegion = True
                break
        if lcInUnableRegion: continue
        
        # Get both adjacent vertices that has been enabled
        lcVertL, lcVertR = GetAdjacentEnabledVerts(i)
        # Measure angles and get smaller one
        lcAngleL = VertsAngle3(inCenterVert, enVert, lcVertL, inZAxis)
        lcAngleR = VertsAngle3(inCenterVert, enVert, lcVertR, inZAxis)
        lcSortArray = [[lcAngleL, lcVertL], [lcAngleR, lcVertR]]
        lcSortArray.sort()
        [lcMinAngle, lcNeigVert1], [tmpAngle, lcNeigVert2] = lcSortArray
        # Enable vertex if angle is large
        if lcMinAngle > gb["MinVertsAngle"]:
            lcEnables[i] = True
            continue
        
        # Make unable region that is defined using vectors and inverce matrix
        lcVec1 = lcNeigVert1.co - inCenterVert.co
        lcVec2 = enVert.co - lcNeigVert1.co
        try:
            lcInv = BMat([lcVec1 * lcVec1, lcVec1 * lcVec2], [lcVec1 * lcVec2, lcVec2 * lcVec2]).invert()
        except ValueError:
            gbLog["Warnings"]["NZ3"] += 1
#            print "!!Near parallel 3!!", lcVec1, lcVec2
            continue
        lcRegion = {"Vec0": lcNeigVert1.co, "Vec1": lcVec1, "Vec2": lcVec2, "Inv": lcInv, "Vert": enVert}
        # Enable vertex if its neighbor vertex is in unable region that has been made right now, when it is in SomeEndVerts state
        if inEndState == "SomeEndVerts" and CheckIfItIsInUnableRegion(lcNeigVert2, lcRegion):
            lcEnables[i] = True
            continue
        
        lcUnableRegions.append(lcRegion)
    
    # Check if the triangle outside has shaper angle than the triangle around center
    for tmpLength, i in lcLengths:
        if lcEnables[i]: continue
        enVert = inVertsAround[i]
        # Ignore vertex if it is in unable regions
        lcInUnableRegion = False
        lcRegionIndex = None
        for j, enRegion in enumerate(lcUnableRegions):
            # Don't check enVert because it is going to be an enable vertex
            if enVert == enRegion["Vert"]:
                lcRegionIndex = j
                continue
            if CheckIfItIsInUnableRegion(enVert, enRegion):
                lcInUnableRegion = True
                break
        if lcInUnableRegion: continue
        
        # Get both adjacent vertices that has been enabled
        lcVertL, lcVertR = GetAdjacentEnabledVerts(i)
        # Measure angles around center and get smaller one
        lcAngleL = VertsAngle3(inCenterVert, enVert, lcVertL, inZAxis)
        lcAngleR = VertsAngle3(inCenterVert, enVert, lcVertR, inZAxis)
        lcSortArray = [[lcAngleL, lcVertL], [lcAngleR, lcVertR]]
        lcSortArray.sort()
        [lcMinAngle, lcNeigVert1], [tmpAngle, lcNeigVert2] = lcSortArray
        # Measure angle around lcNeigVert2
        lcNeigAngle2 = VertsAngle3(lcNeigVert2, enVert, lcNeigVert1, inZAxis)
        
        # Enable vertex if the triangle outside has shaper angle than the triangle around center
        if lcNeigAngle2 < lcMinAngle:
            lcEnables[i] = True
            # Delete the region because enVert has become an enable vertex
            del lcUnableRegions[lcRegionIndex]
    
    # Pull out only enabled vertices
    outVertsAround = [inVertsAround[i] for i in xrange(n) if lcEnables[i]]
    # Add vertex if only one vertex has been gathered
    if inEndState == "NoEndVerts" and len(outVertsAround) < 2:
        outVertsAround.append(inVertsAround[lcLengths[1][1]])
    gbLog["TooSmallVertsAngles"] += len(inVertsAround) - len(outVertsAround)

    inData.VertsAround = outVertsAround
    return True

# Check if angles between adjacent 2 vertices are too large
def CheckIfAnglesAreTooLarge(inData):
    # Assume: VertsAround has been sorted around ZAxis.
    inCenterVert = inData.CenterVert
    inVertsAround = inData.VertsAround
    inZAxis = inData.ZAxis
    inEndState = inData.EndState
    inMakeFace = inData.MakeFace

    n = len(inVertsAround)
    for i in xrange(n - 1):
        # Measure angle between i and i+1 vertices
        lcAngle = VertsAngle2(inCenterVert, inVertsAround[i + 0], inVertsAround[i + 1], inZAxis)
        if 360 - lcAngle < 1e-5:
            gbLog["Warnings"]["NZ2"] += 1
#            print "!!Near zero 2!!", lcAngle
        if lcAngle >= gb["MaxVertsAngle"]:
            inMakeFace[i + 0] = False
            gbLog["TooLargeVertsAngles"] += 1
    if inEndState == "NoEndVerts":
        # Measure angle between first and end vertices
        lcAngle = VertsAngle2(inCenterVert, inVertsAround[ - 1], inVertsAround[ + 0], inZAxis)
        if lcAngle >= gb["MaxVertsAngle"]:
            inMakeFace[ - 1] = False
            gbLog["TooLargeVertsAngles"] += 1

    return True

# Make faces around simply
def MakeFacesAroundSimply(inData):
    inCenterVert = inData.CenterVert
    inVertsAround = inData.VertsAround
    inEndState = inData.EndState
    inMakeFace = inData.MakeFace
    
    # Make face-sets including sets of 3 vertex indices
    outFaces = []
    for i in xrange(len(inVertsAround) - 1):
        if not inMakeFace[i]: continue
        lcVert0 = inVertsAround[i + 0]
        lcVert1 = inVertsAround[i + 1]
        # Register set of 3 vertex indices of face to make
        outFaces.append([lcVert0.index, lcVert1.index, inCenterVert.index])

    # Connect first and last with face if EndVerts are not found
    if inEndState == "NoEndVerts" and inMakeFace[ - 1]:
        lcVert0 = inVertsAround[ - 1]
        lcVert1 = inVertsAround[ + 0]
        # Register set of 3 vertex indices of face to make
        outFaces.append([lcVert0.index, lcVert1.index, inCenterVert.index])

    inData.Faces = outFaces
    return True

# Combine all of faces that have been made in each group
def CombineFacesInAllVertGroups(inData):
    inEndState = inData.EndState
    inFaceGroups = inData.FaceGroups
    
    # Assign group straight if EndVerts are not found
    if inEndState == "NoEndVerts":
        inData.Faces = inFaceGroups[0]
        return True
    
    # Combine face-sets in each group
    outFaces = []
    for enFaceGroup in inFaceGroups:
        outFaces.extend(enFaceGroup)
#        outFaces.append(None)
    
    inData.Faces = outFaces
    return True

# Check if adjacent 2 triangles have good shapes
def CheckIfTrianglesHaveGoodShapes(inData):
    # Assume: Adjacent 2 faces have sequential indices in Faces array.
    # Assume: All items of Faces have the same form as [AroundVert1, AroundVert2, CenterVert].
    # Assume: AroundVert1, 2 must be sorted around ZAxis.
    inMesh = inData.Mesh
    inFaces = inData.Faces

    lcMaxMinAngles = []
    n = len(inFaces)
    for i in xrange(n):
        lcFace0, lcFace1 = inFaces[(i + 0) % n], inFaces[(i + 1) % n]
        # Add None and go to next if no faces are created in next side
        if lcFace0[1] != lcFace1[0]:
            lcMaxMinAngles.append(None)
            continue
        # Measure max internal angles in case of current and modified form
        lcMax1, tmpMin = TriangleMaxMinAngle([inMesh.verts[x] for x in lcFace0])
        lcMax2, tmpMin = TriangleMaxMinAngle([inMesh.verts[x] for x in lcFace1])
        lcCurrMax = max(lcMax1, lcMax2)
        lcMax1, tmpMin = TriangleMaxMinAngle([inMesh.verts[x] for x in [lcFace0[0], lcFace0[1], lcFace1[1]]])
        lcMax2, tmpMin = TriangleMaxMinAngle([inMesh.verts[x] for x in [lcFace0[0], lcFace1[1], lcFace0[2]]])
        lcModiMax = max(lcMax1, lcMax2)
        lcMaxMinAngles.append([lcCurrMax, lcModiMax])
    
    # Gather only angles of modified form and sort them by angles
    lcModiArray = []
    for i, enAngles in enumerate(lcMaxMinAngles):
        if enAngles == None: continue
        lcCurrMax, lcModiMax = enAngles
        if lcCurrMax > lcModiMax:
            lcModiArray.append([lcModiMax, i])
    lcModiArray.sort()
    
    # Change into modofied form if appropriate
    lcIsModified = [False] * n
    for tmpAngle, i in lcModiArray:
        if lcIsModified[i]: continue
        lcFace0, lcFace1 = inFaces[(i + 0) % n], inFaces[(i + 1) % n]
        # Measure angle between 2 triangles of modified form
        lcFacesAngle = FacesAngleAroundEdge(inMesh.verts[lcFace0[0]], inMesh.verts[lcFace1[1]], inMesh.verts[lcFace0[1]], inMesh.verts[lcFace0[2]])
        # Don't change if 2 triangles are reentrant
        if lcFacesAngle < 90: continue
        # Change into modofied form
        lcFace0, lcFace1 = lcFace0[:], lcFace1[:] # [:] is needed to copy array
        inFaces[(i + 0) % n] = [lcFace0[0], lcFace0[1], lcFace1[1]]
        inFaces[(i + 1) % n] = [lcFace0[0], lcFace1[1], lcFace0[2]]
        lcIsModified[(i - 1) % n], lcIsModified[(i + 0) % n], lcIsModified[(i + 1) % n] = True, True, True
        gbLog["ModifiedTriangles"] += 1

    return True

# Extend faces in faces manager
def RegisterFacesToFacesManager(inData):
    inFaces = inData.Faces
    inMana = inData.FacesManager
    
    # Get rid of all None from Faces
    tmpFaces = [enSet for enSet in inFaces if enSet != None]
    inMana.Extend(tmpFaces)
    gbLog["MadeFaces"] += len(tmpFaces)        
    
    return True


#******************************
#---===Basic functions 1===
#******************************

def sign(x):
    if x > 0: return 1
    if x < 0: return - 1
    return 0

def yorn(inBool, inTrue, inFalse):
    if inBool:
        return inTrue
    else:
        return inFalse
    
#******************************
#---===Basic functions 2===
#******************************

def SmallerAngle(inAngle):
    if inAngle > 180: # it can't calculate with "% 180"
        return 360 - inAngle
    else:
        return inAngle

def PointAngleOnXY(inPoint):
    if inPoint.length == 0: return 360
    return atan2(inPoint.y, inPoint.x) / pi * 180 % 360

def VertsAngle(inSharedVert, inVert1, inVert2):
    v1, v2 = inVert1.co - inSharedVert.co, inVert2.co - inSharedVert.co
    return BM.AngleBetweenVecs(v1, v2)

def VecsAngle2(inVec1, inVec2, inAxis):
    v1, v2 = inVec1, inVec2
    return BM.AngleBetweenVecs(v1, v2) * sign(BM.CrossVecs(v1, v2) * inAxis) % 360
    
def VertsAngle2(inSharedVert, inVert1, inVert2, inAxis):
    v1, v2 = inVert1.co - inSharedVert.co, inVert2.co - inSharedVert.co
    return VecsAngle2(v1, v2, inAxis)

def VertsAngle3(inSharedVert, inVert1, inVert2, inAxis):
    return SmallerAngle(VertsAngle2(inSharedVert, inVert1, inVert2, inAxis))
    
def TriangleMaxMinAngle(inVerts):
    lcAngles = [VertsAngle(inVerts[(i + 0) % 3], inVerts[(i - 1) % 3], inVerts[(i + 1) % 3]) for i in xrange(3)]
    return max(lcAngles), min(lcAngles)

def FacesAngleAroundEdge(inSharedVert1, inSharedVert2, inVert1, inVert2):
    lcZAxis = inSharedVert2.co - inSharedVert1.co
    lcXAxis = inVert1.co - inSharedVert1.co
    lcYAxis = BM.CrossVecs(lcZAxis, lcXAxis).normalize()
    lcXAxis = BM.CrossVecs(lcYAxis, lcZAxis).normalize()
    lcXYTransMat = BMat(lcXAxis, lcYAxis, [0, 0, 0])
    lcVert2 = lcXYTransMat * (inVert2.co - inSharedVert1.co)
    return SmallerAngle(PointAngleOnXY(lcVert2))


#******************************
#---===Normal Manager===
#******************************

class NormalManager:
    
    def __init__(self):
        self.Distance = None # In form of float
        self.Normals = None # In form of {MVert.index = BVec, ...}
    
    # Calculate average normal for the specified vertices collecting vertices in the specified distance
    def Calculate(self, inGridMana, inVerts, inDistance):
        inNormals = {}
        
        for enVert in inVerts:

            # Collect closer vertices around the center
            lcVerts = inGridMana.GetVertsInDistance(enVert.co, inDistance)
            if len(lcVerts) < 1:
                inNormals[enVert.index] = None
#                gbLog["NormMana.FewVertsCases"] += 1
                continue
            
            # Calculate z-axis to measure angles
            inNormals[enVert.index] = CalcAverageNormal(enVert, lcVerts)
        
        self.Distance = inDistance
        self.Normals = inNormals
    
    def __getitem__(self, inMVertIndex):
        return self.Normals[inMVertIndex]

# Solve a cubic equation based on Cardano Method
def SolveCubicEquation(a3210):
    
    def pow_ex(x, p):
        if x < 0:
            return - ((-x) ** p)
        else:
            return x ** p

    (a3, a2, a1, a0) = (float(x) for x in a3210)
    A2, A1, A0 = a2 / a3, a1 / a3, a0 / a3
    p, q = A1 - 1.0 / 3.0 * A2 ** 2, A0 - 1.0 / 3.0 * A1 * A2 + 2.0 / 27.0 * A2 ** 3
    D3 = (q / 2.0) ** 2 + (p / 3.0) ** 3
    
    if D3 <= 0:
        r = sqrt((q / 2.0) ** 2 + - D3)
        th = atan2(sqrt(-D3), - q / 2)
        y = [r ** (1.0 / 3.0) * 2.0 * cos(2.0 * pi / 3.0 * k + th / 3.0) for k in xrange(3)]
    else:
        B1, B2 = pow_ex(-q / 2.0 + sqrt(D3), 1.0 / 3.0), pow_ex(-q / 2.0 - sqrt(D3), 1.0 / 3.0)
        y = [B1 + B2, - (B1 + B2) / 2.0 + sqrt(3) * (B1 - B2) / 2.0 * 1j, - (B1 + B2) / 2.0 + sqrt(3) * (-B1 + B2) / 2.0 * 1j]
    ans = [x - A2 / 3.0 for x in y]
        
    return ans
# Test code
#def main():
#    ans = SolveCubicEquation([1, - 9, 26, - 24])
#    print "The result is %s, which should be [2.0, 3.0, 4.0]" % ans
#    ans = SolveCubicEquation([1, 2, 3, 4])
#    print "The result is %s, which should be [-1.6506291914393882, (-0.17468540428030588+1.5468688872313963j), (-0.17468540428030588-1.5468688872313963j)]" % ans

# Calculate average normal based on Lagrange's Lambda Method minimizing of sum(ax+by+cz)^2, in which ax+by+cz represents the distance between a vertex and the zero center
def CalcAverageNormal(inCenterVert, inVerts):
    
#    def b2py_float(x):
#        return round(x * 1e+6) * 1e-6
#    def b2py_vec(x):
#        for i in xrange(3): vec[i] = b2py_float(vec[i])
    NearZero = 1e-5
    
    # Summation vertex coordinates and obtain A matrix 
    Axx, Ayy, Azz, Axy, Ayz, Azx = (0,) * 6
    for enVert in inVerts:
        vec = enVert.co - inCenterVert.co
#        b2py_vec(vec)
        Axx += vec.x ** 2
        Ayy += vec.y ** 2
        Azz += vec.z ** 2
        Axy += vec.x * vec.y
        Ayz += vec.y * vec.z
        Azx += vec.z * vec.x
    
    # Solve det(A - lambda*I) = 0 for three patterns of lambda
    lambs = SolveCubicEquation([ - 1, Axx + Ayy + Azz, Axy ** 2 + Ayz ** 2 + Azx ** 2 - Axx * Ayy - Axx * Azz - Ayy * Azz, - Azz * Axy ** 2 + 2 * Axy * Ayz * Azx - Axx * Ayz ** 2 - Ayy * Azx ** 2 + Axx * Ayy * Azz])
    lamb = lambs[1] # Always the second lambda minimizes sum(ax+by+cz)^2, according to many experiments
    
    def EvalFunc(inNorm):
        a, b, c = inNorm
        return Axx * a ** 2 + Ayy * b ** 2 + Azz * c ** 2 + 2 * Axy * a * b + 2 * Ayz * b * c + 2 * Azx * c * a
    def FindProperNorm(inNorm1, inNorm2):
        e1 = EvalFunc(inNorm1)
        e2 = EvalFunc(inNorm2)
        if e1 < e2:
            return inNorm1
        else:
            return inNorm2

    # Calculate the ratio of a, b, c from lambda
    Axy_abs, Ayz_abs, Azx_abs = abs(Axy), abs(Ayz), abs(Azx)
    if Axy_abs < NearZero and Ayz_abs < NearZero and Azx_abs < NearZero: # when two of a, b, c are zero
        A_min = min([Axx, Ayy, Azz])
        if A_min == Axx:
            outNorm = [1.0, 0.0, 0.0]
        elif A_min == Ayy:
            outNorm = [0.0, 1.0, 0.0]
        else:
            outNorm = [0.0, 0.0, 1.0]
            
    elif Axy_abs < NearZero and Azx_abs < NearZero: # when a is zero
        lcNorm1 = [0.0, - Ayz, Ayy - lamb]
        lcNorm2 = [1.0, 0.0, 0.0]
        outNorm = FindProperNorm(lcNorm1, lcNorm2)
    elif Axy_abs < NearZero and Ayz_abs < NearZero: # when b is zero
        lcNorm1 = [ - Azx, 0.0, Axx - lamb]
        lcNorm2 = [0.0, 1.0, 0.0]
        outNorm = FindProperNorm(lcNorm1, lcNorm2)
    elif Ayz_abs < NearZero and Azx_abs < NearZero: # when c is zero
        lcNorm1 = [ - Axy, Axx - lamb, 0.0]
        lcNorm2 = [0.0, 0.0, 1.0]
        outNorm = FindProperNorm(lcNorm1, lcNorm2)
    
    else:
        a1 = Azx * (Ayy - lamb) - Ayz * Axy
        a2 = Axy * (Azz - lamb) - Ayz * Azx
        b1 = c2 = Ayz * (Axx - lamb) - Azx * Axy
        if abs(a1) > NearZero and abs(a2) > NearZero:
            outNorm = [a1 * a2, a2 * b1, a1 * c2]
        else:
            print "This case is uncertain, not implemented yet. (Err:200901111206)"
            outNorm = [0.0, 0.0, 1.0] # Incorrect values
    
    return BVec(outNorm).normalize()
# Test code
#def main():
#    lcMesh = B.Mesh.Get("Mesh1") # You need a mesh object which mesh name is Mesh1.
#    lcCenter = lcMesh.verts[0]
#    lcNorm = CalcAverageNormal(lcCenter, lcMesh.verts)
#    print "The result is %s." % lcNorm
#
#    # Draw the result normal with a line in Blender
#    lcNormMesh = B.Mesh.New("NormMesh1")
#    B.Scene.GetCurrent().objects.new(lcNormMesh, "NormMesh1")
#    lcNormMesh.verts.extend([lcCenter.co + lcNorm, lcCenter.co - lcNorm])
#    lcNormMesh.edges.extend([0, 1])

# Draw normals / Test function
def DrawNormalVector(inNormMana, inVerts=None, inVecLen=0.1):
    if inVerts == None:
        inVerts = inNormMana.Verts
    
    # Create mesh and object
    lcMesh = B.Mesh.New("NormMesh1")
    B.Scene.GetCurrent().objects.new(lcMesh, "NormMesh1")
    
    lcVerts = []
    lcEdges = []
    for enVert in inVerts:
        lcCenterVec = BVec(enVert.co)
        lcNormal = inNormMana[enVert.index]
        
        lcNormalVec1 = lcCenterVec + lcNormal * - inVecLen # setting for normal looks
        lcNormalVec2 = lcCenterVec + lcNormal * inVecLen # setting for normal looks
        lcVerts.extend([lcNormalVec1, lcNormalVec2])
        lcEdges.append([len(lcVerts) - 2, len(lcVerts) - 1])
    
    lcMesh.verts.extend(lcVerts)
    lcMesh.edges.extend(lcEdges)
    
# Code to test Normal Manager feature
#def Main():
#    lcPGM = PointsGridManager([0.5] * 3)
#    lcPGM.PositionGetter = GetPositionFromMVert
#    lcPGM.Add(B.Mesh.Get("Mesh1").verts)
#    lcNM = NormalManager()
#    lcNM.Calculate(lcPGM, B.Mesh.Get("Mesh1").verts, 1.0)
#    print "The normal of the vertex Mesh.verts[0] is: ", lcNM[0]
#    DrawNormalVector(lcNM, None, 0.5)


#******************************
#---===Faces Manager===
#******************************

class FacesManager:
    def __init__(self, inMesh):
        self.Mesh = inMesh
        self.Verts = [[] for i in xrange(len(inMesh.verts))] # This will waste huge memory if many vertices are given 
    
    def Import(self):
        lcFaces = []
        for enFace in self.Mesh.faces:
            lcFaces.append([enVert.index for enVert in enFace.verts])
        self.Extend(lcFaces)
    
    def Extend(self, inFaces):
        for enFace in inFaces:
            enFace = enFace[:] # copy of array to sort
            enFace.sort()
            for i in enFace:
                lcFaces = self.Verts[i]
                if enFace in lcFaces: continue
                lcFaces.append(enFace)
    
    def Delete(self, inFaces):
        for enFace in inFaces:
            enFace = enFace[:] # copy of array to sort
            enFace.sort()
            for i in enFace:
                lcFaces = self.Verts[i]
                lcFaces.remove(enFace) # Error will occer if specified face isn't found

    def __getitem__(self, inIndex):
        return self.Verts[inIndex]
    
    def Bake(self):
        # Transform Verts array into Blender format
        tmpFaces = []
        for i, enFaces in enumerate(self.Verts):
            for enFace in enFaces:
                # Add face to make
                tmpFaces.append(enFace)
                # Remove other same faces in Verts
                for j in enFace:
                    if i == j: continue
                    self.Verts[j].remove(enFace)
            self.Verts[i] = None
        del self.Verts
        # <Mesh> Make faces
        self.Mesh.faces.extend(tmpFaces)

# Code to test Faces Manager functionarity
#def Main():
#    lcFM = FacesManager(B.Mesh.Get("Mesh1"))
#    lcFM.Import()
#    print "Verts are: ", lcFM.Verts
#    lcFM.Extend([[0,1,2],[3,4,5]])
#    print "Verts are: ", lcFM.Verts
#    lcFM.Delete([[3,4,5]])
#    print "Verts are: ", lcFM.Verts
#    print "When [0] is used: ", lcFM[0]
#    lcFM.Bake()


#******************************
#---===Points Grid Manager===
#******************************

class PointsGridManager:
    
    def __init__(self, inXYZSize, inXYZOffset=[0.0] * 3):
        self.Size = inXYZSize # In form of [float, float, float]
        self.Offset = inXYZOffset # In form of [float, float, float]
        self.Grid = {} # In form of {"x,y,z": [MVert, ...], ...}
        self.PrecisionLevel = 2 # 0: Cube, 1: Cell sphere, 2: Total sphere
        self.PositionGetter = GetPositionFromArray # in form of function
        
    # Add or import vertices to manage by grid (array and MVert are available)
    def Add(self, inVerts):
        inGetter = self.PositionGetter
        
        # Put each vertex into the cell of grid
        outGrid = {}
        for enVert in inVerts:
            
            # Get key name from vertex position
            lcKeyIndex = self.GetKeyIndex(inGetter(enVert))
            lcKeyName = self.KeyIndexToName(lcKeyIndex)
            
            # Add vertex to the dictionary outGrid
            if lcKeyName in outGrid:
                outGrid[lcKeyName].append(enVert)
            else:
                outGrid[lcKeyName] = [enVert]
        
        self.Grid.update(outGrid)
    
    def Clear(self):
        self.Grid = {}
    
    # Get key name for the dictionary from specified position
    def GetKeyIndex(self, inPosition):
        # Assume: inPosition must be array, not MVert

        return [inPosition[i] - (inPosition[i] - self.Offset[i]) % self.Size[i] for i in xrange(3)]
    
    def KeyIndexToName(self, inKeyIndex):
        return hash((inKeyIndex[0], inKeyIndex[1], inKeyIndex[2]))
    
    # Get vertices that are located in the specified distance
    def GetVertsInDistance(self, inPosition, inDistance=0, inPrecisionLevel=None):
        # Assume: inPosition must be array, not MVert
        
        if inPrecisionLevel == None:
            inPrecisionLevel = self.PrecisionLevel
        inGetter = self.PositionGetter
        
        lcKeyIndex = self.GetKeyIndex(inPosition)
        # Calculate how many cells exist in the distance
        lcPluseCount = [int(floor((inPosition[i] + inDistance - lcKeyIndex[i]) / self.Size[i])) for i in xrange(3)]
        lcMinusCount = [int(floor((lcKeyIndex[i] - (inPosition[i] - inDistance)) / self.Size[i])) + 1 for i in xrange(3)]
        
        # Get key names that are located in cube
        lcKeyPoses = []
        for ix in xrange(-lcMinusCount[0], lcPluseCount[0] + 1):
            for iy in xrange(-lcMinusCount[1], lcPluseCount[1] + 1):
                for iz in xrange(-lcMinusCount[2], lcPluseCount[2] + 1):
                    tmpIndex = [ix, iy, iz]
                    lcKeyPoses.append([lcKeyIndex[i] + tmpIndex[i] * self.Size[i] for i in xrange(3)])
        
        # Get key names that are located in sphere
        if inPrecisionLevel == 1:
            lcCellRadius = sqrt(sum(self.Size[i] ** 2 for i in xrange(3)))
            lcNewKeyPoses = []
            for enKey in lcKeyPoses:
                if enKey == lcKeyIndex:
                    lcNewKeyPoses.append(enKey)
                    continue
                
                # Check if the next plus end of the cell enKey is closer to inPosition in each coordinate of xyz and set 1
                lcCellPos = [enKey[i] + 0.5 * self.Size[i] for i in xrange(3)]
                lcDistance = sqrt(sum((lcCellPos[i] - inPosition[i]) ** 2 for i in xrange(3)))
                if lcDistance - lcCellRadius < inDistance:
                    lcNewKeyPoses.append(enKey)
            lcKeyPoses = lcNewKeyPoses
            
        # Get vertices from key names
        outVerts = []
        for enKey in lcKeyPoses:
            lcKeyName = self.KeyIndexToName(enKey) # Time consumption!
            # Discard vertices that have the same position as inPosition
            if enKey == lcKeyIndex:
                if lcKeyName in self.Grid:
                    lcVerts = self.Grid[lcKeyName][:] # [:] is needed to copy array
                    for i, enVert in enumerate(lcVerts):
                        enPosition = inGetter(enVert)
                        lcDist2 = sum((enPosition[i] - inPosition[i]) ** 2 for i in xrange(3))
                        if lcDist2 == 0:
                            del lcVerts[i]
                    outVerts.extend(lcVerts)
                continue
            
            # Gather vertices that cell has
            if lcKeyName in self.Grid:
                outVerts.extend(self.Grid[lcKeyName])
        
        # Get vertices that are located in the real distance
        if inPrecisionLevel == 2:
            lcNewVerts = []
            for enVert in outVerts:
                enPosition = inGetter(enVert)
                lcDistance = sqrt(sum((enPosition[i] - inPosition[i]) ** 2 for i in xrange(3)))
                if lcDistance < inDistance:
                    lcNewVerts.append(enVert)
            outVerts = lcNewVerts
        
        return outVerts
    
    # Check if the cell size is appropriate
    def Analyze(self, inDistance=0):
        for enVerts in self.Grid:
            pass

def GetPositionFromArray(inVert):
    return inVert
def GetPositionFromMVert(inVert):
    return inVert.co

# Code to test Points Grid Manager feature
#def Main():
#    lcPGM = PointsGridManager([0.5] * 3)
#    lcPGM.PositionGetter = GetPositionFromMVert
#    lcPGM.Add(B.Mesh.Get("Mesh1").verts)
#    print "The number of Grid cells: ", len(lcPGM.Grid)
#    lcPGM.PrecisionLevel = 2
#    lcVerts = lcPGM.GetVertsInDistance([1.0, 0.0, 0.0], 1.0)
#    for enVert in lcVerts: enVert.sel = 1
#    print "The number of gathered vertices: ", len(lcVerts)



#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
#---Module of BlenderGUIProvider v2.py
#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# Change logs:
#  2008/11/09 Blender GUI Provider v2
#   +Blender Controls Provider was added to make it easier to create
#    your GUI. You can make the GUI in an easy and well-known way that
#    is similar when you write a UI code in Java or .NET.
#  2008/11/06 Blender GUI Provider v1
#   +Blender GUI Provider is the most basic class that allows you to
#    create your GUI easily for Blender. It provides you with several 
#    basic events needed for your GUI and the control of starting and 
#    ending the GUI with the functions Start and Exit.
#                                                                   END


#******************************
#---===Import declarations===
#******************************

import Blender as B


#******************************
#---===Blender GUI Provider===
#******************************

class BGUIProvider:

    def __init__(self):
        global gbBGUIProviderData
        gbBGUIProviderData = {}
        self.Data = gbBGUIProviderData
        self.IsFirst = True
        
        self.EventHandler_OnLoad = _EventHandlerManager()
        self.EventHandler_OnUnload = _EventHandlerManager()
        self.EventHandler_OnDrawFirst = _EventHandlerManager()
        self.EventHandler_OnRedraw = _EventHandlerManager()
        self.EventHandler_OnClick = _EventHandlerManager()
        self.EventHandler_OnClick_Dict = _DictEventHandlerManager()
        self.EventHandler_OnKeyMouse = _EventHandlerManager()
        self.EventHandler_OnKeyMouse_Dict = _DictEventHandlerManager()

    def Start(self):
        self.EventHandler_OnLoad.Raise()
            
        B.Draw.Register(self.__HandleGUIEvent, self.__HandleKeyMouseEvent, self.__HandleButtonEvent)
        
    def Redraw(self):
        B.Draw.Redraw(1)
        
    def Exit(self):
        lcReturn = self.EventHandler_OnUnload.Raise()
        if lcReturn == False:
            return

        B.Draw.Exit()
    
    def __HandleGUIEvent(self):
        if self.IsFirst:
            self.EventHandler_OnDrawFirst.Raise(self.Data)
            self.IsFirst = False
        self.EventHandler_OnRedraw.Raise(self.Data)
        
    def __HandleButtonEvent(self, evt):
        self.EventHandler_OnClick.Raise(evt)
        self.EventHandler_OnClick_Dict.Raise(evt, evt)
    
    def __HandleKeyMouseEvent(self, evt, val):
        self.EventHandler_OnKeyMouse.Raise(evt, val)
        self.EventHandler_OnKeyMouse_Dict.Raise(evt, evt, val)

class _EventHandlerManager:
    
    def __init__(self):
        self.Handlers = []
    
    # Add your function of event handler
    def Add(self, inHandler):
        self.Handlers.append(inHandler)
        
    # Remove your function of event handler
    def Remove(self, inHandler):
        self.Handlers.remove(inHandler)
    
    # Raise event by calling all added functions
    def Raise(self, *inArguments):
        lcResultSum = True
        for enHandler in self.Handlers:
            lcResult = enHandler(*inArguments)
            if lcResult == None:
                continue
            lcResultSum = lcResultSum and lcResult
        return lcResultSum
    
class _DictEventHandlerManager:

    def __init__(self):
        self.Handlers = {}
    
    def __getitem__(self, inName):
        return self.Handlers[inName]
    
    # Add your function of event handler
    def Add(self, inName, inHandler):
        if not inName in self.Handlers:
            self.Handlers[inName] = _EventHandlerManager()
        self.Handlers[inName].Add(inHandler)
            
    # Remove your function of event handler
    def Remove(self, inName, inHandler):
        self.Handlers[inName].Remove(inHandler)
        if not self.Handlers[inName]:
            del self.Handlers[inName]
    
    # Raise event by calling all added functions
    def Raise(self, inName, *inArguments):
        lcResult = True
        if inName in self.Handlers:
            lcResult = self.Handlers[inName].Raise(*inArguments)
        return lcResult

# Code to test Blender GUI Provider feature
#def Main():
#    def OnDrawFirst(d):
#        d[1001] = B.Draw.Create(1)
#    def OnRedraw(d):
#        d[1001] = B.Draw.Toggle("Toggle", 1001, 10, 40, 100, 20, d[1001].val, "A toggle button")
#        B.Draw.PushButton("Exit", 1002, 10, 10, 100, 20, "Push to exit")
#    def OnClick(evt):
#        lcProv.Exit()
#    def OnUnload():
#        return B.Draw.PupMenu("Really exit?%t|Yes|No") == 1
#    lcProv = BGUIProvider()
#    lcProv.EventHandler_OnDrawFirst.Add(OnDrawFirst)
#    lcProv.EventHandler_OnRedraw.Add(OnRedraw)
#    lcProv.EventHandler_OnClick_Dict.Add(1002, OnClick)
#    lcProv.EventHandler_OnUnload.Add(OnUnload)
#    lcProv.Start()


#******************************
#---===Blender Controls Provider===
#******************************

class BControlProvider:

    def __init__(self, inBControl=None):
        lcProv = BGUIProvider()
        self.BGUIProvider = lcProv
        self.EventHandler_OnLoad = lcProv.EventHandler_OnLoad
        self.EventHandler_OnUnload = lcProv.EventHandler_OnUnload
        self.EventHandler_OnDrawFirst = lcProv.EventHandler_OnDrawFirst
        self.EventHandler_OnRedraw = lcProv.EventHandler_OnRedraw
        self.EventHandler_OnRedraw.Add(self.__HandleRedrawEvent)
        self.EventHandler_OnClick = lcProv.EventHandler_OnClick
        self.EventHandler_OnClick_Dict = lcProv.EventHandler_OnClick_Dict
        self.EventHandler_OnKeyMouse = lcProv.EventHandler_OnKeyMouse
        self.EventHandler_OnKeyMouse_Dict = lcProv.EventHandler_OnKeyMouse_Dict
        
        if inBControl == None:
            self.BControl = BControlLabel(Text="There are no BControls that have been added as the root.")
        else:
            self.BControl = inBControl

    def Start(self):
        self.BGUIProvider.Start()
        
    def __HandleRedrawEvent(self, d):
        lcSize = B.Window.GetAreaSize()
        lcPos = [0, lcSize[1] - 2] # -2 for correct location of the top
        self.BControl._Preprocess()
        self.BControl._Draw(lcPos)
    
    # Search for the BControl that has the specified name
    def Search(self, inName):  
        return self.__Search(inName, self.BControl)
        
    def __Search(self, inName, inBCon): # When inCache is true, it saves a cache and the next time it can search faster  
        try:
            inBCon.BControls
            lcContainer = True
        except AttributeError:
            lcContainer = False
        
        if lcContainer:
            for enBCon in inBCon.BControls:
                lcBCon = self.__Search(inName, enBCon)
                if lcBCon != None:
                    return lcBCon
        else:
            if inBCon.Name == inName:
                return inBCon
        return None
    
    # Collect all the BControls that has a name
    def GetAllNames(self):
        lcNames = {}
        self.__GetAllNames(self.BControl, lcNames)
        return lcNames
        
    def __GetAllNames(self, inBCon, inNames):
        try:
            inBCon.BControls
            lcContainer = True
        except AttributeError:
            lcContainer = False
        
        if lcContainer:
            for enBCon in inBCon.BControls:
                self.__GetAllNames(enBCon, inNames)
        else:
            if inBCon.Name != None:
                inNames[inBCon.Name] = inBCon
    
class BControlHFlowLayout:
    
    def __init__(self, Name=None, Margin=[0] * 4, HAlign=None, VAlign=None,
                  InnerVAlign=None, CellPadding=0, CellSpacing=0, Backcolor=None):
        
        # Common properties
        self.Name = Name
        self.Pos = None # [x, y], calculated automatically
        self.Size = None # [w, h] without margin, calculated automatically
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom

        # Specific properties
        self.BControls = []
        self.InnerVAlign = InnerVAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.CellPadding = CellPadding
        self.CellSpacing = CellSpacing
        self.Backcolor = Backcolor # N: transparent, or [r, g, b], rgb is 0 to 1 

    def _Preprocess(self):
        
        # Calculate child NetSize in advance
        for enBCon in self.BControls:
            enBCon._Preprocess()

        # Calculate this Size
        lcInH = 0
        for enBCon in self.BControls:
            enInH = enBCon.NetSize[1]
            if enInH > lcInH:
                lcInH = enInH
        lcInW = 0
        for enBCon in self.BControls:
            lcInW += enBCon.NetSize[0] + self.CellSpacing + self.CellPadding * 2
        self.Size = [lcInW + self.CellSpacing,
                     lcInH + self.CellSpacing * 2 + self.CellPadding * 2]
                
        # Calculate this NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]

    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control

        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos

        if self.Backcolor != None:
            B.BGL.glColor3f(*self.Backcolor)
            B.BGL.glRectf(int(lcPos[0]), int(lcPos[1]), int(lcPos[0] + self.Size[0]), int(lcPos[1] - self.Size[1]))
        
        # Give child controls the position where they should draw
        lcPos = [inPos[0] + self.Margin[3] + self.CellSpacing + self.CellPadding,
                 inPos[1] - self.Margin[2] - self.CellSpacing - self.CellPadding]
        for enBCon in self.BControls:
            lcDiff = self.Size[1] - enBCon.NetSize[1] - self.CellSpacing * 2 - self.CellPadding * 2
            if enBCon.VAlign != None:
                lcInHAdd = lcDiff * enBCon.VAlign
            elif self.InnerVAlign != None:
                lcInHAdd = lcDiff * self.InnerVAlign
            else:
                lcInHAdd = lcDiff * 0
            enPos = [lcPos[0], lcPos[1] - lcInHAdd]
            enBCon._Draw(enPos)
            
            lcPos[0] += enBCon.NetSize[0] + self.CellSpacing + self.CellPadding * 2
        
    def __getitem__(self, i):
        return self.BControls[i]
    def __iter__(self):
        return self.BControls
    def Append(self, inBControl):
        self.BControls.append(inBControl)
    def Insert(self, inIndex, inBControl):
        self.BControls.insert(inIndex, inBControl)
    def Clear(self):
        self.BControls = []
    def Delete(self, inIndex):
        del self.BControls[inIndex]
    def Remove(self, inBControl):
        self.BControls.remove(inBControl)
        
class BControlVFlowLayout:

    def __init__(self, Name=None, Margin=[0] * 4, HAlign=None, VAlign=None,
                  InnerHAlign=None, CellPadding=0, CellSpacing=0, Backcolor=None):
        
        # Common properties
        self.Name = Name
        self.Pos = None # [x, y], calculated automatically
        self.Size = None # [w, h] without margin, calculated automatically
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        
        # Specific properties
        self.BControls = []
        self.InnerHAlign = InnerHAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.CellPadding = CellPadding
        self.CellSpacing = CellSpacing
        self.Backcolor = Backcolor # N: transparent, or [r, g, b], rgb is 0 to 1 

    def _Preprocess(self):
        
        # Calculate child NetSize in advance
        for enBCon in self.BControls:
            enBCon._Preprocess()

        # Calculate this Size
        lcInW = 0
        for enBCon in self.BControls:
            enInW = enBCon.NetSize[0]
            if enInW > lcInW:
                lcInW = enInW
        lcInH = 0
        for enBCon in self.BControls:
            lcInH += enBCon.NetSize[1] + self.CellSpacing + self.CellPadding * 2
        self.Size = [lcInW + self.CellSpacing * 2 + self.CellPadding * 2,
                     lcInH + self.CellSpacing]
                
        # Calculate this NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]

    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control

        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos

        if self.Backcolor != None:
            B.BGL.glColor3f(*self.Backcolor)
            B.BGL.glRectf(int(lcPos[0]), int(lcPos[1]), int(lcPos[0] + self.Size[0]), int(lcPos[1] - self.Size[1]))
        
        # Give child controls the position where they should draw
        lcPos = [inPos[0] + self.Margin[3] + self.CellSpacing + self.CellPadding,
                 inPos[1] - self.Margin[2] - self.CellSpacing - self.CellPadding]
        for enBCon in self.BControls:
            lcDiff = self.Size[0] - enBCon.NetSize[0] - self.CellSpacing * 2 - self.CellPadding * 2
            if enBCon.HAlign != None:
                lcInWAdd = lcDiff * enBCon.HAlign
            elif self.InnerHAlign != None:
                lcInWAdd = lcDiff * self.InnerHAlign
            else:
                lcInWAdd = lcDiff * 0
            enPos = [lcPos[0] + lcInWAdd, lcPos[1]]
            enBCon._Draw(enPos)
            
            lcPos[1] -= enBCon.NetSize[1] + self.CellSpacing + self.CellPadding * 2
        
    def __getitem__(self, i):
        return self.BControls[i]
    def __iter__(self):
        return self.BControls
    def Append(self, inBControl):
        self.BControls.append(inBControl)
    def Insert(self, inIndex, inBControl):
        self.BControls.insert(inIndex, inBControl)
    def Clear(self):
        self.BControls = []
    def Delete(self, inIndex):
        del self.BControls[inIndex]
    def Remove(self, inBControl):
        self.BControls.remove(inBControl)

class BControlLabel:

    def __init__(self, Name=None, Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="Text", FontSize="normal", Color=[0.0] * 3, Backcolor=None, AutoSize=True, Width=200):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = None # [w, h] without margin, calculated automatically
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        
        # Specific properties
        self.Text = Text
        self.FontSize = FontSize
        self.Color = Color
        self.Backcolor = Backcolor # N: transparent, or [r, g, b], rgb is 0 to 1
        self.AutoSize = AutoSize # T or F
        self.Width = Width
        
    def _Preprocess(self):
        
        # Calculate Size
        if self.AutoSize:
            lcW = B.Draw.GetStringWidth(self.Text, self.FontSize)
            lcH = self.GetStringHeight(self.FontSize)
            self.Size = [lcW, lcH]
        else:
            lcH = self.GetStringHeight(self.FontSize)
            self.Size = [self.Width, lcH]
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        if self.Backcolor != None:
            B.BGL.glColor3f(*self.Backcolor)
            B.BGL.glRectf(int(lcPos[0]), int(lcPos[1]), int(lcPos[0] + self.Size[0]), int(lcPos[1] - self.Size[1]))
            
        B.BGL.glColor3f(*self.Color)
        B.BGL.glRasterPos2i(int(lcPos[0]), int(lcPos[1] - self.Size[1]))
        B.Draw.Text(self.Text, self.FontSize)
        
    def GetStringHeight(self, inFontSize):
        return {"large": 10, "normal": 9, "small": 8, "tiny": 6}[inFontSize]

class BControlString:
    
    def __init__(self, Name=None, Size=[100, 20], Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="String", InitValue="", Length=399, ToolTip="String ToolTip"):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = Size # [w, h] without margin
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.EventHandler_OnCallBack = _EventHandlerManager()
        self.EventHandler_OnCallBack_Dict = _DictEventHandlerManager()
        
        # Specific properties
        self.Text = Text
        self.Button = B.Draw.Create(InitValue)
        self.Length = Length
        self.ToolTip = ToolTip
        
    def _Preprocess(self):
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        self.Button = B.Draw.String(self.Text, self.Id, int(lcPos[0]), int(lcPos[1] - self.Size[1]), int(self.Size[0]), int(self.Size[1]), self.Button.val, self.Length, self.ToolTip, self.__CallBack)
        
    def __CallBack(self, evt, val):
        self.EventHandler_OnCallBack.Raise(evt, val)
        self.EventHandler_OnCallBack_Dict.Raise(evt, evt, val)

class BControlNumber:
    
    def __init__(self, Name=None, Size=[100, 20], Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="Number", InitValue=0.0, Min=0.0, Max=1.0, ToolTip="Number ToolTip"):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = Size # [w, h] without margin
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.EventHandler_OnCallBack = _EventHandlerManager()
        self.EventHandler_OnCallBack_Dict = _DictEventHandlerManager()
        
        # Specific properties
        self.Text = Text
        self.Button = B.Draw.Create(InitValue)
        self.Min = Min
        self.Max = Max
        self.ToolTip = ToolTip
        
    def _Preprocess(self):
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        self.Button = B.Draw.Number(self.Text, self.Id, int(lcPos[0]), int(lcPos[1] - self.Size[1]), int(self.Size[0]), int(self.Size[1]), self.Button.val, self.Min, self.Max, self.ToolTip, self.__CallBack)
        
    def __CallBack(self, evt, val):
        self.EventHandler_OnCallBack.Raise(evt, val)
        self.EventHandler_OnCallBack_Dict.Raise(evt, evt, val)

class BControlSlider:
    
    def __init__(self, Name=None, Size=[100, 20], Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="Slider", InitValue=0.0, Min=0.0, Max=1.0, ToolTip="Slider ToolTip"):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = Size # [w, h] without margin
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.EventHandler_OnCallBack = _EventHandlerManager()
        self.EventHandler_OnCallBack_Dict = _DictEventHandlerManager()
        
        # Specific properties
        self.Text = Text
        self.Button = B.Draw.Create(InitValue)
        self.Min = Min
        self.Max = Max
        self.ToolTip = ToolTip
        
    def _Preprocess(self):
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        self.Button = B.Draw.Slider(self.Text, self.Id, int(lcPos[0]), int(lcPos[1] - self.Size[1]), int(self.Size[0]), int(self.Size[1]), self.Button.val, self.Min, self.Max, 0, self.ToolTip, self.__CallBack)
        
    def __CallBack(self, evt, val):
        self.EventHandler_OnCallBack.Raise(evt, val)
        self.EventHandler_OnCallBack_Dict.Raise(evt, evt, val)

class BControlToggle:
    
    def __init__(self, Name=None, Size=[100, 20], Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="Toggle", InitValue=0, ToolTip="Toggle ToolTip"):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = Size # [w, h] without margin
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.EventHandler_OnCallBack = _EventHandlerManager()
        self.EventHandler_OnCallBack_Dict = _DictEventHandlerManager()
        
        # Specific properties
        self.Text = Text
        self.Button = B.Draw.Create(InitValue)
        self.ToolTip = ToolTip
        
    def _Preprocess(self):
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        self.Button = B.Draw.Toggle(self.Text, self.Id, int(lcPos[0]), int(lcPos[1] - self.Size[1]), int(self.Size[0]), int(self.Size[1]), self.Button.val, self.ToolTip, self.__CallBack)
        
    def __CallBack(self, evt, val):
        self.EventHandler_OnCallBack.Raise(evt, val)
        self.EventHandler_OnCallBack_Dict.Raise(evt, evt, val)

class BControlButton:
    
    def __init__(self, Name=None, Size=[100, 20], Margin=[0] * 4, HAlign=None, VAlign=None,
                  Text="Button", ToolTip="Button ToolTip"):
        
        # Common properties
        self.Id = CreateNewBControlID() # int, calculated automatically
        self.Name = Name
        self.Pos = None # [x, y] without margin, calculated automatically
        self.Size = Size # [w, h] without margin
        self.NetSize = None # [w, h] including margin, calculated automatically
        self.Margin = Margin # [top, right, bottom, left]
        self.HAlign = HAlign # N: Default, 0: Left, 0.5: Center, 1: Right
        self.VAlign = VAlign # N: Default, 0: Top, 0.5: Center, 1: Bottom
        self.EventHandler_OnCallBack = _EventHandlerManager()
        self.EventHandler_OnCallBack_Dict = _DictEventHandlerManager()
        
        # Specific properties
        self.Text = Text
        self.ToolTip = ToolTip
        
    def _Preprocess(self):
        
        # Calculate NetSize
        self.NetSize = [self.Margin[3] + self.Size[0] + self.Margin[1],
                        self.Margin[0] + self.Size[1] + self.Margin[2]]
        
    def _Draw(self, inPos):
        # Assume: inPos is top-left corner including margin for this control
        
        lcPos = [inPos[0] + self.Margin[3],
                 inPos[1] - self.Margin[0]]
        self.Pos = lcPos
        
        B.Draw.PushButton(self.Text, self.Id, int(lcPos[0]), int(lcPos[1] - self.Size[1]), int(self.Size[0]), int(self.Size[1]), self.ToolTip, self.__CallBack)
        
    def __CallBack(self, evt, val):
        self.EventHandler_OnCallBack.Raise(evt, val)
        self.EventHandler_OnCallBack_Dict.Raise(evt, evt, val)
        
def CreateNewBControlID():
    global gbBControl
    try:
        gbBControl += 1
    except NameError:
        gbBControl = 0
    return gbBControl

# Code to test Blender Controls Provider feature
#def Main():
#    lcProv = BControlProvider()
#    lcProv.Start()
#def Main():
#    lcProv = BControlProvider(BControlButton())
#    lcProv.Start()
#def Main():
#    lcHFlo = BControlHFlowLayout(CellSpacing=5, Backcolor=[0.8]*3)
#    lcHFlo.Append(BControlToggle())
#    lcHFlo.Append(BControlNumber())
#    lcVFlo = BControlVFlowLayout(CellSpacing=10, Backcolor=[0.5]*3)
#    lcVFlo.Append(lcHFlo)
#    lcHFlo = BControlHFlowLayout(CellSpacing=5, Backcolor=[0.8]*3)
#    lcHFlo.Append(BControlLabel(VAlign=0.5))
#    lcHFlo.Append(BControlButton())
#    lcVFlo.Append(lcHFlo)
#    lcProv = BControlProvider(lcVFlo)
#    lcProv.Start()
#def Main():
#    lcButt = BControlButton()
#    lcProv = BControlProvider(lcButt)
#    def OnClick(evt, val):
#        lcProv.BGUIProvider.Exit()
#    def OnUnload():
#        return B.Draw.PupMenu("Really exit?%t|Yes|No") == 1
#    lcButt.EventHandler_OnCallBack.Add(OnClick)
#    lcProv.EventHandler_OnUnload.Add(OnUnload)
#    lcProv.Start()



#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
#---Module of TimeProfile v1.py
#MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# Change logs:
#  2008/11/03 Time Profiler v1
#   +Time Profiler allows you to collect the profiles of the execution, such as
#    taken time and how many times it was called.
#   +It can display the result in the three different ways.
#                                                                   END


#******************************
#---===Import declarations===
#******************************

import time
import re


#******************************
#---===Time Profiler===
#******************************

class TimeProfiler:
    
    def __init__(self, inEnable=True):
        self.Profiles = {} # in form of {string Name: [float TakenTime, int CalledCount], ...}
        self.PrevData = None # in form of [string Name, float StartTime, int IncrementAmount]
        self.StartTime = time.clock()
        
        self.Enable = inEnable # in form of bool IsEnable
        self.RegEx = ".*" # a regular expression string that limits displayed items searching the name
        self.Delimiter = "." # a name delimiter that makes profile groups
        self.ShowMode = 1 # 0: display groups in the same columns, 1: display groups in another columns, 2: display groups separately
        
        if not inEnable:
            # Force to ignore the function calls
            self.Start = lambda inName: None
            self.End = lambda : None
    
    def Start(self, inName, inNotCount=False):
        inPrev = self.PrevData
        
        if inPrev != None:
            self.End()
        
        if inNotCount:
            lcIncre = 0
        else:
            lcIncre = 1
            
        self.PrevData = [inName, time.clock(), lcIncre]
    
    def End(self):
        inName, inTime, inIncre = self.PrevData
        
        inTime = time.clock() - inTime
        
        # Add taken time and increment count
        if inName in self.Profiles:
            self.Profiles[inName][0] += inTime
            self.Profiles[inName][1] += inIncre
        else:
            self.Profiles[inName] = [inTime, inIncre]

        self.PrevData = None
    
    def Print(self, inOrder=0, inReverse=False): # Order is 0: Name order, 1: Time order
        outResult = "Time Profile:\n"

        outResult += self.__PrintDetails(inOrder, inReverse)
        
        outResult += "---------------------------------------\n"
        outResult += "%0.3f [s]\n" % (time.clock() - self.StartTime)
        
        return outResult
    
    def __PrintDetails(self, inOrder=0, inReverse=False):
        inProfiles = self.Profiles
        inRegEx = self.RegEx
        inDelimiter = self.Delimiter
        inShowMode = self.ShowMode
        outResult = ""

        if len(inProfiles) == 0:
            return outResult
        
        if self.PrevData != None:
            lcName = self.PrevData[0]
            self.Start(lcName, True) # Not count calls
        
        # Add parent items that are not in inProfiles yet
        lcAddiProfs = {}
        for enName in inProfiles.iterkeys():
            lcElems = enName.split(inDelimiter)
            lcName = lcElems[0]
            for enElem in lcElems[1:]:
                if not lcName in inProfiles:
                    lcAddiProfs[lcName] = [0.0, 0]
                lcName += inDelimiter + enElem
        inProfiles.update(lcAddiProfs)
        
        # Add up time to parent items
        lcParents = {} # in form of {string Name: [float SumTime, int SumCount, int ChildNum], ...}
        for enName, (enTime, enCount) in inProfiles.iteritems():
            lcElems = enName.split(inDelimiter)
            lcName = lcElems[0]
            for enElem in lcElems[1:]:
                if not lcName in lcParents:
                    lcParents[lcName] = [inProfiles[lcName][0], inProfiles[lcName][1], 1]
                lcParents[lcName][0] += enTime
                lcParents[lcName][1] += enCount
                lcParents[lcName][2] += 1
                lcName += inDelimiter + enElem
        
        # Process ordering and regular expression limiting
        lcRe = re.compile(inRegEx)
        lcProfiles = [[enName, enTime, enCount] for enName, (enTime, enCount) in inProfiles.iteritems()
            if lcRe.search(enName) != None]
        def cmp1(x, y):
            if x[inOrder] > y[inOrder]:
                return 1
            else:
                return - 1
        def cmp2(x, y):
            if x[inOrder] < y[inOrder]:
                return 1
            else:
                return - 1
        if inOrder in [0]:
            lcProfiles.sort(cmp1, None, inReverse)
        else:
            lcProfiles.sort(cmp2, None, inReverse)
        
        # Create result string
        if inShowMode == 0:
            outResult += "--No.---Seconds--Calls---Name of \"%s\"\n" % (inRegEx)
            lcTime = 0
            lcCount = 0
            for i, (enName, enTime, enCount) in enumerate(lcProfiles):
                if enName in lcParents:
                    enParentTime = lcParents[enName][0]
                    enParentCount = lcParents[enName][1]
                    enParentName = "%s(%s)" % (enName, lcParents[enName][2])
                    outResult += "  Sum %9.3f %6d %s %s\n" % (enParentTime, enParentCount, "+", enParentName)
                    outResult += "%4d. %9.3f %6d %s %s\n" % (i + 1, enTime, enCount, "-", enName)
                else:
                    outResult += "%4d. %9.3f %6d %s %s\n" % (i + 1, enTime, enCount, "-", enName)
                lcTime += enTime
                lcCount += enCount
            outResult += "---------------------------------------\n"
            outResult += "  Sum %9.3f %6d - Total\n" % (lcTime, lcCount)
        elif inShowMode == 1:
            outResult += "--No.---Seconds-------Sum--Calls----Sum---Name of \"%s\"\n" % (inRegEx)
            lcTime = 0
            lcCount = 0
            for i, (enName, enTime, enCount) in enumerate(lcProfiles):
                if enName in lcParents:
                    enParentTime = lcParents[enName][0]
                    enParentCount = lcParents[enName][1]
                    enParentName = "%s(%s)" % (enName, lcParents[enName][2])
                    outResult += "%4d. %9.3f %9.3f %6d %6d %s %s\n" % (i + 1, enTime, enParentTime, enCount, enParentCount, "+", enParentName)
                else:
                    outResult += "%4d. %9.3f           %6d        %s %s\n" % (i + 1, enTime, enCount, "-", enName)
                lcTime += enTime
                lcCount += enCount
            outResult += "---------------------------------------\n"
            outResult += "  Sum %9.3f           %6d        - Total\n" % (lcTime, lcCount)
        elif inShowMode == 2:
            outResult += "--No.---Seconds--Calls---Name of \"%s\"\n" % (inRegEx)
            lcTime = 0
            lcCount = 0
            for i, (enName, enTime, enCount) in enumerate(lcProfiles):
                outResult += "%4d. %9.3f %6d %s %s\n" % (i + 1, enTime, enCount, "-", enName)
                lcTime += enTime
                lcCount += enCount
            outResult += "---------------------------------------\n"
            for i, (enName, enTime, enCount) in enumerate(lcProfiles):
                if not enName in lcParents:
                    continue
                enSumTime, enSumCount, enChildNum = lcParents[enName]
                enParentName = "%s(%s)" % (enName, enChildNum)
                outResult += "  Sum %9.3f %6d %s %s\n" % (enSumTime, enSumCount, "+", enParentName)
            outResult += "---------------------------------------\n"
            outResult += "  Sum %9.3f %6d - Total\n" % (lcTime, lcCount)
        
        return outResult

# Code to test Time Profiler feature
#def Main():
#    lcTP = TimeProfiler()
#    for i in xrange(10):
#        lcTP.Start("A")
#        time.sleep(0.03)
#        lcTP.Start("A.A")
#        time.sleep(0.1)
#        lcTP.Start("A.A.A")
#        time.sleep(0.05)
#        lcTP.Start("B.B")
#        time.sleep(0.01)
#    print lcTP.Print()
#    print lcTP.Print(1)
#    lcTP.RegEx = "^A" # Name starts with "A"
#    print lcTP.Print()
#    
#    lcTP = TimeProfiler(False)
#    lcTP.Start("C")
#    time.sleep(0.1)
#    print lcTP.Print()



#******************************
#---===Start point===
#******************************

def Main_inScript():
    
    # Functions that handles the corresponding button events
    
    def Exit(evt, val):
        lcProv.BGUIProvider.Exit()
        
    def Skin(evt, val):
        global gbTP
        
        gb["TargetObject"] = lcTargetObject.Button.val
        gb["MaxAroundDist"] = lcMaxAroundDist.Button.val
        gb["MaxDistForAxis"] = lcMaxDistForAxis.Button.val * gb["MaxAroundDist"]
        gb["GridSize"] = [lcGridSize.Button.val * gb["MaxAroundDist"]] * 3
        gb["IgnoreErrors"] = True
        
        lcEnable = lcUseTimeProfile.Button.val == 1
        gbTP = TimeProfiler(lcEnable)
        gbTP.ShowMode = 2
        print "-----Start-----"
        SkinVerts() # main function of skinning
        print "-----gbLog-----"
        print gbLog
        print gbTP.Print()
        
    def Debug_DrawNormal(evt, val):
        gb["TargetObject"] = lcTargetObject.Button.val
        gb["MaxDistForAxis"] = lcMaxDistForAxis.Button.val * gb["MaxAroundDist"]
        gb["GridSize"] = [lcGridSize.Button.val * gb["MaxAroundDist"]] * 3
        
        # Comes out of EditMode temporarily
        lcEditMode = B.Window.EditMode()
        if lcEditMode:
            B.Window.EditMode(0)
        
        obj = B.Object.Get(gb["TargetObject"])
        mesh_name = obj.getData().name
        lcVerts = B.Mesh.Get(mesh_name).verts
        lcTargetVerts = [lcVerts[i] for i in lcVerts.selected()]
        
        # Restore the state of EditMode
        if lcEditMode:
            B.Window.EditMode(1)
        
        lcPGM = PointsGridManager(gb["GridSize"])
        lcPGM.PositionGetter = GetPositionFromMVert
        lcPGM.Add(lcVerts)
        lcNM = NormalManager()
        lcNM.Calculate(lcPGM, lcTargetVerts, gb["MaxDistForAxis"])
        DrawNormalVector(lcNM, lcTargetVerts, gb["MaxDistForAxis"] / 3.0)
        
        B.Redraw()
        
    # Make layout for the GUI
    
    lcBase = BControlVFlowLayout(
        CellSpacing=10,
    )
    
    
    
    lcVFlo = BControlVFlowLayout(
        CellSpacing=2,
        Backcolor=[0.5] * 3,
    )
    lcBase.Append(lcVFlo)
    
    
    
    lcHFlo = BControlHFlowLayout(
        HAlign=0.5,
        CellSpacing=3,
    )
    lcLabe = BControlLabel(
        Margin=[3] * 4,
        Text=__scriptname__ + " " + __version__,
        Color=[1.0] * 3,
    )
    lcHFlo.Append(lcLabe)
    lcVFlo.Append(lcHFlo)
    
    
    
    objs = B.Object.GetSelected()
    if not objs:
        obj_name = "Must set!"
    else:
        obj_name = objs[0].name

    lcHFlo = BControlHFlowLayout(
        CellSpacing=3,
        Backcolor=[0.8] * 3,
    )
    lcLabe = BControlLabel(
        VAlign=0.5,
        Text="TargetObject: (= Plane, etc...)",
        Width=200,
        AutoSize=False,
    )
    lcHFlo.Append(lcLabe)
    lcNumb = BControlString(
        Text="",
        InitValue=obj_name,
        ToolTip="Must set! Specify the mesh name that has a point cloud to skin.",
    )
    lcHFlo.Append(lcNumb)
    lcTargetObject = lcNumb
    lcVFlo.Append(lcHFlo)
    
    
    
    lcHFlo = BControlHFlowLayout(
        CellSpacing=3,
        Backcolor=[0.8] * 3,
    )
    lcLabe = BControlLabel(
        VAlign=0.5,
        Text="DistForSearch: (call it \"d\")",
        Width=200,
        AutoSize=False,
    )
    lcHFlo.Append(lcLabe)
    lcNumb = BControlNumber(
        Text="",
        InitValue=0.1,
        Min=0.001,
        Max=1000.000,
        ToolTip="Must set! Specify the search distance for vertices around each center vertex. It depends on the density of the vertices in the point cloud.",
    )
    lcHFlo.Append(lcNumb)
    lcMaxAroundDist = lcNumb
    lcVFlo.Append(lcHFlo)
    
    
    
    lcHFlo = BControlHFlowLayout(
        CellSpacing=3,
        Backcolor=[0.8] * 3,
    )
    lcLabe = BControlLabel(
        VAlign=0.5,
        Text="DistForAxis/d: (= 1 to 3)",
        Width=200,
        AutoSize=False,
    )
    lcHFlo.Append(lcLabe)
    lcNumb = BControlNumber(
        Text="",
        InitValue=2.0,
        Min=1.0,
        Max=10.0,
        ToolTip="Specify the search distance to calculate average normal vectors. It's the ratio to d and better to set to 1 to 3.",
    )
    lcHFlo.Append(lcNumb)
    lcMaxDistForAxis = lcNumb
    lcVFlo.Append(lcHFlo)
    
    
    
    lcHFlo = BControlHFlowLayout(
        CellSpacing=3,
        Backcolor=[0.8] * 3,
    )
    lcLabe = BControlLabel(
        VAlign=0.5,
        Text="GridSize/d: (= 2 to 4)",
        Width=200,
        AutoSize=False,
    )
    lcHFlo.Append(lcLabe)
    lcNumb = BControlNumber(
        Text="",
        InitValue=3.0,
        Min=1.0,
        Max=10.0,
        ToolTip="Specify the cell size of PointsGridManager. It affects only the speed performance. It's the ratio to d and better to set to 2 to 4.",
    )
    lcHFlo.Append(lcNumb)
    lcGridSize = lcNumb
    lcVFlo.Append(lcHFlo)
    
    
    
    lcHFlo = BControlHFlowLayout(
        HAlign=0.5,
        CellSpacing=5,
    )
    lcButt = BControlButton(
        Text="Skin",
        ToolTip="Run the script and skin the point cloud.",
    )
    lcButt.EventHandler_OnCallBack.Add(Skin)
    lcHFlo.Append(lcButt)
    lcButt = BControlButton(
        Text="Exit",
        ToolTip="End the script.",
    )
    lcButt.EventHandler_OnCallBack.Add(Exit)
    lcHFlo.Append(lcButt)
    lcVFlo.Append(lcHFlo)
    
    
    
    lcVFlo = BControlVFlowLayout(
        CellSpacing=2,
        Backcolor=[0.5] * 3,
    )
    lcBase.Append(lcVFlo)



    lcHFlo = BControlHFlowLayout(
        HAlign=0.5,
        CellSpacing=3,
    )
    lcLabe = BControlLabel(
        Margin=[3] * 4,
        Text="For Debug",
        Color=[1.0] * 3,
    )
    lcHFlo.Append(lcLabe)
    lcVFlo.Append(lcHFlo)

    
    
    lcHFlo = BControlHFlowLayout(
        CellSpacing=5,
    )
    lcButt = BControlButton(
        Size=[40, 20],
        Text="Nor",
        ToolTip="Draw average normal vectors for the selected vertices.",
    )
    lcButt.EventHandler_OnCallBack.Add(Debug_DrawNormal)
    lcHFlo.Append(lcButt)
    lcTogg = BControlToggle(
        Size=[40, 20],
        Text="Pro",
        ToolTip="Whether to use TimeProfiler. With it, it will takes more time but you can see the details of the time profile.",
    )
    lcHFlo.Append(lcTogg)
    lcUseTimeProfile = lcTogg
    lcVFlo.Append(lcHFlo)
    
    
    
    lcProv = BControlProvider(lcBase)
    lcProv.Start()
    
def Main_inMenu():
    global gbTP
    
    ui = {}
    ui["DistForSearch"] = B.Draw.Create(1.0)
    ui["DistForAxis/d"] = B.Draw.Create(2.0)
    ui["GridSize/d"] = B.Draw.Create(3.0)
    
    objs = B.Object.GetSelected()
    if not objs:
        B.Draw.PupMenu("Error: No objects are selected.%t|Please specify the object that you want to skin.")
        return
    lcTargetObject = objs[0].name
    
    block = []
    block.append(("DistForSearch=d: ", ui["DistForSearch"], 0.001, 1000.0, "Must set! Specify the search distance for vertices around each center."))
    block.append(("DistForAxis/d: ", ui["DistForAxis/d"], 1.000, 10.000, "Specify the search distance to calculate average normal. It might be 1 to 3."))
    block.append(("GridSize/d: ", ui["GridSize/d"], 1.000, 10.000, "Specify the cell size of PointsGridManager. It might be 2 to 4."))
    lcResult = B.Draw.PupBlock("Skinning Setups:", block)
    if not lcResult:
        return
    
    gb["TargetObject"] = lcTargetObject
    gb["MaxAroundDist"] = ui["DistForSearch"].val
    gb["MaxDistForAxis"] = ui["DistForAxis/d"].val * gb["MaxAroundDist"]
    gb["GridSize"] = [ui["GridSize/d"].val * gb["MaxAroundDist"]] * 3
    gb["IgnoreErrors"] = True
        
    gbTP = TimeProfiler(False)
    gbTP.ShowMode = 2
    print "-----Start-----"
    SkinVerts() # main function of skinning
    print "-----gbLog-----"
    print gbLog
    print gbTP.Print()

def Main():
    if B.Window.EditMode():
        Main_inMenu()
    else:
        Main_inScript()

    
Main()
