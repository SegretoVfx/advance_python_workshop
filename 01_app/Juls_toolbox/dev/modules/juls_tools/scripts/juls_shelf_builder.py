# SHELF BUILDER **************************************************************
# Description   = This creates the class needed for the shelf creation
# functions.
#
# File name     = juls_shelf_builder.py
# Date of birth = 1/10/2024
#
# Author   = Juls
# Email   = segretovfx@gmail.com
#
# Usage = This will work only if used with this three other files:
#         juls_shelf_builder
#         juls_shelf_functions
#         juls_shelf_info
#
# *********************************************************************



'''juls_shelf_builder.py'''

import maya.cmds as cmds

import juls_shelf_info



def _null(*args):
    pass



class Builder():
    '''Class to build different shelves buttons and separators
    the use of these buttons is done within the "CustomShelf" class.'''

    def __init__(self, name=juls_shelf_info.shelf_name, iconPath=""):
        self.name = name

        self.iconPath = iconPath

        self.labelBackground = (.2, 0, .5, 1)
        self.labelColour = (0, 1, 1)

        self.clean_old_shelf()
        cmds.setParent(self.name)
        self.build()

    def build(self):
        '''This method should be overwritten in derived classes to actually 
        build the shelf elements. Otherwise, nothing is added to the shelf.'''
        pass

    def add_button(self, label, annotation, icon = "defaultIconTest.png", command =_null, 
                   doubleCommand =_null, enable=True):
        '''Adds a shelf button with the specified label, command, double click 
        command and image.'''
        cmds.setParent(self.name)
        if icon:
            icon = self.iconPath + icon
        cmds.shelfButton(width= 37, height= 37, image=icon, l=label, ndp=True,  
                         command =command, dcc=doubleCommand, enable=enable, 
                         imageOverlayLabel=label, olb =self.labelBackground, 
                         olc=self.labelColour, annotation = annotation)
        
    def add_separator(self):
        '''Adds a shelf button with the specified label, command, double click 
        command and image.'''
        cmds.setParent(self.name)
        cmds.shelfButton(width= 37, height= 37, image= "spacer.png", l= "", 
                         olb =self.labelBackground, olc=self.labelColour)

    def add_sub_separator(self):
        '''Adds separator in the menu list.'''
        cmds.setParent(self.name)
        cmds.menuItem( divider=True )

    def add_menu_item(self, parent, label, command =_null, icon = ""):
        '''Adds a shelf button with the specified label, command, double click 
        command and image.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p= parent, l=label, c=command, i=icon, tearOff= 1)


    def _disabled_add_menu_item(self, parent, label, command =_null, icon = ""):
        '''Disabled menu'''
        return cmds.menuItem(p= parent, l=label, tearOff= 1, enable=False)

    def add_sub_menu(self, parent, label, icon =None):
        '''Adds a sub menu item with the specified label and icon to the 
        specified parent popup menu.'''
        if icon:
            icon = self.iconPath + icon
        return cmds.menuItem(p= parent, l=label, i=icon, subMenu= 1, tearOff= 1)

    def clean_old_shelf(self):
        '''Checks if the shelf exists and empties it if it does or creates it 
        if it does not.'''
        if cmds.shelfLayout(self.name, ex= 1):
            if cmds.shelfLayout(self.name, q= 1, ca= 1):
                for each in cmds.shelfLayout(self.name, q= 1, ca= 1):
                    cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p= "ShelfLayout")
            
    
