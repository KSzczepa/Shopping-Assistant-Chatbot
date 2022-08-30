#!/usr/bin/env python


from naoqi import ALProxy
from optparse import OptionParser
from pepper_nodes.srv import *
import rospy




class Speech2TextNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.stt = ALProxy("ALSpeech2Text", ip, port)
        

    def listen(self):
        try:
            voice_msg = self.stt.listen()
            print(voice_msg)
        except:
            self.stt = ALProxy("ALTextToSpeech", self.ip, self.port)
            voice_msg = self.stt.listen()
            print(voice_msg)

        return "ACK"
    
    def start(self):
        rospy.init_node("speech2text_node")
        rospy.Service('stt', Speech2Text, self.listen)

        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        sttnode = Speech2TextNode(options.ip, int(options.port))
        sttnode.start()
    except rospy.ROSInterruptException:
        pass