
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
	
    #Delete any existing prop geoms
    DLUtils.DeleteMesh(propName)
	
    #Generate Hub    
    bpy.ops.mesh.primitive_cylinder_add(vertices=res,radius=hubDia/2,depth=hubHeight,location=(0,0,0)) 
    cyl = bpy.data.objects["Cylinder"]
    cyl.name = propName
    cyl.data.name = propName
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
	
    verts = TurboMachLib.NACA4Profile(camber=0,thickness=10,chord=20,npts=50) 
	
    #print(verts)
    
    return