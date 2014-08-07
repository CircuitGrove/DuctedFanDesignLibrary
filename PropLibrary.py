
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
import time

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
    
    #error check of inputs
    if(len(chordArray) != nspan or len(NACAArray) != nspan):
        print("The size of the array of chord lengths or the array of airfoil NACA digits does not match the number of span points used to define the blade geometry.")
    
    #Delete any existing prop geoms
    DLUtils.DeleteMesh(propName)
	   
    #Generate Hub   
    DLUtils.DrawCylinder("Hub",hubDia,0,hubHeight+0.001,res)#use a 0.001m tolerance which we'll trim off.
    cyl = bpy.data.objects["Hub"]
    cyl.name = propName
    cyl.data.name = propName
    DLUtils.SelectOnly(propName)
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    
	#Blade root will be at center of rotation.
    bladeHeight = propDia/2 
 
    #Generate vertex coordinates with twist and scale along the span        
    dspan = bladeHeight/nspan
    for i in range(0,nspan+1): 
        span = i*dspan
        if(span == 0):
            twistAngle = math.pi/2
        else:
            twistAngle = math.atan(pitch/(2*math.pi*span))
        
        #get the airfoil profile vertices
        tmpVerts = TurboMachLib.NACA4Profile(camber=NACAArray[i][0]*10,thickness=NACAArray[i][2]*10+NACAArray[i][3],camberPos=NACAArray[i][1]*10,chord=chordArray[i],npts=npts) 
        
        centerOfTwist[0] = 20/2
        
        for v in range(0,len(tmpVerts)):
            
            #shift all verts for twisting
            tmpVerts[v][0] -= centerOfTwist[0]
            tmpVerts[v][1] -= centerOfTwist[1]
           
            #Twist the airfoil vertices.  First we shift them to get the desired center of rotation.
            tmpVert[0] = tmpVerts[v][0]*math.cos(twistAngle) -tmpVerts[v][1]*math.sin(twistAngle)
            tmpVert[1] = tmpVerts[v][0]*math.sin(twistAngle) +tmpVerts[v][1]*math.cos(twistAngle)
            
            #shift all verts to their proper span location in Z
            tmpVert[2] = span+0.01*bladeHeight #Shift blade by 1% of blade height to prevent poor boolean ops
             
            #append the vert to the master vertex list
            verts.append((tmpVert[0],tmpVert[1],tmpVert[2]))
     

    
    
    #Generate Polies from vertex IDs
    #Bottom Cap
    faces.append((0,1,npts))
    for i in range(1,npts-1):
        faces.append((i,i+1,npts+i))    
        faces.append((i,npts+i,npts+i-1))    
    
    #Middle
    nPerStage = npts*2-1
    for j in range(0,nspan):
        #Top Side
        for i in range(0,npts-1):
            faces.append((nPerStage*j+i,nPerStage*(j+1)+i,nPerStage*(j+1)+i+1))
            faces.append((nPerStage*j+i,nPerStage*(j+1)+i+1,nPerStage*j+i+1))
        
        #First strip for bottom side (hooks to verts from top side)
        faces.append((nPerStage*j,nPerStage*(j+1)+npts,nPerStage*(j+1)))
        faces.append((nPerStage*j,nPerStage*j+npts,nPerStage*(j+1)+npts))
    
        #Rest of bottom side
        for i in range(0,npts-2):
            faces.append((nPerStage*j+i+npts,nPerStage*(j+1)+i+npts+1,nPerStage*(j+1)+i+npts))
            faces.append((nPerStage*j+i+npts,nPerStage*j+i+npts+1,nPerStage*(j+1)+i+npts+1))
        
        #Back face
        faces.append((nPerStage*j+npts-1,nPerStage*(j+1)+npts-1,nPerStage*(j+1)+npts*2-2))
        faces.append((nPerStage*j+npts-1,nPerStage*(j+1)+npts*2-2,nPerStage*(j)+npts*2-2))
    
    #Top Cap
    faces.append((nPerStage*(nspan),nPerStage*(nspan)+1,nPerStage*(nspan)+npts))
    for i in range(1,npts-2):
        faces.append((nPerStage*(nspan)+i,nPerStage*(nspan)+npts+i,nPerStage*(nspan)+i+1))    
        faces.append((nPerStage*(nspan)+i,nPerStage*(nspan)+npts+i-1,nPerStage*(nspan)+npts+i))    
    
     
    #Create Blender object for the blade
    dAngle = 360.0/nBlades
    
    for i in range(0,nBlades):
        print("Draw Blade_" + str(i))
        blade = DLUtils.createMesh("Blade_"+str(i), origin, verts, [], faces)
        DLUtils.SelectOnly("Blade_"+str(i))
        bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,0.0,1.0))
        bpy.ops.transform.rotate(value=math.radians(dAngle)*i,axis=(1.0,0.0,0.0))
        
    #Union the blades to the hub
    for i in range(0,nBlades):
        print("Union: Blade_" +str(i))
        DLUtils.BooleanMesh(propName,"Blade_"+str(i),"UNION",True) 
        
    #trim the blades to hub height
    DLUtils.DrawBox("box", propDia,propDia,propDia)
    DLUtils.MoveObject("box",[propDia/2+hubHeight/2,0,0])
    DLUtils.BooleanMesh(propName,"box","DIFFERENCE",True) 
    
    #cut the axle hole   
    DLUtils.DrawCylinder("hole",axleDia,0,hubHeight*2,res)
    DLUtils.SelectOnly("hole")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    DLUtils.BooleanMesh(propName,"hole",'DIFFERENCE',True)
    
   
    
    #trim the blades to the proper dia
    
    #done!
    
   
        
    return