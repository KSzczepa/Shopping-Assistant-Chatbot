#!/usr/bin/env python3


import rospy
from std_msgs.msg import String, Int8
#DO PUBLISHERA /\ /\ /\ /\ 
from logging import NullHandler, raiseExceptions
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, FollowupAction

from multiprocessing import Process, Queue, Pipe

from rasa_sdk.interfaces import NLU_FALLBACK_INTENT_NAME

import sys
from pathlib import Path
# base_path = Path(__file__).parent
# file_path = (base_path / "dict.py").resolve()


from actions.dict import my_dictionary
import os


#PUDLISHER
#Init node
rospy.init_node('chatbot_response', anonymous=True)
chatbot_response = rospy.Publisher('new_username_chatbot', String, queue_size=10)


BASKET = {}
USERS = []
shop_list = my_dictionary()


class ActionAdd(Action):
    def name(self) -> Text:
        return "action_receive_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product = tracker.get_slot("product")
        username = tracker.get_slot("username")

        if product == None:
            dispatcher.utter_message(text=f'I do not recognize the product!') 
            evt = FollowupAction(name= "utter_asistant")
            return [evt]

        shop_list.add(username, product)
        
        dispatcher.utter_message(text=f'Product {product} has been added to your shopping list!') 
        
        
        return [AllSlotsReset()]
       
                 
 
class ActionRemove(Action):
    def name(self) -> Text:
        return "action_remove_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        product = tracker.get_slot("product")
        username = tracker.get_slot("username")

        if product == None:
            #clear the whole list for this person
            out_msg = shop_list.remove(username)

        else:
            #delete only one product
            out_msg = shop_list.remove(username, product)
            dispatcher.utter_message(text=out_msg)        

        return [AllSlotsReset()]


class ActionShow(Action):
    def name(self) -> Text:
        return "action_show_basket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # product = tracker.get_slot("product")
        username = tracker.get_slot("username")

        out_msg = shop_list.show(username)
        dispatcher.utter_message(text=out_msg)  

        return [AllSlotsReset()]

    

class CheckUser(Action):
    def name(self) -> Text:
        return "check_user_existance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        
        if username == 'None' or username == None:
            dispatcher.utter_message(text='I do not recognize you.')
            # evt = FollowupAction(name= "utter_ask_name")
            evt = FollowupAction(name= "update_user_database")
            return[evt]
        else:            
            if username not in USERS:
                dispatcher.utter_message(text=f'Hello {username}!')
                USERS.append(username) #also we have to update database in main fcn and speaker identification fcn
                evt = FollowupAction(name= "update_user_database")
                return[evt]
            else:
                chatbot_response.publish(username)


        return []



class UpdateUserDatabase(Action):
    def name(self) -> Text:
        return "update_user_database"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        
        #UPDATE DATABASE
        if username == 'None' or username == None:
            text_to_send = "Undefined"
            chatbot_response.publish(text_to_send)
            evt = FollowupAction(name= "utter_ask_name")
        else:
            chatbot_response.publish(username)
            evt = FollowupAction(name= "utter_asistant")
      

        return [evt]



    