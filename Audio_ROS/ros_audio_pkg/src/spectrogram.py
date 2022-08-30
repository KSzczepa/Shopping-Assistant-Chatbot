#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np
import librosa

def pcm_to_float(v):
    ret = np.array(v).astype(np.float32)

    ret /= 32768
    ret[ret > 1] = 1.0
    ret[ret < -1] = -1.
    
    return ret


def callback(data):
    f_data = pcm_to_float(data.data)
    spectrogram = librosa.stft(
        f_data,
        n_fft=2048,
        hop_length=int(16000*0.01),
        win_length=int(16000*0.02),
        window='hann'
    )

    rospy.loginfo("Spectro shape: "+str(spectrogram.shape))

    
def listener():
    rospy.init_node('spectrogram_node', anonymous=True)
    rospy.Subscriber("mic_data", Int16MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()