#!/usr/bin/env python

import argparse
import rospy
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import Twist
from control_msgs.msg import JointJog

TwistMsg = Twist
joint_deltas = JointJog
NODENAME = 'leap_data'

def callback_ros(msg):
    msg = leapros()

def leap_to_twist():
    li =leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    rospy.init_node(NODENAME)
    rospy.Subscriber("leapmotion/data", leapros, callback_ros)
    leap_pub = rospy.Publisher('servo_server/delta_twist_cmds',TwistMsg,queue_size=1)
    joint_delta_pub= rospy.Publisher('servo_server/delta_joint_cmds',JointJog,queue_size=1)
    rate = rospy.Rate(60)
    twist_msg = TwistMsg()
    twist = twist_msg
    while not rospy.is_shutdown():
        #get palm position and orientation
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        
        twist.linear.x = hand_palm_pos_[0]
        twist.linear.y = hand_palm_pos_[1]
        twist.linear.z = hand_palm_pos_[2]
        twist.angular.x = hand_pitch_
        twist.angular.y = hand_yaw_
        twist.angular.z = hand_roll_
        
        joint_delta_pub.publish(joint_deltas)       
        leap_pub.publish(twist)
        rate.sleep()
    
 

if __name__ == '__main__':
    try:
        leap_to_twist()
    except rospy.ROSInterruptException:
        pass
