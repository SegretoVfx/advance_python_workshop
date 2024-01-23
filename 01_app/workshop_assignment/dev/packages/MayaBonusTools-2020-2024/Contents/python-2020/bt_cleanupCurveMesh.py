# Copyright (C) 1997-2020 Autodesk, Inc., and/or its licensors.
# All rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its licensors,
# which is protected by U.S. and Canadian federal copyright law and by
# international treaties.
#
# The Data is provided for use exclusively by You. You have the right to use,
# modify, and incorporate this Data into other products for purposes authorized 
# by the Autodesk software license agreement, without fee.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. AUTODESK
# DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
# INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE 
# OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS
# LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK AND/OR ITS
# LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.
#
# Author:   Steven T. L. Roselle    
#
# Created:        ( 04/01/15 )

from pymel.core import *
import maya.cmds as cmds


def bt_cleanupCurveMesh():
        
    instanceNode = ''
    extrudeNode = ''
    
    select(filterExpand(sm=12),r=1)
    select(listRelatives( parent=True))
    meshes = ls(sl=1)    
    
    if (meshes.__len__()):
        
        for mesh in meshes:        

            if (attributeQuery ('taper', exists=1, node=mesh)):
                extrudeNode = (listConnections (mesh+'.taper'))
                instanceNode = (listConnections (extrudeNode[0]+'.path'))
                        
            #delete remaining history and constraints
            delete (mesh, ch=1)
            delete (mesh, constraints=1)      
            
            if (attributeQuery ('width', exists=1, node=mesh)):
                delete(listConnections (mesh+'.width'))
                deleteAttr (mesh+".width")
            if (attributeQuery ('orientation', exists=1, node=mesh)):
                delete(listConnections (mesh+'.orientation'))
                deleteAttr (mesh+".orientation")
                 
            if (attributeQuery ('curvature', exists=1, node=mesh)):
                deleteAttr (mesh+".curvature")
            if (attributeQuery ('taper', exists=1, node=mesh)):
                deleteAttr (mesh+".taper")
            if (attributeQuery ('twist', exists=1, node=mesh)):
                deleteAttr (mesh+".twist")
            if (attributeQuery ('lengthDivisionSpacing', exists=1, node=mesh)):
                deleteAttr (mesh+'.lengthDivisionSpacing') 
            if (attributeQuery ('lengthDivisions', exists=1, node=mesh)):
                deleteAttr (mesh+".lengthDivisions")                               
            if (attributeQuery ('widthDivisions', exists=1, node=mesh)):
                deleteAttr (mesh+".widthDivisions")  
                
            if (objExists (instanceNode)):
                delete (instanceNode)
                
    else:
        warning ('No meshes selected.\n')
 
        
#bt_cleanupCurveMesh()


