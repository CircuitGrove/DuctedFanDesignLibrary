
#///////////////////////////////////////////////
# 	
#    Turbomachinery Design Library (Python/Blender)
#    Copyright (C) 2014  Circuit Grove
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    To contribute to the Circuit Grove distribution, contact contrib@circuitgrove.com 
#
#//////////////////////////////////////////////
# 	
#   
#
#	
#
#///////////////////////////////////////////////

import bpy
import os
import math
import mathutils
import DLUtils
import TurboMachLib

def Prop(propName,propDia,pitch,\
        hubHeight,hubDia,axleDia,\
		chordArray,NACAArray,\
        nspan,npts,nBlades):
		
    res = 64
    verts = []
    tmpVerts = []
    tmpVert = [0,0,0]
    faces = []
    origin=(0,0,0)
    centerOfTwist = [0,0]
    
    #Delete any existing prop geoms
    DLUtils.DeleteMesh(propName)
	
    #Generate Hub    
    bpy.ops.mesh.primitive_cylinder_add(vertices=res,radius=hubDia/2,depth=hubHeight,location=(0,0,0)) 
    cyl = bpy.data.objects["Cylinder"]
    cyl.name = propName
    cyl.data.name = propName
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
	#Blade root will be at center of rotation, scale blade height by 
    #5% because we will be trimming the excess.
    bladeHeight = propDia/2*1.05 
 
    #Generate vertex coordinates with twist and scale along the span        
    dspan = bladeHeight/nspan
    for i in range(0,nspan+1): 
        span = i*dspan
        if(span == 0):
            twistAngle = math.pi/2
        else:
            twistAngle = math.atan(pitch/(2*math.pi*span))
        
        #get the airfoil profile vertices
        tmpVerts = TurboMachLib.NACA4Profile(camber=0,thickness=10,chord=20,npts=50) 
        
        centerOfTwist[0] = 20/2
        
        for v in range(0,len(tmpVerts)):
            
            #shift all verts for twisting
            tmpVerts[v][0] -= centerOfTwist[0]
            tmpVerts[v][1] -= centerOfTwist[1]
           
            #Twist the airfoil vertices.  First we shift them to get the desired center of rotation.
            tmpVert[0] = tmpVerts[v][0]*math.cos(twistAngle) -tmpVerts[v][1]*math.sin(twistAngle)
            tmpVert[1] = tmpVerts[v][0]*math.sin(twistAngle) +tmpVerts[1][1]*math.cos(twistAngle)
            
            #shift all verts to their proper span location in Z
            tmpVert[2] = span
             
            #append the vert to the master vertex list
            verts.append((tmpVert[0],tmpVert[1],tmpVert[2]))
            
    #Generate Polies from vertex IDs
    #Bottom Cap
    faces.append((0,1,npts+1))
    for i in range(0,npts-1):
        faces.append((i,i+1,npts+i+1))    
        faces.append((i,npts+i+1,npts+i))    

    #Middle
    nPerStage = npts*2
    for j in range(0,nspan):
        for i in range(0,npts-1):
            faces.append((nPerStage*j+i,nPerStage*(j+1)+i,nPerStage*(j+1)+i+1))
            faces.append((nPerStage*j+i,nPerStage*(j+1)+i+1,nPerStage*j+i+1))
        for i in range(0,npts-1):
            faces.append((nPerStage*j+i+npts,nPerStage*(j+1)+i+1+npts,nPerStage*(j+1)+i+npts))
            faces.append((nPerStage*j+i+npts,nPerStage*j+i+1+npts,nPerStage*(j+1)+i+1+npts))
        faces.append((nPerStage*j+npts-1,nPerStage*(j+1)+npts-1,nPerStage*(j+1)+npts*2-1))
        faces.append((nPerStage*j+npts-1,nPerStage*(j+1)+npts*2-1,nPerStage*(j)+npts*2-1))
    #Top Cap
    faces.append((nPerStage*(nspan),nPerStage*(nspan)+1,nPerStage*(nspan)+npts+1))
    for i in range(0,npts-1):
        faces.append((nPerStage*(nspan)+i,nPerStage*(nspan)+npts+i+1,nPerStage*(nspan)+i+1))    
        faces.append((nPerStage*(nspan)+i,nPerStage*(nspan)+npts+i,nPerStage*(nspan)+npts+i+1))    
    
    #Create Blender object for the blade    
    blade = DLUtils.createMesh(propName, origin, verts, [], faces)
    
    return