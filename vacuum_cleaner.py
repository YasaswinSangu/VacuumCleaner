#!/usr/bin/env python
# license removed for brevity

import rospy
import math
import time
from geometry_msgs.msg import Twist
class VacuumCleaner:

    
    
# This method is to initialize the environment
    def __init__(self,maxX_p,maxY_p,side_p,radius_p,cube_centre_p,cylinder_centre_p,positive_y_p):
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.init_node('path_instructor', anonymous=True)
        self.rot=Twist()
        self.maxX=maxX_p
        self.maxY=maxY_p
        self.side=side_p
        a=int(self.side/2)
        area_square=self.side*self.side
        self.radius=radius_p
        area_cyl= 4*self.radius*self.radius
        self.cube_centre=cube_centre_p
        self.cylinder_centre=cylinder_centre_p
        self.current_vertical=1
        self.current_horizontal=1
        self.back_cnt=0
        self.positive_y=positive_y_p
        self.moves=[]
        self.moves_complete=[]
        self.grids_covered= []
        self.grids_to_cover= ((self.maxX*self.maxY)-(area_square*(len(self.cube_centre)))-(area_cyl*(len(self.cylinder_centre))))
        print(self.grids_to_cover)
        self.forbidden=[[-1]*(self.maxX+2) for _ in range((self.maxY+2))]
        for i in range(0,(int(self.maxX)+2)):
            self.forbidden[0].pop(0)
            self.forbidden[0].append(int(i))
            self.forbidden[int(self.maxY)+1].pop(0)
            self.forbidden[int(self.maxY)+1].append(int(i))
        for i in range(0,self.maxY+2):
            self.forbidden[i].pop(0)
            self.forbidden[i].append(0)
            self.forbidden[i].pop(0)
            self.forbidden[i].append((self.maxY)+1)
        self.forbidden[0].remove((self.maxY)+1)
        self.forbidden[0].append(1)
        self.forbidden[(self.maxY)+1].remove((self.maxY)+1)   
        self.forbidden[(self.maxY)+1].append(1) 
        for l in self.cube_centre:
            for m in range(int(l[1])-a,(int(l[1])+(a-1)+1)):
                for k in range(int(l[0])-a,(int(l[0])+(a-1)+1)):
                    self.forbidden[m].pop(0)
                    self.forbidden[m].append(k)
        for l in self.cylinder_centre:
            for m in range(int(l[1])-self.radius,(int(l[1])+(self.radius-1)+1)):
                for k in range(int(l[0])-self.radius,(int(l[0])+(self.radius-1)+1)):
                    self.forbidden[m].pop(0)
                    self.forbidden[m].append(k)  
         
# This function checks if a robot can make a left turn or not            
    def left_is_free(self):
        if (self.current_horizontal-1) in self.forbidden[self.current_vertical]:
            return False
        else:
            return True

# This function checks if a robot can make a right turn or not
    def right_is_free(self):
        if (self.current_horizontal+1) in self.forbidden[self.current_vertical]:
            return False
        else:
            return True

# This function checks if a robot can go up or not
    def up_is_free(self):
        if (self.current_horizontal) in self.forbidden[self.current_vertical+1]:
            return False
        else:
            return True

# This function checks if a robot can go down or not
    def down_is_free(self):
        if (self.current_horizontal) in self.forbidden[self.current_vertical-1]:
            return False
        else:
            return True                      
                
# This method is for moving the robot around
    def move(self,direction):
        self.forbidden[self.current_vertical].pop(0)    
        self.forbidden[self.current_vertical].append(self.current_horizontal) 
        self.moves.append([self.current_horizontal,self.current_vertical])
        self.moves_complete.append([self.current_horizontal,self.current_vertical])
        for i in range(self.back_cnt):
            self.moves[-1-i].pop()
            self.moves[-1-i].pop(0)
        self.back_cnt=0
        if(direction=='U'):
            self.current_vertical+=1
            self.rot.linear.x=0.2
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(5)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5) 
        elif(direction=='D'):
            self.current_vertical-=1
            self.rot.linear.x= -(0.2)
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(5)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)
        elif(direction=='L'):
            self.current_horizontal-=1
            self.rot.linear.x= (0.0)
            self.rot.angular.z= (0.5)
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(math.pi)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)
            self.rot.linear.x= (0.2)
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(5)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)
            self.rot.linear.x= (0.0)
            self.rot.angular.z= -(0.5)
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(math.pi)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)

        elif(direction=='R'):
            self.current_horizontal+=1
            self.rot.linear.x= (0.0)
            self.rot.angular.z= -(0.5)
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(math.pi)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)
            self.rot.linear.x= (0.2)
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(5)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5)
            self.rot.linear.x= (0.0)
            self.rot.angular.z= (0.5)
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(math.pi)
            self.rot.linear.x=0.0
            self.rot.angular.z=0.0
            rospy.loginfo(self.rot)
            self.pub.publish(self.rot)
            time.sleep(0.5) 
        
