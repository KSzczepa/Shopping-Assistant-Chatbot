#!/usr/bin/env python
from cv_bridge import CvBridge
from naoqi import ALProxy
from optparse import OptionParser
from sensor_msgs.msg import Image
import numpy as np
import rospy


TOP_CAMERA = 0
BOTTOM_CAMERA = 1
DEPTH_CAMERA = 2

RES_120P = 0
RES_240P = 1
RES_480P = 2
RES_960P = 3

COLORSPACE_GRAYSCALE = 8
COLORSPACE_RGB = 13

MODE_RGB = 0
MODE_DEPTH = 1
MODE_RGBD = 2

class ImageInputNode:

    def __init__(self, ip, port, resolution=RES_480P, rgb_camera=TOP_CAMERA, fps=20):
        self.fps = fps

        if resolution == RES_120P:
            self.width, self.height = 160, 120
        elif resolution == RES_240P:
            self.width, self.height = 320, 240
        elif resolution == RES_480P:
            self.width, self.height = 640, 480
        elif resolution == RES_960P:
            self.width, self.height = 1280, 960
        else:
            self.width, self.height = None, None
        self.camera = ALProxy("ALVideoDevice", ip, port)
        self.rgb_sub = self.camera.subscribeCamera("RGB Stream", rgb_camera, resolution, COLORSPACE_RGB, self.fps)
        if not self.rgb_sub:
            raise Exception("Camera is not initialized properly")
        self.image_publisher = rospy.Publisher('in_rgb', Image, queue_size=1)
        self.bridge = CvBridge()

    def get_color_frame(self):
        raw_rgb = self.camera.getImageRemote(self.rgb_sub)
        image = np.frombuffer(raw_rgb[6], np.uint8).reshape(raw_rgb[1], raw_rgb[0], 3)
        return image

    def get_fov(self, mode="RGB"):
        hfov, vfov = 0, 0
        if mode == "RGB":
            hfov = 57.2 * np.pi / 180
            vfov = 44.3 * np.pi / 180
        return hfov, vfov
    
    def stop(self):
        self.camera.unsubscribe(self.rgb_sub)

    def start(self):
        rospy.init_node("image_input_node")
        rate = rospy.Rate(self.fps)
        while not rospy.is_shutdown():
            frame = self.get_color_frame()
            if frame is not None:
                msg = self.bridge.cv2_to_imgmsg(frame)
                msg.header.stamp = rospy.Time.now()
                self.image_publisher.publish(msg)
            rate.sleep()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--ip", dest="ip", default="10.0.1.207")
    parser.add_option("--port", dest="port", default=9559)
    (options, args) = parser.parse_args()
    try:
        image_input = ImageInputNode(options.ip, int(options.port))
        image_input.start()
    except rospy.ROSInterruptException:
        pass