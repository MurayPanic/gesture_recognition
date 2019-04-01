import cv2
import numpy as np
import math
from scipy.stats import chisquare

def dist(a,b):
    """
    This function is used to calculate the ABSOLUTE distance
    between two points given their coordinate. Please restore
    the coordinates of the point using list
    """
    try:
        distance=math.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

    except TypeError:
        print('Please input the coordinates of the points using list. for example dist([1,0],[0,1])')
    else:
        return distance

def angle_pos(a,b):
    """
    This function is used to calculate the angle position of b given the
    orign a.Please restore the coordinates of the point using list or np array
    This function is restricted to return positive result
    """
    try:
        ax = a[0]
        ay = a[1]
        bx = b[0]
        by = b[1]

        delta_x = bx-ax
        delta_y = by-ay

        if delta_x>0:
            slope = delta_y/delta_x
            theta = math.atan(slope)
        elif ( delta_x<0 and delta_y>=0):
            slope = delta_y/delta_x
            theta = math.atan(slope)+ math.pi
        elif (delta_x<0 and delta_y<0):
            slope = delta_y/delta_x
            theta = math.atan(slope)- math.pi
        elif (delta_x==0 and delta_y>0):
            theta = math.pi/2
        elif (delta_x==0 and delta_y<0):
            theta = -math.pi/2
        elif (delta_x==0 and delta_y==0):
            theta=0
        
    except TypeError:
        print('Please input the coordinates of the points using list. for example dist([1,0],[0,1])')    
    else:
        if theta<0:
            return theta + 2*math.pi
        else:
            return theta

def cal_line(a,b):
    """
    This function is to calculate the line equation qiven
    the coordinates of two points
    The return of this function is the coefficient of the
    line equatin Ax + By + C =0
    note that the line has direction which is from a to b
    """
    try:
        x_1 = a[0]
        y_1 = a[1]
        x_2 = b[0]
        y_2 = b[1]
        
        A = y_2 - y_1
        B = x_1 - x_2
        C = x_2 * y_1 - x_1 * y_2

        


        
    except TypeError:
        print('Please input the coordinates of the points using list. for example dist([1,0],[0,1])')    
    else:

        return [A, B, C]

def height_point_line(point, line_coeff):
    """
    This function calculate the distance betwen a point and a straight line
    Please input the point coordinates using lists
    Please input the line equation coefficents using list.
    The line has direction.
    The point which is on the left hand side of the line is given a positive height
    where those on the right hand side  is given a negative height
    """
    try:
        A = line_coeff[0]
        B = line_coeff[1]
        C = line_coeff[2]
        denominator = math.sqrt(A**2 + B**2)
        numerator = - (  A* point[0] + B* point[1] + C)
        dist = numerator / denominator
    

    except TypeError:
        print('Please input the point and the equatiion coefficents using list')
    else:
        return dist

def mid_point(point_a, point_b):
    """
    This function return the midpoint coordinates
    """
    x_a = point_a[0]
    y_a = point_a[1]
    x_b = point_b[0]
    y_b = point_b[1]

    x_mid = (x_a + x_b) /2
    y_mid = (y_a + y_b) /2

    return [x_mid, y_mid]


def dist_point_line(point, line_coeff):
    """
    This function calculate the abosolute distance betwen a point and a straight line
    Please input the point coordinates using lists
    Please input the line equation coefficents using list.
    The line has no direction.
    """
    try:
        A = line_coeff[0]
        B = line_coeff[1]
        C = line_coeff[2]
        denominator = math.sqrt(A**2 + B**2) +np.finfo(float).eps 
        numerator = abs (  A* point[0] + B* point[1] + C) 
        dist = numerator / denominator
    except TypeError:
        print('Please input the point and the equatiion coefficents using list')
    else:
        return dist

def perpendicular_foot(point, line_coeff):
    """
    This function return the perpendicular foot
    given a line and a point
    """
    
    A = line_coeff[0]
    B = line_coeff[1]
    C = line_coeff[2]

    x = (B*B * point[0] - A*B* point[1] - A*C) / (A**2 + B**2+np.finfo(float).eps )
    y = (-A*B * point[0] + A*A* point[1] - B*C) / (A**2 + B**2+np.finfo(float).eps )

    return [x,y]



    
