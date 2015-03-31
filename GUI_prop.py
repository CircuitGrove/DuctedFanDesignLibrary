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
        
        
       
        
        propellerProps = PropLibrary.PropellerProps()
       
        propellerProps.Standard()
        
        PropLibrary.Propeller(propName="test",propDia=7*25.4,pitch=4*25.4,\
        hubHeight=8.5,hubDia=13,axleDia=5.2,\
		PropellerProps=propellerProps,\
        bladeTransition=30,nspan=20,npts=20,nBlades=2)
        
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



