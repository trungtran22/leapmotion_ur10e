#!/usr/bin/env python

import argparse
import rospy
import leap_interface
from geometry_msgs.msg import Twist
from control_msgs.msg import JointJog
from sensor_msgs.msg import Joy

TwistMsg = Twist
joint_deltas = JointJog
NODENAME = 'leap_data'

def leap_publishing():
    li =leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    leap_pub = rospy.Publisher('servo_server/cmd_vel',TwistMsg,queue_size=1)
    joint_delta_pub= rospy.Publisher('servo_server/delta_joint_cmds',JointJog,queue_size=1)
    joy_sub = rospy.Subscriber('leap/joy',leap_publishing(),queue_size=1)
    rospy.init_node(NODENAME)
    rate = rospy.Rate(60)
    twist_msg = TwistMsg()
    twist = twist_msg

    while not rospy.is_shutdown():
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
        
        
        leap_pub.publish(twist_msg)
        rate.sleep()
 

if __name__ == '__main__':
    try:
        leap_publishing()
    except rospy.ROSInterruptException:
        pass
