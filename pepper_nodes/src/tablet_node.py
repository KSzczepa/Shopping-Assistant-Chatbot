#!/usr/bin/env python

from naoqi import ALProxy
from optparse import OptionParser
from pepper_nodes.srv import *
import rospy

class TabletNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tablet_proxy = ALProxy("ALTabletService", ip, port)
        self.tablet_proxy.resetTablet()

    def load_url(self, msg):
        try:
            self.tablet_proxy.showWebview(msg.url)
        except:
            self.tablet_proxy = ALProxy("ALTabletService", self.ip, self.port)
            self.tablet_proxy.showWebview(msg.url)
        return "ACK"

    def execute_js(self, msg):
        try:
            self.tablet_proxy.executeJS(msg.js)
        except:
            self.tablet_proxy = ALProxy("ALTabletService", self.ip, self.port)
            self.tablet_proxy.executeJS(msg.js)
            
        return "ACK"

    def start(self):
        rospy.init_node("tablet_node")

        rospy.Service('execute_js', ExecuteJS, self.execute_js)
        rospy.Service('load_url', LoadUrl, self.load_url)

        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        node = TabletNode(options.ip, int(options.port))
        node.start()
    except rospy.ROSInterruptException:
        pass
