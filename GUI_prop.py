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

import sys
sys.path.append("c:/users/andre/Desktop/archive/Mavrix_aircraft/Tools/DuctedFanDesignLibrary") #We need to instruct Blender about where the library files are
sys.path.append("C:\Python33\Lib\site-packages")#We need access to NumPy/SciPy Python
import bpy
import math
import mathutils
import DLUtils
import TurboMachLib
import PropLibrary

class DrawProp(bpy.types.Operator):
    bl_idname = "draw.prop"
    bl_label = "Draw Propellor"

    def execute(self, context):
        
        #we need to pass in an array of the chord lengths at each span point
        chordArray=[11,12,15.6,16,14,12.5,10.4,9.4,8.4,7.4,6]
        
        #We need to pass in an array of the NACA4 digits at each span point.
        NACAArray=[[2,4,5,5],[2,4,4,5],[2,4,3,0],[2,4,1,5],[2,4,1,2],[2,4,1,2],[2,4,1,2],[2,4,1,2],[2,4,1,2],[2,4,1,2],[2,4,1,2]]

        PropLibrary.Prop(propName="test",propDia=6*25.4,pitch=4*25.4,\
        hubHeight=12,hubDia=13,axleDia=5.0,\
		chordArray=chordArray,NACAArray=NACAArray,\
        nspan=10,npts=20,nBlades=2)
        
        return {'FINISHED'}
        
        

class CustomPanel(bpy.types.Panel):
    """A Custom Panel"""
    bl_label = "Propeller Design Library"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    
    def draw(self,context):
        layout = self.layout
        ###################################################
               
        row = layout.row()
        row.prop(context.scene,"propName")
        row = layout.row()
        row.operator("draw.prop")

def register():        

###########
## Prop Properties
##########

    bpy.types.Scene.propName = bpy.props.StringProperty(
            name="Propellor Name",
            description="Name to assign to the Propellor object and mesh",
            default="Propellor")


    
    bpy.utils.register_class(DrawProp)
    bpy.utils.register_class(CustomPanel)

def unregister():
    bpy.utils.unregister_class(CustomPanel)
 
if __name__ == "__main__":
    register()       
