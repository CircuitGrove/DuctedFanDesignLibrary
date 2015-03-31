
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

def BladeAxialStress(spanPts,areaArray, YoungsModulus, density,rpm):

    if(len(spanPts) != len(areaArray)):
        return [];
    
    stress = []
    dx = 0
    dy = 0
    force = 0
    
    angVel = rpm/60*2*math.pi
    
    #from tip to root
    for i in reversed(range(0,len(areaArray))):
        if(i == 0):
            dx = (spanPts[i+1] - spanPts[i])/2
        elif(i == len(spanPts)-1):
            dx = (spanPts[i] - spanPts[i-1])/2
        else:
            dx = (spanPts[i+1] - spanPts[i])/2 + (spanPts[i] - spanPts[i-1])/2
        
        volume = dx*areaArray[i]/math.pow(1000,3) #m^3
        mass = density*volume
        
        force += mass*pow(angVel,2)*(spanPts[i]/1000)
        stress.append(force/(areaArray[i]/math.pow(1000,2))) #N/m^2
        
        print(" ")
        print("Span: " + str(spanPts[i]))
        print("Mass: " + str(mass))
        print("force: " + str(force))
        print("Area: " + str(areaArray[i]))
        print("stress: " + str(stress[len(stress)-1]))
        
    return (stress)
        
    
class PropellerProps:

    #Chord interpolation
    rootChord = 10 #root chord
    transitionChord = 25
    tipChord = 10 #tip chord        
    
    rootSlope = 00.0;
    transitionSlope = 0.0;
    tipSlope = -5.0;
    
    rootStrength = 20.0;
    transitionStrengthRoot = 10.0;
    transitionStrengthTip = 10.0;
    tipStrength = 30.0;

    #Skew interpolation
    rootSkew=0.5;
    transitionSkew=0.6; 
    tipSkew=1.0;
    
    rootSkewSlope=10.0; 
    transitionSkewSlope=0.0;
    tipSkewSlope=0.0;
    
    rootSkewStrength=2.0; 
    transitionSkewStrengthRoot=4.0;
    transitionSkewStrengthTip=10.0;
    tipSkewStrength=30.0;
    
    #thickness interpolation
    rootThick=0.55;
    transitionThick=0.15; 
    tipThick=0.15;
    
    rootThickSlope=0.0; 
    transitionThickSlope=0.0;
    tipThickSlope=0.0;
    
    rootThickStrength=4.0; 
    transitionThickStrengthRoot=4.0;
    transitionThickStrengthTip=10.0;
    tipThickStrength=30.0;
    
    def Allouette(self):

        #Chord interpolation
        self.rootChord = 10 #root chord
        self.transitionChord = 25
        self.tipChord = 10 #tip chord        
        
        self.rootSlope = 00.0;
        self.transitionSlope = 0.0;
        self.tipSlope = -5.0;
        
        self.rootStrength = 20.0;
        self.transitionStrengthRoot = 10.0;
        self.transitionStrengthTip = 10.0;
        self.tipStrength = 30.0;

        #Skew interpolation
        self.rootSkew=0.5;
        self.transitionSkew=0.6; 
        self.tipSkew=1.0;
        
        self.rootSkewSlope=10.0; 
        self.transitionSkewSlope=0.0;
        self.tipSkewSlope=0.0;
        
        self.rootSkewStrength=2.0; 
        self.transitionSkewStrengthRoot=4.0;
        self.transitionSkewStrengthTip=10.0;
        self.tipSkewStrength=30.0;
        
        #thickness interpolation
        self.rootThick=0.55;
        self.transitionThick=0.15; 
        self.tipThick=0.15;
        
        self.rootThickSlope=0.0; 
        self.transitionThickSlope=0.0;
        self.tipThickSlope=0.0;
        
        self.rootThickStrength=4.0; 
        self.transitionThickStrengthRoot=4.0;
        self.transitionThickStrengthTip=10.0;
        self.tipThickStrength=30.0;
        
    def Standard(self):
    
        #Chord interpolation
        self.rootChord = 10 #root chord
        self.transitionChord = 20
        self.tipChord = 13 #tip chord        
        
        self.rootSlope = 0.0;
        self.transitionSlope = 0.0;
        self.tipSlope = 0.0;
        
        self.rootStrength = 10.0;
        self.transitionStrengthRoot = 20.0;
        self.transitionStrengthTip = 20.0;
        self.tipStrength = 0.0;

        #Skew interpolation
        self.rootSkew=0.5;
        self.transitionSkew=0.5; 
        self.tipSkew=0.5;
        
        self.rootSkewSlope=0.0; 
        self.transitionSkewSlope=0.0;
        self.tipSkewSlope=0.0;
        
        self.rootSkewStrength=0.0; 
        self.transitionSkewStrengthRoot=0.0;
        self.transitionSkewStrengthTip=0.0;
        self.tipSkewStrength=0.0;
        
        #thickness interpolation
        self.rootThick=0.55;
        self.transitionThick=0.15; 
        self.tipThick=0.10;
        
        self.rootThickSlope=0.0; 
        self.transitionThickSlope=0.0;
        self.tipThickSlope=0.0;
        
        self.rootThickStrength=0.0; 
        self.transitionThickStrengthRoot=0.0;
        self.transitionThickStrengthTip=0.0;
        self.tipThickStrength=0.0;
        
