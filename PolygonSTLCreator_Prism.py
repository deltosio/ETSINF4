###############################
#    Ángel Pérez González     #
#        ETSINF  UPV          #
#         DM3D 2022           #
###############################

from math import cos, pi, sin
import os
import numpy as np


def rotX(theta):
    return np.array([[1, 0, 0],[ 0, cos(theta), -sin(theta)],[ 0, sin(theta), cos(theta)]])

def rotY(theta):
    return np.array([[cos(theta), 0, sin(theta)],[ 0, 1, 0],[ -sin(theta), 0, cos(theta)]])

def rotZ(theta):
    return np.array([[cos(theta), -sin(theta), 0],[ sin(theta), cos(theta), 0],[ 0, 0, 1]])

def normalCalc(p1,p2,p3):
    v1 = [p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2]]
    v2 = [p1[0] - p3[0], p1[1] - p3[1], p1[2] - p3[2]]
    vector = np.cross(v1,v2)
    return vector

def facetWrite(normal, p1, p2, p3):
    file.write("facet normal " + str(normal[0]) + " " + str(normal[1]) + " " + str(normal[2]) + os.linesep)
    file.write("\touter loop"+  os.linesep)
    file.write("\t\tvertex " + str(p1[0]) + " " + str(p1[1])+ " " + str(p1[2])+  os.linesep)
    file.write("\t\tvertex " + str(p2[0]) + " " + str(p2[1])+ " " + str(p2[2])+  os.linesep)
    file.write("\t\tvertex " + str(p3[0]) + " " + str(p3[1])+ " " + str(p3[2])+  os.linesep)
    file.write("\tendloop" + os.linesep)
    file.write("endfacet" + os.linesep)

def portionCalc(sides, i, length, height, rotationX, rotationY):
    
    #Grad to radians for the rotation matrix
    thetaZ = (((-360/sides)) * (pi/180)) 
    
    thetaX = rotationX * (pi/180)
    thetaY = rotationY * (pi/180)
    #Rotation matrix
    R = rotZ(thetaZ)
    
    #Calculus of the radio for the circumscribed circle with the length of the side
    radio = length/(2*sin(-thetaZ/2))

    #Primary points for the calculus
    p00 = [0,0,0]
    p01 = [0,0,height]
    p10 = [radio,0,0] 
    p20 = p10 @ R
    p11 = [radio,0,height]
    p21 = p11 @ R

    #Rotation of primary points to do the other portions
    for j in range(i):
        p10 = p10 @ R
        p20 = p20 @ R 
        p11 = p11 @ R
        p21 = p21 @ R

    if(thetaX != 0 and thetaY != 360):
        p00 = p00 @ rotX(thetaX)
        p01 = p01 @ rotX(thetaX)
        p10 = p10 @ rotX(thetaX)
        p20 = p20 @ rotX(thetaX) 
        p11 = p11 @ rotX(thetaX)
        p21 = p21 @ rotX(thetaX)

    if(thetaY != 0 and thetaY != 360 ):
        p00 = p00 @ rotY(thetaY)
        p01 = p01 @ rotY(thetaY)
        p10 = p10 @ rotY(thetaY)
        p20 = p20 @ rotY(thetaY) 
        p11 = p11 @ rotY(thetaY)
        p21 = p21 @ rotY(thetaY)

    #Calculus of the normal vector for the facets
    normal11 = normalCalc(p10,p21,p11)
    normal22 = normalCalc(p20,p21,p10)
    normal00 = normalCalc(p00,p20,p10)
    normal01 = normalCalc(p01,p11,p21)

    #Write facet data on the file
    facetWrite(normal11,p10,p21,p11)
    facetWrite(normal22,p20,p21,p10)
    facetWrite(normal00,p00,p20,p10)
    facetWrite(normal01,p01,p11,p21)

def main():
    #Start menu
    print("Select number of sides (minimum 3): ")
    sides = int(input())
    while(sides < 3):
        print("Invalid number")
        print("Select number of sides (minimum 3): ")
        sides = int(input())
    print("Select the length of the side: ")
    length = float(input())
    while(length <= 0):
        print("Invalid number")
        print("Select the length of the side: ")
        length = float(input())

    print("Select the height of the prism: ")
    height = float(input())
    while(height <= 0):
        print("Invalid number")
        print("Select the height of the prism: ")
        height = float(input())
    print("Rotation on X (Deg 0-360): ")
    rotationX = float(input())
    while(rotationX < 0 or rotationX > 360):
        print("Rotation on X (Deg 0-360): ")
        rotationX = float(input())
    print("Rotation on Y (Deg 0-360): ")
    rotationY = float(input())
    while(rotationY < 0 or rotationY > 360):
        print("Rotation on X (Deg 0-360): ")
        rotationY = float(input())

    #Start of the STL file
    file.write("solid polygon"+str(sides)+"sides" + os.linesep)

    #Calculus of the points and normal vectors for the facets
    for i in range(sides) :
        portionCalc(sides, i, length, height, rotationX, rotationY)
    
    #End of the STL file
    file.write("endsolid")
    file.close()

#It creates the file on the same directory where you execute the program
file = open(".\polygon.stl", "w")
main()