#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np

def callback(data):
    en = np.mean(np.array(data.data)**2)**0.5

    en_ticks = min(int(max(0,5*np.log10(en))),30)
    space_ticks = 30-en_ticks
    print('RMS> '+('#'*en_ticks)+(' '*space_ticks)+"%.2f"%en,end='\r')
    
def listener():
    rospy.init_node('microphone_listener', anonymous=True)
    rospy.Subscriber("mic_data", Int16MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()