def Propeller(propName,propDia,pitch,\
        hubHeight,hubDia,axleDia,\
		PropellerProps,\
        bladeTransition,nspan,npts,nBlades):
		
    p=PropellerProps    
        
    res = 64  #used to define cylinder resolution.
    
    #initialising arrays we'll need.
    verts = []
    tmpVerts = []
    tmpVert = [0,0,0]
    faces = []
    origin=(0,0,0)
    centerOfTwist = [0,0]
    
    p.rootSlope *= math.pi/180
    p.transitionSlope *= math.pi/180
    p.tipSlope *= math.pi/180
    
    p.rootSkewSlope *= math.pi/180
    p.transitionSkewSlope *= math.pi/180
    p.tipSkewSlope *= math.pi/180
    
    #An array of the chord lengths at each span point
    chordArray = []
    #An array of the NACA4 digits at each span point.
    NACAArray = []
    #An array that holds the position along the blade span of the airfoil cross-sections
    sPos = []
    #An array that holds the amount of skew of each airfoil cross-section
    skew = []

   
    #Blade root will be at center of rotation.
    bladeHeight = propDia/2 
    bladeLen = bladeHeight - bladeTransition
    dSpan = bladeHeight/nspan
    
    lastI = 0;
    for i in range(0,nspan+1):

        span = i*dSpan
        
        if(span < bladeTransition):
                        
            #Using cubic spline interpolation.
            t = span/bladeTransition
            tm1 = 1-t
            
            #root to transition point interpolation
            y1 = p.rootChord
            y2 = p.rootChord + math.sin(p.rootSlope)*p.rootStrength
            y3 = p.transitionChord - math.sin(p.transitionSlope)*p.transitionStrengthRoot
            y4 = p.transitionChord
            
            chord = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            
            chordArray.append(chord)
            
            x1=0
            x2=math.cos(p.rootSlope)*p.rootStrength
            x3=(bladeTransition-math.cos(p.transitionSlope)*p.transitionStrengthRoot)
            x4=bladeTransition
            
            x = pow(tm1,3)*x1 + 3*pow(tm1,2)*t*x2 + 3*tm1*pow(t,2)*x3 + pow(t,3)*x4
            sPos.append(x)
            
            
            y1 = p.rootThick
            y2 = p.rootThick + math.sin(p.rootThickSlope)*p.rootThickStrength
            y3 = p.transitionThick - math.sin(p.transitionThickSlope)*p.transitionThickStrengthRoot
            y4 = p.transitionThick
            
            thickPt = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            print(thickPt)
            NACAArray.append([5,3,int(thickPt*10),int(thickPt*100-int(thickPt*10)*10)])
            
            y1 = p.rootSkew
            y2 = p.rootSkew + math.sin(p.rootSkewSlope)*p.rootSkewStrength
            y3 = p.transitionSkew - math.sin(p.transitionSkewSlope)*p.transitionSkewStrengthRoot
            y4 = p.transitionSkew
            
            skewPt = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            skew.append(skewPt);
        else:
                
            #Using cubic spline interpolation.
            t = (span-bladeTransition)/bladeLen
            tm1 = 1-t
            
            y1 = p.transitionChord
            y2 = p.transitionChord + math.sin(p.transitionSlope)*p.transitionStrengthTip
            y3 = p.tipChord - math.sin(p.tipSlope)*p.tipStrength
            y4 = p.tipChord
            
            chord = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            
            chordArray.append(chord)
            
            x1=0
            x2=math.cos(p.transitionSlope)*p.transitionStrengthTip
            x3=(bladeLen-math.cos(p.tipSlope)*p.tipStrength)
            x4=bladeLen
            
            x = pow(tm1,3)*x1 + 3*pow(tm1,2)*t*x2 + 3*tm1*pow(t,2)*x3 + pow(t,3)*x4
            sPos.append(bladeTransition+x)
            
            y1 = p.transitionThick
            y2 = p.transitionThick + math.sin(p.rootThickSlope)*p.rootThickStrength
            y3 = p.tipThick - math.sin(p.transitionThickSlope)*p.transitionThickStrengthTip
            y4 = p.tipThick
            
            thickPt = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            
            NACAArray.append([5,3,int(thickPt*10),int(thickPt*100-int(thickPt*10)*10)])
            
            y1 = p.transitionSkew
            y2 = p.transitionSkew+ math.sin(p.transitionSkewSlope)*p.transitionSkewStrengthTip
            y3 = p.tipSkew - math.sin(p.tipSkewSlope)*p.tipSkewStrength
            y4 = p.tipSkew
            
            skewPt = pow(tm1,3)*y1 + 3*pow(tm1,2)*t*y2 + 3*tm1*pow(t,2)*y3 + pow(t,3)*y4
            skew.append(skewPt);
        
         
    
    #error check of inputs
    if(len(chordArray) != nspan or len(NACAArray) != nspan):
        print("The size of the array of chord lengths or the array of airfoil NACA digits does not match the number of span points used to define the blade geometry.")
    
    #Delete any existing prop geoms
    DLUtils.DeleteMesh(propName)
	   
    #Generate Hub   
    DLUtils.DrawCylinder("Hub",hubDia,0,hubHeight,res)#use a 0.001m tolerance which we'll trim off.
    cyl = bpy.data.objects["Hub"]
    cyl.name = propName
    cyl.data.name = propName
    DLUtils.SelectOnly(propName)
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    DLUtils.MoveObject(propName,[2.0,0,0])
    
    areaArray = []
 
    #Generate vertex coordinates with twist and scale along the span        
    for i in range(0,nspan+1): 
        span = sPos[i] #i*dSpan
        if(span == 0):
            twistAngle = 0
        elif(span < bladeTransition):
             twistAngle = math.atan(pitch/(2*math.pi*span))*span/bladeTransition
        else:
            twistAngle = math.atan(pitch/(2*math.pi*span))
        
        
        #get the airfoil profile vertices
        tmpVerts = TurboMachLib.NACA4Profile(camber=NACAArray[i][0],thickness=NACAArray[i][2]*10+NACAArray[i][3],camberPos=NACAArray[i][1]*10,chord=chordArray[i],npts=npts) 
        areaArray.append(0);
        
        centerOfTwist[0] = chordArray[i]*skew[i]
        #centerOfTwist[1] = raiseFoil
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
     
            if(v != 0):
                dx = abs(verts[len(verts)-1][0] - verts[len(verts)-2][0])
                dy = abs(verts[len(verts)-1][1] + verts[len(verts)-2][1])/2
                areaArray[i] +=  dy*dx
                
            

    
    
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
    for i in range(1,npts-1):
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
    DLUtils.DrawBox("box", hubDia*1.1,hubDia*1.1,hubDia*1.1)
    DLUtils.MoveObject("box",[propDia/2+hubHeight/2+0.001,0,0])
    DLUtils.BooleanMesh(propName,"box","DIFFERENCE",True) 
    
    #cut the axle hole   
    DLUtils.DrawCylinder("hole",axleDia,0,hubHeight*2,res)
    DLUtils.SelectOnly("hole")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    DLUtils.BooleanMesh(propName,"hole",'DIFFERENCE',True)
    
   
    #Cut room for the axle shive
    DLUtils.DrawCylinder("ShiveHole",(hubDia-axleDia)/4+axleDia,0,hubHeight/1.5,res)
    DLUtils.SelectOnly("ShiveHole")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    DLUtils.BooleanMesh(propName,"ShiveHole",'DIFFERENCE',True)
    #DLUtils.MoveObject(propName,[2.0,0,0])
    
    #trim the blades to the proper dia
    DLUtils.DrawCylinder("BladeTrim",propDia,0,propDia,256)
    DLUtils.SelectOnly("BladeTrim")
    bpy.ops.transform.rotate(value=math.radians(90),axis=(0.0,1.0,0.0))
    DLUtils.BooleanMesh(propName,"BladeTrim",'INTERSECT',True)
    
    #done!
    print((BladeAxialStress(sPos,areaArray, 40e6, 1300,15000)))
    
    return
