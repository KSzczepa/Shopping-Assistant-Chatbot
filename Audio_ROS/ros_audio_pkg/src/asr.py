#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, String, Int16
import numpy as np
# from multiprocessing import Process, Pipe
# import multiprocessing
# from multiprocessing import Lock

from speech_recognition import AudioData
import speech_recognition as sr

# Initialize a Recognizer
r = sr.Recognizer()

# Init node
rospy.init_node('speech_recognition', anonymous=True)
pub1 = rospy.Publisher('voice_data', Int16MultiArray, queue_size=1)
pub2 = rospy.Publisher('voice_txt', String, queue_size=1)
dialog_flag = rospy.Publisher('voice_listening', Int16, queue_size=10)
# rate = rospy.Rate(1) # 1hz



# this is called from the background thread
def callback(audio):
    global voice_msg_to_send
    data = np.array(audio.data,dtype=np.int16)
    audio_data = AudioData(data.tobytes(), 16000, 2)
    rospy.loginfo("asr: received voice data from mic")

    try:
        spoken_text= r.recognize_google(audio_data, language='en-GB')
        
        pub1.publish(audio) # Publish audio only if it contains words   
        pub2.publish(spoken_text)

        flag = 0
        dialog_flag.publish(flag)
       
        rospy.loginfo("asr: received audio")

    except sr.UnknownValueError:
        rospy.loginfo("asr: cannot understand words")
        # print("Google Speech Recognition cannot understand from this audio file")
        # print("Try again")
        # pass
    except sr.RequestError as e:
        rospy.loginfo("asr: request error occured")
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
        pass

def listener():
    rospy.Subscriber("mic_data", Int16MultiArray, callback)
    rospy.wait_for_message('return_to_listen', Int16)
    # rospy.loginfo("asr: received flag return to listen")

    rospy.spin()

if __name__ == '__main__':
    # rospy.wait_for_service('dialogue_server')
    listener()