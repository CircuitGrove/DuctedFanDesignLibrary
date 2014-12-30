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
        
        
        
        rootChord = 15 #root chord
        tipChord = 10 #tip chord        
        rootCPPos = 0.1 #Root control point position (@ root =0.0, @ tip = 1.0)
        tipCPPos = 0.9 #Tip control point position (@ root =0.0, @ tip = 1.0)
        rootCPStrength = 2.5 # root chord multiplier
        tipCPStrength =  0.8 # tip chord multiplier
        rootSkew = 0.5 #Shifts the airfoil forward or back, 0.5 is neutral
        rootCPSkew = 0.5 #Shifts the airfoil forward or back, 0.5 is neutral
        tipCPSkew = 0.5 #Shifts the airfoil forward or back, 0.5 is neutral
        tipSkew = 0.5 #Shifts the airfoil forward or back, 0.5 is neutral

        PropLibrary.Prop(propName="test",propDia=9*25.4,pitch=6*25.4,\
        hubHeight=16,hubDia=20,axleDia=7,\
		rootChord=rootChord,rootCPPos=rootCPPos,rootCPStrength=rootCPStrength,\
        tipChord=tipChord,tipCPPos=tipCPPos,tipCPStrength=tipCPStrength,\
        rootSkew=rootSkew,rootCPSkew=rootCPSkew, tipCPSkew=tipCPSkew, tipSkew=tipSkew,\
        nspan=10,npts=20,nBlades=3)
        
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

