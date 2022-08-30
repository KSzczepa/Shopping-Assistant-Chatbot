#!/usr/bin/env python3

import rospy
from rasa_ros.srv import Dialogue, DialogueResponse
from std_msgs.msg import Int16MultiArray, String, Int16
import numpy as np
# from naoqi import ALProxy


from speech_recognition import AudioData
import speech_recognition as sr

import os


# Initialize a Recognizer
r = sr.Recognizer()

#Init node
rospy.init_node('writting', anonymous=True)

main_out = rospy.Publisher('bot_finished', String, queue_size=10)

dialog_flag = rospy.Publisher('voice_listening', Int16, queue_size=10)


class TerminalInterface:
    '''Class implementing a terminal i/o interface. 

    Methods
    - get_text(self): return a string read from the terminal
    - set_text(self, text): prints the text on the terminal

    '''

    def get_text(self):
        return input("[IN]:  ") 

    def set_text(self,text):
        print("[OUT]:",text)



def main():

    rospy.wait_for_service('dialogue_server')
    dialogue_service = rospy.ServiceProxy('dialogue_server', Dialogue)
    print('You can speak now')
    # msg_in = f"rosservice call /tts \"You can speak now\""
    # os.system(msg_in)
    flag_start = 1
    dialog_flag.publish(flag_start)

    
    while not rospy.is_shutdown():
        
        spoken_text = rospy.wait_for_message("dialogue_activ",String) 
        # string = f'dialog_interface {rospy.get_time()}'
        # rospy.loginfo(string)

        flag_start = 0
        dialog_flag.publish(flag_start)        
         
        message = str("[IN]: " + spoken_text.data)
        print(message)
        if message == 'exit': 
            break
        try:
            bot_answer = dialogue_service(message)
            terminal = TerminalInterface()  
            terminal.set_text(bot_answer.answer)

            # msg = f"rosservice call /tts \"{bot_answer.answer}\""
            # os.system(msg)
            
            flag_start = 1
            dialog_flag.publish(flag_start)
            
            
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)
        
     




if __name__ == '__main__':
    try: 
        main()
    except rospy.ROSInterruptException:
        pass