#This method is to plan the next moves
    def plan_move(self):
        if self.positive_y:
            if self.left_is_free():
                self.move('L')                                                                                  
            elif self.up_is_free():
                self.move('U')
            elif self.down_is_free():
                self.move('D')
                self.positive_y = not self.positive_y    
            elif self.right_is_free():
                self.move('R')
                self.positive_y = not self.positive_y
            else:
                self.back_track()
        else:
            if self.left_is_free():
                self.move('L')
            elif self.down_is_free():
                self.move('D')
            elif self.up_is_free():
                self.move('U')
                self.positive_y = not self.positive_y
            elif self.right_is_free():
                self.move('R')
                self.positive_y = not self.positive_y
            else:
                self.back_track()
        
            
# This function helps the robot to trace back it's steps in-case it gets stuck somewhere
    def back_track(self):
        if self.back_cnt==0:
            self.forbidden[self.current_vertical].pop(0)   
            self.forbidden[self.current_vertical].append(self.current_horizontal)
        horizontal_back_track= self.moves[-1-self.back_cnt][0]- self.current_horizontal
        vertical_back_track= self.moves[-1-self.back_cnt][1]-self.current_vertical
        self.moves_complete.append([self.current_horizontal,self.current_vertical])
        if horizontal_back_track:
            if horizontal_back_track==1:
                self.current_horizontal+=1
                self.rot.linear.x= (0.0)
                self.rot.angular.z= -(0.5)
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(math.pi)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5)
            	self.rot.linear.x= (0.2)
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(5)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5)
            	self.rot.linear.x= (0.0)
            	self.rot.angular.z= (0.5)
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(math.pi)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5) 

            else:
                self.current_horizontal-=1
                self.rot.linear.x= (0.0)
            	self.rot.angular.z= (0.5)
           	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(math.pi)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
           	self.pub.publish(self.rot)
           	time.sleep(0.5)
           	self.rot.linear.x= (0.2)
           	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
          	time.sleep(5)
          	self.rot.linear.x=0.0
           	self.rot.angular.z=0.0
           	rospy.loginfo(self.rot)
          	self.pub.publish(self.rot)
            	time.sleep(0.5)
            	self.rot.linear.x= (0.0)
            	self.rot.angular.z= -(0.5)
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(math.pi)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5)

        else:
            if vertical_back_track==1:
                self.current_vertical+=1 
                self.positive_y= not self.positive_y
                self.rot.linear.x=0.2
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(5)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5)  

            else:
                self.current_vertical-=1 
                self.positive_y= not self.positive_y
                self.rot.linear.x= -(0.2)
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(5)
            	self.rot.linear.x=0.0
            	self.rot.angular.z=0.0
            	rospy.loginfo(self.rot)
            	self.pub.publish(self.rot)
            	time.sleep(0.5)

        self.back_cnt+=1      
        

def main():                                                           # Change the first 6 variables of this method according to your map
    maxX_p = 4                                                      # Maximum X-Dimension of map
    maxY_p = 6                                                       # Maximum Y-Dimension of map        
    side_p = 1                                                       # length of side of cube 
    radius_p = 1                                                      # radius of cylinder 
    cube_centre_p =  [[3.0,4.0],[2.0,1.0]]                            # List of co-ordinates of cubes 
    cylinder_centre_p = [[1.0,4.0]]                      # List of co-ordinates of cylinder    
    positive_y_p = True 
    obj=VacuumCleaner(maxX_p,maxY_p,side_p,radius_p,cube_centre_p,cylinder_centre_p,positive_y_p)
    while len(obj.grids_covered) < obj.grids_to_cover-1:
        if [obj.current_horizontal,obj.current_vertical] not in obj.grids_covered:
            obj.grids_covered.append([obj.current_horizontal,obj.current_vertical])
        obj.plan_move()
         
    obj.moves.append([obj.current_horizontal,obj.current_vertical])
    obj.moves_complete.append([obj.current_horizontal,obj.current_vertical])
    print(obj.moves_complete)
main()    
        
#def talker(self):
 #   self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
  #  rospy.init_node('path_instructor', anonymous=True)
   # self.rot=Twist()
    #main()
    #self.rot.linear.x=0.22
    #self.rot.angular.z=0.4
    #rospy.loginfo(rot)
    #self.pub.publish(rot)
    
 
#if __name__ == '__main__':
#    try:
#        talker()
 #   except rospy.ROSInterruptException:
 #       pass
