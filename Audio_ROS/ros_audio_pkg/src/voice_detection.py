#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray, Int16
import numpy as np

import time
import speech_recognition as sr

pub = rospy.Publisher('mic_data', Int16MultiArray, queue_size=1)
rospy.init_node('voice_detection_node', anonymous=True)

global flag
flag = 0

def callback2(voice_flag):
    global flag
    flag = voice_flag.data

# this is called from the background thread
def callback(recognizer, audio):
    
    data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    data_to_send = Int16MultiArray()
    data_to_send.data = data
        
    global flag
    if flag != 0:
        pub.publish(data_to_send)
        string_msg = f"voice detection: i have sent data {flag}"
        rospy.loginfo(string_msg)
    else:
        string_msg = f"voice detection: i have not sent data {flag}"
        rospy.loginfo(string_msg)



# Initialize a Recognizer
r = sr.Recognizer()

# Audio source
m = sr.Microphone(device_index=None,
                    sample_rate=16000,
                    chunk_size=1024)

# Calibration within the environment
# we only need to calibrate once, before we start listening
print("Calibrating...")
with m as source:
    r.adjust_for_ambient_noise(source,duration=3)  
print("Calibration finished")


# start listening in the background
# `stop_listening` is now a function that, when called, stops background listening
print("Recording...")

rospy.Subscriber('voice_listening', Int16, callback2)

stop_listening = r.listen_in_background(m, callback)


rospy.spin()