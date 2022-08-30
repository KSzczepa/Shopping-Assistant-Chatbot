#!/usr/bin/env python

import os
print(os.environ["PYTHONPATH"])

from naoqi import ALProxy
from optparse import OptionParser
from pepper_nodes.srv import *
import rospy

class WakeUpNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.motion_proxy = ALProxy("ALMotion", ip, port)
        self.posture_proxy = ALProxy("ALRobotPosture", ip, port)

    def rest(self, *args):
        try:
            self.motion_proxy.rest()
        except:
            self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            self.motion_proxy.rest()
        return "ACK"

    def wakeup(self, *args):
        try:
            self.motion_proxy.wakeUp()
            self.stand()
        except:
            self.motion_proxy = ALProxy("ALMotion", self.ip, self.port)
            self.posture_proxy = ALProxy("ALRobotPosture", self.ip, self.port)
            self.motion_proxy.wakeUp()
            self.stand()         

        return "ACK"   

    def stand(self, *args):
        self.posture_proxy.goToPosture("StandInit", 0.5)

    def start(self):
        rospy.init_node("wakeup_node")
        self.wakeup()
        self.stand()        
        rospy.Service("wakeup", WakeUp, self.wakeup)
        rospy.Service("rest", Rest, self.rest)
        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = WakeUpNode(options.ip, int(options.port))
        node.start()
    except rospy.ROSInterruptException:
        pass
