#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
import numpy as np


class Nodo(object):
    def __init__(self):
        # Params
        self.br = CvBridge()

    def callback(self, msg):
        image = self.br.imgmsg_to_cv2(msg)
        cv2.imshow("Pepper Camera", image)
        cv2.waitKey(50)

    def start(self):
        # Subscriber
        rospy.Subscriber("/in_rgb", Image, self.callback)

        rospy.spin()


if __name__ == '__main__':
    rospy.init_node("camera_show_node", anonymous=True)
    my_node = Nodo()
    my_node.start()
