import cv2
import time
import numpy as np

try:
    import depthai as dai
    DEPTHAI_AVAILABLE = True
except ImportError:
    DEPTHAI_AVAILABLE = False

class CameraSystem:
    def __init__(self, use_oakd=False, width=640, height=480):
        self.use_oakd = use_oakd and DEPTHAI_AVAILABLE
        self.width = width
        self.height = height
        self.cap = None
        self.pipeline = None
        self.device = None
        self.q_rgb = None

        if self.use_oakd:
            self.init_oakd()
        else:
            self.init_webcam()

    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        if not self.cap.isOpened():
            print("❌ ERROR: Could not open webcam (index 0)!")
        else:
            print("✅ Webcam initialized successfully")

    def init_oakd(self):
        self.pipeline = dai.Pipeline()
        cam_rgb = self.pipeline.create(dai.node.ColorCamera)
        cam_rgb.setPreviewSize(self.width, self.height)
        cam_rgb.setInterleaved(False)
        cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
        
        xout_rgb = self.pipeline.create(dai.node.XLinkOut)
        xout_rgb.setStreamName("rgb")
        cam_rgb.preview.link(xout_rgb.input)
        
        self.device = dai.Device(self.pipeline)
        self.q_rgb = self.device.getOutputQueue(name="rgb", maxSize=4, blocking=False)

    def get_frame(self):
        if self.use_oakd:
            in_rgb = self.q_rgb.tryGet()
            if in_rgb is not None:
                return in_rgb.getCvFrame()
            return None
        else:
            ret, frame = self.cap.read()
            if ret:
                return cv2.flip(frame, 1) 
            return None

    def release(self):
        if self.use_oakd:
            if self.device:
                self.device.close()
        else:
            if self.cap:
                self.cap.release()
