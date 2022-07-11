#!/usr/bin/env python
import nuke
import array, os, random, subprocess

class create_write_nodes (object):

    def __init__(self):

        def deselectAll():
            ########################Deselect All Nodes#########################
            all = nuke.allNodes()
            for node in all:
                node.knob('selected').setValue(False)
        
      
        string = ""
        other = ""
        dot = ""
        xPos = 1700
        yPos = 8000
        increment = 55

        views = nuke.views() #Save Views
        viewsTrue = []       #Set Variable for True Views
        viewsFalse = []      #Set Variable for False Views
        valueTrue = []       #Set Variable for True List
        valueFalse = []      #Set Variable for False List
        viewsValue = ""      #Set Variable for Final Views List to Write Node
        deselectAll()
        
        
        
        #############Panel for Categories############# 
        p = nuke.Panel("Select Category")
        p.addButton("Badges")
        p.addButton("Accessories")
        p.addButton("Wheels")
        p.addButton("Paint")
        result = p.show()
        
        other = p.value("Search For:")
        
        #############Find views by Category#############
        
        
        ##Badges
        if result == 0:
            for e in views:
                string = str.startswith(e,"B")
                stringStrip = e.lstrip('B_')
                if string == True:
                    dot = nuke.createNode("Dot")
                    dot.knob("xpos").setValue(xPos)
                    dot.knob("name").setValue("Dot_" + e)
                    dot.knob("xpos").setValue(xPos-300)
                    dot.knob("ypos").setValue(yPos)

                    writeNode = nuke.createNode("Write")
                    writeNode.knob("name").setValue("WriteNode_" + e)
                    writeNode.knob("file").setValue("[value root.PSD]/[value root.Filename]_1xx_f%02d_" + stringStrip +".exr")
                    writeNode.knob("channels").setValue("rgba")
                    writeNode.knob("metadata").setValue("all metadata")
                    writeNode.knob("file_type").setValue("exr")
                    writeNode.knob("xpos").setValue(xPos)
                    writeNode.knob("ypos").setValue(yPos-10)
                    writeNode.knob("views").setValue(e)
                    writeNode.knob("selected").setValue(False)
                    yPos = yPos + increment
        
        
        ##Accessories
        if result == 1:
            for e in views:
                string = str.startswith(e,"A_")
                stringStrip = e.lstrip('A_')
                print(stringStrip)
                if string == True:
                    dot = nuke.createNode("Dot")
                    dot.knob("xpos").setValue(xPos)
                    dot.knob("name").setValue("Dot_" + e)
                    dot.knob("xpos").setValue(xPos-300)
                    dot.knob("ypos").setValue(yPos)
        
                    writeNode = nuke.createNode("Write")
                    writeNode.knob("name").setValue("WriteNode_" + e)
                    writeNode.knob("file").setValue("[value root.PSD]/[value root.Filename]_1xx_f%02d_" + stringStrip +".exr")
                    writeNode.knob("channels").setValue("rgba")
                    writeNode.knob("file_type").setValue("exr")
                    writeNode.knob("metadata").setValue("all metadata")
                    writeNode.knob("xpos").setValue(xPos)
                    writeNode.knob("ypos").setValue(yPos-10)
                    writeNode.knob("views").setValue(e)
                    writeNode.knob("selected").setValue(0)
                    dot.knob("selected").setValue(0)
                    yPos = yPos + increment
        
        ##Wheels
        if result == 2:
            for e in views:
                string = str.startswith(e,"W")
                stringStrip = e.lstrip('W_')
                if string == True:
                    dot = nuke.createNode("Dot")
                    dot.knob("xpos").setValue(xPos)
                    dot.knob("name").setValue("Dot_" + e)
                    dot.knob("xpos").setValue(xPos-300)
                    dot.knob("ypos").setValue(yPos)
        
                    writeNode = nuke.createNode("Write")
                    writeNode.knob("name").setValue("WriteNode_" + e)
                    writeNode.knob("file").setValue("[value root.PSD]/[value root.Filename]_1xx_f%02d_" + stringStrip +".exr")
                    writeNode.knob("channels").setValue("rgba")
                    writeNode.knob("file_type").setValue("exr")
                    writeNode.knob("metadata").setValue("all metadata")
                    writeNode.knob("xpos").setValue(xPos)
                    writeNode.knob("ypos").setValue(yPos-10)
                    writeNode.knob("views").setValue(e)
                    writeNode.knob("selected").setValue(0)
                    dot.knob("selected").setValue(0)
                    yPos = yPos + increment



        ##Paint
        if result == 3:
            for e in views:
                string = str.startswith(e,"P")
                stringStrip = e.lstrip('P_')
                if string == True:
                    dot = nuke.createNode("Dot")
                    dot.knob("xpos").setValue(xPos)
                    dot.knob("name").setValue("Dot_" + e)
                    dot.knob("xpos").setValue(xPos-300)
                    dot.knob("ypos").setValue(yPos)
        
                    writeNode = nuke.createNode("Write")
                    writeNode.knob("name").setValue("WriteNode_" + e)
                    writeNode.knob("file").setValue("[value root.PSD]/[value root.Filename]_1xx_f%02d_" + stringStrip + ".exr")
                    writeNode.knob("channels").setValue("rgba")
                    writeNode.knob("file_type").setValue("exr")
                    writeNode.knob("metadata").setValue("all metadata")
                    writeNode.knob("xpos").setValue(xPos)
                    writeNode.knob("ypos").setValue(yPos-10)
                    writeNode.knob("views").setValue(e)
                    writeNode.knob("selected").setValue(0)
                    dot.knob("selected").setValue(0)
                    yPos = yPos + increment
