#!/usr/bin/env python

import argparse
import rospy
import leap_interface
from geometry_msgs.msg import TwistStamped

TwistMsg = TwistStamped
NODENAME = 'leap_data'
leap_start = 0.02
leap_end = 0.55
app_start = -0.5
app_end = 0.5
leap_range = leap_start - leap_end
app_range = app_start - app_end

def mapping(x):
    #mapping between leap motion value and application value in this case is ur10e cmd_vel
    return (x - leap_start)*(leap_range/app_range) +app_start
    
def leap_to_twist():
    li =leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    rospy.init_node(NODENAME)
    leap_pub = rospy.Publisher('servo_server/delta_twist_cmds',TwistMsg,queue_size=1)
    rate = rospy.Rate(60)
    twist_msg = TwistMsg()
    twist = twist_msg
    while not rospy.is_shutdown():
            #get palm position
            hand_palm_pos_= li.get_hand_palmpos()
        
            #map leap data to robot arm working space
            hand_palm_pos_x_ = mapping(round(hand_palm_pos_[0]*(10**(-2)),2))
            hand_palm_pos_y_ = mapping(round(hand_palm_pos_[1]*(10**(-2)),2))
            hand_palm_pos_z_ = mapping(round(hand_palm_pos_[2]*(10**(-2)),2))
        
            #round data to 2 digits
            hand_palm_pos_x = round(hand_palm_pos_x_,2)
            hand_palm_pos_y = round(hand_palm_pos_y_,2)
            hand_palm_pos_z = round(hand_palm_pos_z_,2)
             
             #exceed limit, stream velocity = 0
            if hand_palm_pos_x > 0.5 or hand_palm_pos_x < -0.5:
                hand_palm_pos_x = 0
                hand_palm_pos_y = 0
                hand_palm_pos_z = 0
                
            
            if hand_palm_pos_y > 0.5 or hand_palm_pos_y < -0.5:
                hand_palm_pos_x = 0
                hand_palm_pos_y = 0
                hand_palm_pos_z = 0
                
            
                
            if hand_palm_pos_z > 0.5 or hand_palm_pos_z < -0.5:
                hand_palm_pos_x = 0
                hand_palm_pos_y = 0
                hand_palm_pos_z = 0
                   
	

            twist.twist.linear.x = hand_palm_pos_x
            twist.twist.linear.y = hand_palm_pos_z
            twist.twist.linear.z = hand_palm_pos_y
            #fix angular value
            twist.twist.angular.x = 0
            twist.twist.angular.y = 0
            twist.twist.angular.z = 0
        
            leap_pub.publish(twist)
            rate.sleep()
            

    

if __name__ == '__main__':
    try:
        leap_to_twist()
    except rospy.ROSInterruptException:
        pass
