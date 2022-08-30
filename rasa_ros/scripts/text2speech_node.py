#!/usr/bin/env python
import sys
# sys.path.append('/home/klaudia/pyonoqi/lib//python2.7/site-packages')
sys.path.append('./pyonoqi')
from naoqi import ALProxy
from optparse import OptionParser
from pepper_nodes.srv import *
import rospy



class Text2SpeechNode:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.tts = ALProxy("ALTextToSpeech", ip, port)
        

    def say(self, msg):
        try:
            self.tts.say(msg.speech)
        except:
            self.tts = ALProxy("ALTextToSpeech", self.ip, self.port)
            self.tts.say(msg.speech)
        return "ACK"
    
    def start(self):
        rospy.init_node("text2speech_node")
        rospy.Service('tts', Text2Speech, self.say)

        rospy.spin()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()

    try:
        ttsnode = Text2SpeechNode(options.ip, int(options.port))
        ttsnode.start()
    except rospy.ROSInterruptException:
        pass