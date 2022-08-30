#!/usr/bin/python3
from tensorflow.python.ops.gen_logging_ops import Print
import rospy
from std_msgs.msg import Int16MultiArray, String, Int16
import numpy as np
import pickle
import os


from identification.deep_speaker.audio import get_mfcc
from identification.deep_speaker.model import get_deep_speaker
from identification.utils import batch_cosine_similarity, dist2id


REF_PATH = os.path.dirname(os.path.abspath(__file__))
RATE = 16000

# Load model
model = get_deep_speaker(os.path.join(REF_PATH,'deep_speaker.h5'))

n_embs = 0
X = []
y = []

TH = 0.75
last_label = 'None'

pub = rospy.Publisher('username', String, queue_size=10)
pub_to_asr = rospy.Publisher('return_to_listen', Int16, queue_size=10)


def listener():
    rospy.init_node('reidentification_node', anonymous=True)

    global last_label

    while not rospy.is_shutdown():
        data = rospy.wait_for_message("voice_data",Int16MultiArray)

        audio_data = np.array(data.data)

        # to float32
        audio_data = audio_data.astype(np.float32, order='C') / 32768.0

        # Processing
        ukn = get_mfcc(audio_data, RATE)

        # Prediction
        ukn = model.predict(np.expand_dims(ukn, 0))

        if len(X) > 0:
            # Distance between the sample and the support set
            emb_voice = np.repeat(ukn, len(X), 0)

            cos_dist = batch_cosine_similarity(np.array(X), emb_voice)
            
            # Matching
            id_label = dist2id(cos_dist, y, TH, mode='avg')
        
        if len(X) == 0 or id_label is None: #Unnown user
            pub.publish('None')
            newuser = rospy.wait_for_message("user_new_data", String)
            msg = f"speaker_ident: unnown user, base: {y}"
            rospy.loginfo(msg)
            if newuser.data not in y and newuser.data != "Undefined":
                X.append(ukn[0])
                y.append(newuser.data)
                last_label = newuser.data

        else: #User is known
            pub.publish(id_label)
            rospy.wait_for_message("user_new_data", String)
            # rospy.loginfo("speaker_ident: known user")
            last_label = id_label
   
        msg_asr = 1
        pub_to_asr.publish(msg_asr)


if __name__ == '__main__':
    listener()