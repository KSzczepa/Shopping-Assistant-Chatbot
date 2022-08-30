#!/usr/bin/env python3

import rospy
from std_msgs.msg import String, Int8
import numpy as np

class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 


#Variables
global users
users = []
shop_lists = []
nested_dict = my_dictionary()
global last_name
last_name = "Undefined"


#Init node
rospy.init_node('main_fcn', anonymous=True)

user_activate = rospy.Publisher('user_new_data', String, queue_size=10)
dialog_activate = rospy.Publisher('dialogue_activ', String, queue_size=10)



def user_callback(name, pub_flag):
    global last_name, users
    if name == 'None':   
        pass
        
    elif name == "Undefined":
        if pub_flag == True:
            user_activate.publish(name)

    else: #received name

        if not name in users and name != "Undefined":
            users.append(name)        

        if pub_flag == True:
            user_activate.publish(name)

    return name
    


def main():   

    # rospy.wait_for_service('dialogue_server')

    while not rospy.is_shutdown():
      
        spoken_text = rospy.wait_for_message("voice_txt",String)
        username = rospy.wait_for_message("username",String)
        pub_flag = False
        activ_name = user_callback(username.data, pub_flag)     

        if activ_name != 'None' and activ_name != 'Undefined':
            msg_to_chatbot = activ_name + ': ' + spoken_text.data
        else:
            msg_to_chatbot = spoken_text.data

        # print(msg_to_chatbot)
        dialog_activate.publish(msg_to_chatbot)

        #wait for a message from chatbot
        chatbot_response = rospy.wait_for_message("new_username_chatbot", String)
        # rospy.loginfo("main: received username\'s name from chatbot")
        pub_flag = True
        activ_name = user_callback(chatbot_response.data, pub_flag)

        


if __name__ == '__main__':
    main()